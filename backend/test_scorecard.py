import unittest
from energy_efficiency_scorecard import EnergyEfficiencyScorecard


class TestEnergyEfficiencyScorecard(unittest.TestCase):
    def test_efficient_home(self):
        # Extremely efficient home: low consumption density, high insulation, high appliances
        res = EnergyEfficiencyScorecard.get_score_and_plan(
            home_size_sqft=2000,
            consumption_kwh=600,   # density = 0.3 (should score 40/40)
            insulation_level="excellent", # 30/30
            appliance_efficiency="high" # 30/30
        )
        self.assertEqual(res["score"], 100)
        self.assertEqual(res["rating"], "A (Highly Efficient)")
        self.assertIn("lower", res["benchmark"]["comparison"])
        self.assertIn("Solar & Storage", "".join(res["improvement_plan"]))

    def test_inefficient_home(self):
        # Inefficient home: high consumption density, poor insulation, low appliances
        res = EnergyEfficiencyScorecard.get_score_and_plan(
            home_size_sqft=1000,
            consumption_kwh=2200,   # density = 2.2 (should score 0/40)
            insulation_level="poor", # 6/30
            appliance_efficiency="low" # 10/30
        )
        self.assertEqual(res["score"], 16)
        self.assertEqual(res["rating"], "F (Inefficient)")
        self.assertIn("higher", res["benchmark"]["comparison"])
        self.assertIn("Upgrade Insulation", "".join(res["improvement_plan"]))
        self.assertIn("Replace Old Appliances", "".join(res["improvement_plan"]))
        self.assertIn("Install Smart Thermostat", "".join(res["improvement_plan"]))
        self.assertIn("Professional Audit", "".join(res["improvement_plan"]))

    def test_average_home(self):
        res = EnergyEfficiencyScorecard.get_score_and_plan(
            home_size_sqft=1500,
            consumption_kwh=1500,   # density = 1.0 (scores 25.0/40)
            insulation_level="average", # 18/30
            appliance_efficiency="medium" # 20/30
        )
        # Score should be round(25.0 + 18.0 + 20.0) = 63 (D)
        self.assertEqual(res["score"], 63)
        self.assertEqual(res["rating"], "D (Below Average)")
        self.assertIn("Optimize Appliances", "".join(res["improvement_plan"]))

    def test_invalid_parameters(self):
        # Invalid home size
        with self.assertRaises(ValueError):
            EnergyEfficiencyScorecard.get_score_and_plan(0, 500, "good", "medium")
        with self.assertRaises(ValueError):
            EnergyEfficiencyScorecard.get_score_and_plan(-100, 500, "good", "medium")

        # Negative consumption
        with self.assertRaises(ValueError):
            EnergyEfficiencyScorecard.get_score_and_plan(1000, -1, "good", "medium")

        # Invalid insulation level
        with self.assertRaises(ValueError):
            EnergyEfficiencyScorecard.get_score_and_plan(1000, 500, "superb", "medium")

        # Invalid appliance efficiency
        with self.assertRaises(ValueError):
            EnergyEfficiencyScorecard.get_score_and_plan(1000, 500, "good", "ultra")


if __name__ == "__main__":
    unittest.main()
