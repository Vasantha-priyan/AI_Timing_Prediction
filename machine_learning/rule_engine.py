"""
Rule-Based Prediction Engine (Random Forest Surrogate Backup)
Provides zero-shot timing violation predictions based on established VLSI physical design heuristics.
"""

import logging
from typing import Dict, Any, Tuple, List

logger = logging.getLogger("RuleEngine")

class RuleBasedPredictor:
    def __init__(self):
        pass

    def predict_sample(self, sample: Dict[str, Any]) -> Tuple[str, float, float, List[str]]:
        """
        Evaluates physical design features and returns (prediction_label, confidence, probability, violation_reasons).
        """
        score = 0.0
        reasons = []

        clk = sample.get("Clock Period", 2.0)
        critical_path = sample.get("Estimated Critical Path Length", sample.get("Critical Path Estimate", 1.8))
        fanout = sample.get("Maximum Fanout", 10)
        depth = sample.get("Logic Depth", 10)
        congestion = sample.get("Routing Congestion", 60.0)
        utilization = sample.get("Cell Utilization", sample.get("Placement Density", 0.65))

        # Rule 1: Delay Exceeds Clock Period
        if critical_path >= clk:
            score += 0.40
            reasons.append(f"Critical path delay ({critical_path:.3f}ns) exceeds clock period ({clk:.3f}ns).")
        elif critical_path >= 0.85 * clk:
            score += 0.20
            reasons.append(f"Critical path delay consumes { (critical_path/clk)*100:.1f}% of clock period budget.")

        # Rule 2: Maximum Fanout > 20
        if fanout > 20:
            score += 0.25
            reasons.append(f"Maximum fanout of {fanout} exceeds safe threshold (20). High parasitic load capacitance.")
        elif fanout > 14:
            score += 0.10

        # Rule 3: Logic Depth > 15
        if depth > 15:
            score += 0.25
            reasons.append(f"Combinational logic depth of {depth} gates exceeds threshold (15).")
        elif depth > 12:
            score += 0.10

        # Rule 4: Utilization > 80%
        if utilization > 0.80:
            score += 0.20
            reasons.append(f"Cell placement utilization ({utilization*100:.1f}%) exceeds maximum density threshold (80%).")

        # Rule 5: Routing Congestion > 75%
        if congestion > 75.0:
            score += 0.20
            reasons.append(f"Routing congestion ({congestion:.1f}%) causes severe net detour delays.")

        # Normalize probability [0, 1]
        prob = min(0.99, max(0.01, score))
        is_violation = (prob >= 0.50)
        label = "YES" if is_violation else "NO"
        confidence = (prob if is_violation else (1.0 - prob)) * 100.0

        if not reasons and not is_violation:
            reasons.append("All microarchitectural and physical layout parameters are within timing budgets.")

        return label, confidence, prob, reasons

if __name__ == "__main__":
    predictor = RuleBasedPredictor()
    test_s = {"Clock Period": 1.5, "Estimated Critical Path Length": 1.7, "Maximum Fanout": 22, "Logic Depth": 16}
    lbl, conf, pr, rsn = predictor.predict_sample(test_s)
    print(f"Prediction: {lbl}, Conf: {conf:.1f}%, Reasons: {rsn}")
