from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.routing_service import build_service


class LeadRoutingServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = build_service(ROOT)

    def test_summary_shape(self) -> None:
        summary = self.service.summary()
        self.assertEqual(summary["brokerage"], "Northstar Residential Group")
        self.assertGreater(summary["leadCount"], 0)

    def test_luxury_boston_multifamily_routes_to_marcus(self) -> None:
        lead = self.service.lead("lead-9002")
        self.assertIsNotNone(lead)
        self.assertEqual(lead["primaryAgent"], "Marcus Lee")

    def test_newton_luxury_routes_to_priya(self) -> None:
        lead = self.service.lead("lead-9004")
        self.assertIsNotNone(lead)
        self.assertEqual(lead["primaryAgent"], "Priya Nair")


if __name__ == "__main__":
    unittest.main()
