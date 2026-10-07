"""Regression: markdown outside the ingest root must not become lattice nodes via symlinks."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INGEST = REPO_ROOT / "scripts" / "ingest.py"


class TestIngestSymlink(unittest.TestCase):
    def test_symlink_outside_root_is_skipped(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "vault"
            outside = Path(td) / "outside"
            root.mkdir()
            outside.mkdir()
            (root / "inside.md").write_text("# Inside Note\n", encoding="utf-8")
            (outside / "secret.md").write_text("# Outside Secret\n", encoding="utf-8")
            os.symlink(outside / "secret.md", root / "leak.md")

            out = Path(td) / "out"
            subprocess.run(
                [sys.executable, str(INGEST), str(root), "--out", str(out)],
                check=True,
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            lattice = json.loads((out / "lattice.json").read_text(encoding="utf-8"))
            node_ids = {n["id"] for n in lattice["nodes"]}

        self.assertIn("page:inside.md", node_ids)
        self.assertNotIn("page:leak.md", node_ids)
        titles = {n["title"] for n in lattice["nodes"]}
        self.assertIn("Inside Note", titles)
        self.assertNotIn("Outside Secret", titles)


if __name__ == "__main__":
    unittest.main()
