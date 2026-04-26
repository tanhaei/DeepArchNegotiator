from __future__ import annotations
import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/"src"))
from deep_arch_negotiator.core import ArchitectureImpactOracle, ArchitectureConsistencyGuard, negotiate
from deep_arch_negotiator.data import PROPOSALS

class CoreTest(unittest.TestCase):
    def test_oracle_and_guard(self):
        props={p.id:p for p in PROPOSALS}; oracle=ArchitectureImpactOracle(); guard=ArchitectureConsistencyGuard()
        direct=oracle.predict(props["direct_db"]); gateway=oracle.predict(props["gateway_event"])
        self.assertEqual(direct.delta_coupling, 0.42); self.assertEqual(gateway.delta_coupling, 0.08)
        self.assertLess(gateway.architecture_cost(), direct.architecture_cost())
        self.assertFalse(guard.check(props["direct_db"], direct).passed)
        self.assertTrue(guard.check(props["gateway_event"], gateway).passed)
    def test_negotiation_selects_gateway(self):
        res=negotiate(); self.assertEqual(res.accepted.id, "gateway_event"); self.assertEqual(res.guard.hard_violation_count, 0); self.assertEqual(res.adoption_rate, 0.85); self.assertGreater(res.nash_score, 0.30)
if __name__ == "__main__": unittest.main()
