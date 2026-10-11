"""
Dataset Generator Module
Sweeps benchmark designs across varying clock constraints and placement densities, parsing metrics into combined_dataset.csv.
"""

import os
import sys
import logging
import pandas as pd
import yaml
from typing import List, Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from eda_flow.run_eda_flow import EDARunner, BENCHMARK_PROFILES
from feature_extraction.report_parser import ReportParser

logger = logging.getLogger("DatasetGenerator")

class DatasetGenerator:
    def __init__(self, config_path: str = "config/settings.yaml", base_dir: str = "."):
        self.base_dir = os.path.abspath(base_dir)
        self.config_path = os.path.join(self.base_dir, config_path)
        self.dataset_dir = os.path.join(self.base_dir, "dataset")
        os.makedirs(self.dataset_dir, exist_ok=True)

        self.eda_runner = EDARunner(base_dir=self.base_dir)
        self.parser = ReportParser()

        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f: self.config = yaml.safe_load(f)
        else:
            self.config = {}

    def generate_dataset(self, force_mock: bool = True) -> pd.DataFrame:
        clock_periods = self.config.get("dataset", {}).get("clock_period_sweep", [0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0])
        placement_densities = self.config.get("dataset", {}).get("placement_densities", [0.40, 0.50, 0.60, 0.70, 0.85])
        benchmarks = list(BENCHMARK_PROFILES.keys())

        records: List[Dict[str, Any]] = []
        logger.info(f"Generating dataset across {len(benchmarks)} benchmarks, {len(clock_periods)} T_clk values, and {len(placement_densities)} densities...")

        for design in benchmarks:
            for clk in clock_periods:
                for density in placement_densities:
                    rpt_paths = self.eda_runner.run_flow(design, clock_period=clk, placement_density=density, force_mock=force_mock)
                    record = self.parser.parse_reports(
                        yosys_path=rpt_paths["yosys"],
                        openroad_path=rpt_paths["openroad"],
                        sta_path=rpt_paths["sta"],
                        design_name=design,
                        clock_period=clk,
                        placement_density=density
                    )
                    records.append(record)

        df = pd.DataFrame(records)
        df.drop_duplicates(inplace=True)
        df.ffill(inplace=True)

        output_path = os.path.join(self.base_dir, self.config.get("dataset", {}).get("output_csv", "dataset/combined_dataset.csv"))
        df.to_csv(output_path, index=False)
        logger.info(f"Dataset generated cleanly! Saved {len(df)} records to {output_path}")
        return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    gen = DatasetGenerator()
    df = gen.generate_dataset(force_mock=True)
    print("Dataset Shape:", df.shape)
