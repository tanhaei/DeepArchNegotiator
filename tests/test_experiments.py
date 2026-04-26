from __future__ import annotations
import sys, unittest, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/"src"))
from deep_arch_negotiator.experiments import run_all

class ExperimentTest(unittest.TestCase):
    def test_run_all(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload=run_all(tmp); out=Path(tmp)
            self.assertEqual(payload["bioarc"]["accepted_proposal"], "gateway_event")
            self.assertTrue((out/"bioarc_result.json").exists())
            self.assertTrue((out/"ablation.svg").exists())
            self.assertTrue((out/"impact_prediction.csv").exists())
if __name__ == "__main__": unittest.main()
