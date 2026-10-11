"""
Unit Tests for Machine Learning Pipeline, Rule Engine, and Optimization Engine
"""

import os
import sys
import pytest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from dataset.dataset_generator import DatasetGenerator
from machine_learning.train_models import MLTrainer
from machine_learning.rule_engine import RuleBasedPredictor
from optimization.recommendation_engine import OptimizationEngine

def test_ml_and_rule_engine():
    gen = DatasetGenerator(base_dir=BASE_DIR)
    df = gen.generate_dataset(force_mock=True)

    assert not df.empty
    assert "TimingViolation" in df.columns
    assert "WNS" not in df.columns

    rule_eng = RuleBasedPredictor()
    label, conf, prob, reasons = rule_eng.predict_sample(df.iloc[0].to_dict())
    assert label in ["YES", "NO"]
    assert 0.0 <= conf <= 100.0

    trainer = MLTrainer(base_dir=BASE_DIR)
    results, best_name, summary_df = trainer.train_and_evaluate(df)

    assert "Random Forest" in results
    assert "Decision Tree" in results
    assert "XGBoost" in results

    eng = OptimizationEngine()
    recs = eng.generate_recommendations(df.iloc[0].to_dict(), is_violation=True)
    assert len(recs) > 0
