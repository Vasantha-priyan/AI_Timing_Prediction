"""
Unit Tests for Report Parser Module
"""

import os
import sys
import pytest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from feature_extraction.report_parser import ReportParser
from eda_flow.run_eda_flow import EDARunner

def test_report_parsing():
    runner = EDARunner(base_dir=BASE_DIR)
    paths = runner.run_flow("mux_2to1", clock_period=1.5, placement_density=0.65, force_mock=True)

    parser = ReportParser()
    metrics = parser.parse_reports(paths["yosys"], paths["openroad"], paths["sta"], "mux_2to1", 1.5, 0.65)

    assert metrics["Design Name"] == "mux_2to1"
    assert metrics["Clock Period"] == 1.5
    assert metrics["Clock Frequency"] > 0.0
    assert metrics["TimingViolation"] in ["YES", "NO"]
