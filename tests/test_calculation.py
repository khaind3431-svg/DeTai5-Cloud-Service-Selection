import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from calculation import calculate_tco, normalize_benefit, normalize_cost, rank_providers


CSV_PATH = ROOT / "data" / "providers.csv"


def sample_data():
    return pd.DataFrame(
        {
            "provider": ["A", "B", "C"],
            "sla_percent": [99.9, 99.95, 99.99],
            "compute_monthly_vnd": [100, 120, 150],
            "storage_monthly_vnd": [10, 10, 10],
            "network_monthly_vnd": [10, 10, 10],
            "support_monthly_vnd": [10, 10, 10],
            "operations_monthly_vnd": [10, 10, 10],
            "migration_one_time_vnd": [100, 100, 100],
            "risk_level": [4, 3, 2],
        }
    )


class CalculationTest(unittest.TestCase):
    def test_normalize_benefit(self):
        score = normalize_benefit(pd.Series([10, 20, 30]))
        self.assertEqual(list(score.round(2)), [0.0, 50.0, 100.0])

    def test_normalize_cost(self):
        score = normalize_cost(pd.Series([10, 20, 30]))
        self.assertEqual(list(score.round(2)), [100.0, 50.0, 0.0])

    def test_calculate_tco(self):
        data = sample_data()
        result = calculate_tco(data, 12)
        self.assertEqual(result.iloc[0], 1780)

    def test_rank_providers_returns_highest_score_first(self):
        result = rank_providers(sample_data(), 12, 40, 35, 25)
        self.assertGreaterEqual(result.iloc[0]["total_score"], result.iloc[1]["total_score"])
        self.assertGreaterEqual(result.iloc[1]["total_score"], result.iloc[2]["total_score"])


class DemoCloudDataTest(unittest.TestCase):
    def test_csv_has_real_cloud_providers(self):
        data = pd.read_csv(CSV_PATH)
        self.assertEqual(
            list(data["provider"]),
            ["AWS", "Azure", "Google Cloud", "FPT Cloud", "Viettel IDC"],
        )

    def test_demo_default_weights_ranks_real_providers(self):
        data = pd.read_csv(CSV_PATH)
        result = rank_providers(data, 36, 40, 35, 25)
        self.assertEqual(len(result), 5)
        self.assertGreaterEqual(
            result.iloc[0]["total_score"], result.iloc[-1]["total_score"]
        )
        self.assertIn(result.iloc[0]["provider"], ["FPT Cloud", "Viettel IDC"])


if __name__ == "__main__":
    unittest.main()
