"""
VLSI Timing Closure Optimization Recommendation Engine
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger("OptimizationEngine")

class OptimizationEngine:
    def __init__(self):
        self.fanout_threshold = 20
        self.logic_depth_threshold = 15
        self.congestion_threshold = 75.0
        self.placement_density_threshold = 0.80
        self.wirelength_threshold_per_cell = 25.0

    def generate_recommendations(self, sample_features: Dict[str, Any], is_violation: bool = True) -> List[Dict[str, str]]:
        recommendations = []

        clock_period = sample_features.get("Clock Period", 2.0)
        critical_path = sample_features.get("Estimated Critical Path Length", sample_features.get("Critical Path Estimate", 1.8))
        fanout = sample_features.get("Maximum Fanout", 10)
        logic_depth = sample_features.get("Logic Depth", 10)
        congestion = sample_features.get("Routing Congestion", 60.0)
        density = sample_features.get("Placement Density", sample_features.get("Cell Utilization", 0.65))
        cells = max(1, sample_features.get("Number of Standard Cells", 100))
        wire_length = sample_features.get("Estimated Wire Length", 2000.0)

        # 1. Fanout Optimization
        if fanout > self.fanout_threshold:
            recommendations.append({
                "Parameter": "Maximum Fanout",
                "Observed Value": f"{fanout}",
                "Status": "HIGH",
                "Action": "Reduce Fanout / Insert Buffer Trees",
                "Description": f"Fanout of {fanout} exceeds threshold ({self.fanout_threshold}). Insert clock/signal buffers or clone driving logic gates to distribute heavy load capacitance."
            })

        # 2. Logic Depth / Pipelining
        if logic_depth > self.logic_depth_threshold:
            recommendations.append({
                "Parameter": "Logic Depth",
                "Observed Value": f"{logic_depth} gates",
                "Status": "HIGH",
                "Action": "Insert Pipeline Registers / Logic Retiming",
                "Description": f"Combinational logic path depth of {logic_depth} is excessive. Break long critical combinational chains by inserting pipeline register stages."
            })

        # 3. Routing Congestion & Placement
        if congestion > self.congestion_threshold:
            recommendations.append({
                "Parameter": "Routing Congestion",
                "Observed Value": f"{congestion:.1f}%",
                "Status": "HIGH",
                "Action": "Improve Placement / Expand Core Area",
                "Description": f"Routing congestion of {congestion:.1f}% causes net detour and parasitic RC delay spikes. Apply placement blockages or expand die area."
            })

        # 4. Placement Density & Utilization
        if density > self.placement_density_threshold:
            recommendations.append({
                "Parameter": "Placement Density",
                "Observed Value": f"{density:.2f}",
                "Status": "HIGH",
                "Action": "Reduce Target Utilization",
                "Description": f"Placement utilization of {density*100:.1f}% restricts cell movements during optimization. Reduce target utilization to ~0.65 to enable buffer insertion."
            })

        # 5. Wire Length & Detours
        wl_per_cell = wire_length / cells
        if wl_per_cell > self.wirelength_threshold_per_cell:
            recommendations.append({
                "Parameter": "Estimated Wire Length",
                "Observed Value": f"{wire_length:.1f} um ({wl_per_cell:.1f} um/cell)",
                "Status": "HIGH",
                "Action": "Re-route Critical Nets & Bound Region Placement",
                "Description": f"Interconnect wire length per cell is high. Tighten bounding box placement constraints on long nets to reduce wire capacitance."
            })

        # 6. Critical Path & Gate Sizing
        if critical_path >= 0.85 * clock_period or is_violation:
            recommendations.append({
                "Parameter": "Critical Path Delay",
                "Observed Value": f"{critical_path:.3f} ns (Clock: {clock_period:.3f} ns)",
                "Status": "CRITICAL",
                "Action": "Cell Upsizing & High-Vt to Low-Vt Transistor Swapping",
                "Description": f"Critical path delay consumes { (critical_path/clock_period)*100:.1f}% of clock cycle budget. Upsize drive-strength of gates along critical path and perform LVT cell swapping."
            })

        if not recommendations:
            recommendations.append({
                "Parameter": "Overall Design Constraints",
                "Observed Value": "Optimal",
                "Status": "NORMAL",
                "Action": "No Timing Optimization Required",
                "Description": "Design parameters satisfy setup timing margins without violation risks."
            })

        return recommendations

if __name__ == "__main__":
    pass
