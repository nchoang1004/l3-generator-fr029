"""Đợt 5: SVG, isolated artifact failure, retry (API-008 §7) with fault injection."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import contracts  # noqa: E402
from l3slice import extract, model, render, snapshot, verify  # noqa: E402

FIX = HERE / "fixtures"


def verified_of(name="shop_full"):
    snap, sources = snapshot.take(FIX / name)
    inv = snapshot.inventory(snap)
    unit = inv["units"][0]["id"]
    facts = extract.extract(snap, sources, unit)
    membership = json.loads((FIX / f"{name}.membership.json").read_text(encoding="utf-8"))
    return verify.verify(snap, sources, inv, facts, model.build(snap, unit, facts, membership))


def broken_svg(model_, plan):
    raise OSError("disk full while drawing")


def hashes(out: Path) -> dict:
    return {p.relative_to(out).as_posix(): render.sha(p.read_bytes()) for p in out.rglob("*") if p.is_file()}


class Publish(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "out"
        self.bundle = render.render(verified_of(), "run_p", "shop_full", self.out, renderers={"svg": broken_svg})
        self.svg = next(a for a in self.bundle["artifacts"] if a["kind"] == "diagram_image")

    def tearDown(self):
        self.tmp.cleanup()

    def test_one_failed_artifact_does_not_block_others(self):
        contracts.validate(self.bundle, 8, "ResultBundle")
        self.assertEqual(self.svg["status"], "failed")
        self.assertEqual(self.svg["error"]["code"], "RENDER_FAILED")
        self.assertTrue(self.svg["error"]["retryable"])
        self.assertFalse((self.out / "architecture.svg").exists())
        self.assertTrue(all(a["status"] == "ready" for a in self.bundle["artifacts"] if a is not self.svg))

    def test_retry_makes_svg_ready_and_keeps_other_bytes(self):
        before = hashes(self.out)
        after_bundle = render.retry_artifact(self.out, self.svg["artifact_id"])
        contracts.validate(after_bundle, 8, "ResultBundle")
        new = next(a for a in after_bundle["artifacts"] if a["artifact_id"] == self.svg["artifact_id"])
        self.assertEqual(new["status"], "ready")
        render.check_svg(after_bundle["result"]["model"], (self.out / "architecture.svg").read_text(encoding="utf-8"))
        after = hashes(self.out)
        for path, digest in before.items():
            if path != "manifest.json":
                self.assertEqual(after[path], digest, path)
        self.assertEqual(new["sha256"], after["architecture.svg"])
        self.assertEqual({k: v for k, v in after_bundle.items() if k != "artifacts"},
                         json.loads((self.out / "result.json").read_text(encoding="utf-8")))

    def test_crash_between_install_and_manifest_leaves_artifact_failed(self):
        with self.assertRaises(RuntimeError):
            render.retry_artifact(self.out, self.svg["artifact_id"], _crash_after_install=True)
        manifest = json.loads((self.out / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(next(a for a in manifest["artifacts"] if a["kind"] == "diagram_image")["status"], "failed")
        again = render.retry_artifact(self.out, self.svg["artifact_id"])
        self.assertEqual(next(a for a in again["artifacts"] if a["kind"] == "diagram_image")["status"], "ready")

    def test_failed_manifest_replace_keeps_old_manifest(self):
        old = (self.out / "manifest.json").read_bytes()
        real = render.os.replace
        calls = []

        def flaky(src, dst):
            calls.append(dst)
            if str(dst).endswith("manifest.json"):
                raise OSError("permission denied")
            return real(src, dst)
        with mock.patch.object(render.os, "replace", flaky), self.assertRaises(render.ExportError) as e:
            render.retry_artifact(self.out, self.svg["artifact_id"])
        self.assertEqual(e.exception.code, "PUBLISH_FAILED")
        self.assertEqual((self.out / "manifest.json").read_bytes(), old)
        self.assertEqual(sorted(p.name for p in self.out.glob(".manifest*")), [])

    def test_ready_artifact_retry_is_a_no_op(self):
        readme = next(a for a in self.bundle["artifacts"] if a["kind"] == "readme")
        before = (self.out / "manifest.json").read_bytes()
        render.retry_artifact(self.out, readme["artifact_id"])
        self.assertEqual((self.out / "manifest.json").read_bytes(), before)

    def test_changed_ready_file_blocks_retry(self):
        (self.out / "README.md").write_text("đã sửa tay", encoding="utf-8")
        with self.assertRaises(render.ExportError) as e:
            render.retry_artifact(self.out, self.svg["artifact_id"])
        self.assertEqual(e.exception.code, "INVALID_INPUT")

    def test_other_renderer_version_is_refused(self):
        with mock.patch.object(render, "RENDERER_VERSION", "slice-render-v99"), self.assertRaises(render.ExportError) as e:
            render.retry_artifact(self.out, self.svg["artifact_id"])
        self.assertEqual(e.exception.code, "VERSION_UNAVAILABLE")

    def test_format_invalid_is_not_retryable(self):
        manifest = json.loads((self.out / "manifest.json").read_text(encoding="utf-8"))
        target = next(a for a in manifest["artifacts"] if a["kind"] == "api")
        target.update(status="failed", sha256=None, bytes=None,
                      error={"code": "FORMAT_INVALID", "reason": "test", "retryable": False})
        (self.out / "manifest.json").write_text(render.dump(manifest), encoding="utf-8")
        with self.assertRaises(render.ExportError) as e:
            render.retry_artifact(self.out, target["artifact_id"])
        self.assertEqual(e.exception.code, "ARTIFACT_NOT_RETRYABLE")


class SvgCheck(unittest.TestCase):
    def test_script_in_svg_is_rejected(self):
        m = verified_of()["model"]
        _, plan = render.mermaid(m)
        bad = render.svg(m, plan).replace("</svg>", '<script>alert(1)</script></svg>')
        with self.assertRaises(render.ExportError):
            render.check_svg(m, bad)

    def test_missing_edge_in_svg_is_rejected(self):
        m = verified_of()["model"]
        _, plan = render.mermaid(m)
        with self.assertRaises(render.ExportError):
            render.check_svg(m, render.svg(m, dict(plan, edges=[])))


if __name__ == "__main__":
    unittest.main()
