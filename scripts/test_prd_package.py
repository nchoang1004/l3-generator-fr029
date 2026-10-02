"""Test chặn ghi view khi đang review (EXEC §B.17) và đường recovery.

    python3 scripts/test_prd_package.py
"""
import tempfile
import unittest
from pathlib import Path

import prd_package as pp

CHG = "CHG-X-2026-002"


class GuardReviewFreeze(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = pp.AIDE
        pp.AIDE = Path(self.tmp.name)
        (pp.AIDE / "evidence" / "reviews").mkdir(parents=True)

    def tearDown(self):
        pp.AIDE = self.old
        self.tmp.cleanup()

    def review(self, chg, baseline):
        p = pp.AIDE / "evidence" / "reviews" / f"REVIEW-{baseline}.yaml"
        p.write_text(f"change_set: {chg}\nbaseline: {baseline}\n", encoding="utf-8")

    def test_no_review_passes(self):
        pp.guard_review_freeze(CHG)

    def test_review_blocks_plain_render(self):
        self.review(CHG, f"BL-{CHG}-r6")
        with self.assertRaises(pp.Problem):
            pp.guard_review_freeze(CHG)

    def test_recovery_blocks_reviewed_baseline_only(self):
        self.review(CHG, f"BL-{CHG}-r6")
        with self.assertRaises(pp.Problem):
            pp.guard_review_freeze(CHG, f"BL-{CHG}-r6")
        pp.guard_review_freeze(CHG, f"BL-{CHG}-r7")

    def test_recovery_matches_whole_key(self):
        self.review(CHG, f"BL-{CHG}-r10")
        pp.guard_review_freeze(CHG, f"BL-{CHG}-r1")

    def test_other_change_set_does_not_block(self):
        self.review("CHG-OTHER-2026-001", "BL-CHG-OTHER-2026-001-r6")
        pp.guard_review_freeze(CHG)


if __name__ == "__main__":
    unittest.main()
