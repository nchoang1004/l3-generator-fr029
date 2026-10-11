"""Đợt 8: ZIP intake (API-002 §2, §5; TM-SYS-L3GEN). Archives are built in the test; nothing is extracted to disk."""
from __future__ import annotations

import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import contracts  # noqa: E402
from l3slice import snapshot  # noqa: E402

FILES = {"app/main.py": b"from fastapi import FastAPI\r\napp = FastAPI()\n", "README.md": b"# x\n",
         "requirements.txt": b"fastapi\n"}


class Zip(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def make(self, entries, name="in.zip"):
        path = self.dir / name
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
            for entry in entries:
                if isinstance(entry, zipfile.ZipInfo):
                    zf.writestr(entry, b"x")
                else:
                    zf.writestr(*entry)
        return path

    def refused(self, path, code):
        before = sorted(p.name for p in self.dir.rglob("*"))
        with self.assertRaises(snapshot.IntakeError) as e:
            snapshot.take_zip(path, "run_z")
        self.assertEqual(e.exception.code, code)
        contracts.validate(e.exception.payload, 2, "SnapshotError")
        self.assertEqual(sorted(p.name for p in self.dir.rglob("*")), before)  # nothing written

    def test_same_bytes_as_local_give_same_snapshot(self):
        local = self.dir / "src"
        for rel, data in FILES.items():
            (local / rel).parent.mkdir(parents=True, exist_ok=True)
            (local / rel).write_bytes(data)
        snap_l, src_l = snapshot.take(local)
        snap_z, src_z = snapshot.take_zip(self.make(list(FILES.items())))
        contracts.validate(snap_z, 2, "Snapshot")
        self.assertEqual(snap_z["snapshot_id"], snap_l["snapshot_id"])
        self.assertEqual(src_z, src_l)
        self.assertEqual(snap_z["excluded"], [{"path": "README.md", "reason": "Chỉ đọc file .py và manifest Python"}])

    def test_path_escape(self):
        for i, bad in enumerate(["../outside.py", "/abs.py", "a/../../b.py", "a\\b.py", "C:x.py", "a//b.py", "./a.py"]):
            with self.subTest(bad=bad):
                raw = zipfile.ZipInfo("placeholder")
                raw.filename = bad  # bypass zipfile's own name cleaning
                self.refused(self.make([("ok.py", b""), raw], name=f"e{i}.zip"), "PATH_ESCAPE")

    def test_link_and_special_entries(self):
        link = zipfile.ZipInfo("link.py")
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        self.refused(self.make([link]), "LINK_NOT_ALLOWED")
        fifo = zipfile.ZipInfo("pipe.py")
        fifo.external_attr = (stat.S_IFIFO | 0o644) << 16
        self.refused(self.make([fifo], "f.zip"), "ZIP_INVALID")

    def test_collisions_and_reserved_names(self):
        self.refused(self.make([("A.py", b""), ("a.py", b"")]), "PATH_COLLISION")
        self.refused(self.make([("café.py", b""), ("café.py", b"")], "u.zip"), "PATH_COLLISION")
        self.refused(self.make([("con.py", b"")], "r.zip"), "PATH_COLLISION")
        self.refused(self.make([("x.py.", b"")], "d.zip"), "PATH_COLLISION")

    def test_not_a_zip(self):
        path = self.dir / "fake.zip"
        path.write_bytes(b"not a zip")
        self.refused(path, "ZIP_INVALID")

    def test_limits_at_and_over(self):
        path = self.make([("a.py", b"12345"), ("b.py", b"678")])
        with mock.patch.object(snapshot, "ZIP_MAX_UNCOMPRESSED", 8):
            snapshot.take_zip(path)
        with mock.patch.object(snapshot, "ZIP_MAX_UNCOMPRESSED", 7):
            self.refused(path, "INTAKE_LIMIT")
        with mock.patch.object(snapshot, "ZIP_MAX_FILES", 2):
            snapshot.take_zip(path)
        with mock.patch.object(snapshot, "ZIP_MAX_FILES", 1):
            self.refused(path, "INTAKE_LIMIT")
        size = path.stat().st_size
        with mock.patch.object(snapshot, "ZIP_MAX_COMPRESSED", size):
            snapshot.take_zip(path)
        with mock.patch.object(snapshot, "ZIP_MAX_COMPRESSED", size - 1):
            self.refused(path, "INTAKE_LIMIT")

    def test_header_size_is_not_trusted(self):
        path = self.make([("a.py", b"x" * 1000)])
        raw = bytearray(path.read_bytes())
        with zipfile.ZipFile(path) as zf:
            info = zf.infolist()[0]
        # Rewrite the declared uncompressed size in the central directory to 1 byte.
        cd = raw.rfind(b"PK\x01\x02")
        raw[cd + 24:cd + 28] = (1).to_bytes(4, "little")
        path.write_bytes(bytes(raw))
        with mock.patch.object(snapshot, "ZIP_MAX_UNCOMPRESSED", 500):
            with self.assertRaises(snapshot.IntakeError) as e:
                snapshot.take_zip(path)
        self.assertIn(e.exception.code, ("INTAKE_LIMIT", "ZIP_INVALID"))
        self.assertEqual(info.file_size, 1000)


if __name__ == "__main__":
    unittest.main()
