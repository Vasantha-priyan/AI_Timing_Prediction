"""
Multi-Corner Multi-Mode (MCMM) Static Timing Analysis (STA) Engine
Simulates and evaluates Static Timing Analysis across PVT (Process, Voltage, Temperature) corners:
1. SS_0P9V_125C (Slow-Slow Worst Case Setup Corner)
2. TT_1P1V_25C (Typical Operating Corner)
3. FF_1P21V_M40C (Fast-Fast Best Case Hold Corner)
"""

import numpy as np
from typing import Dict, Any
import plotly.graph_objects as go

class MCMMTimingAnalyzer:
    """
    Enterprise PVT Multi-Corner STA Engine for Nangate 45nm Library.
    """
    def __init__(self):
        # PVT Corner Derating Parameters (Alpha Power-Law Model)
        self.corners = {
            "SS_0P9V_125C": {
                "name": "Slow-Slow (Worst Setup)",
                "voltage": 0.90,
                "temp": 125,
                "delay_factor": 1.45,
                "hold_factor": 0.85,
                "color": "#DC2626" # Red
            },
            "TT_1P1V_25C": {
                "name": "Typical-Typical (Nominal)",
                "voltage": 1.10,
                "temp": 25,
                "delay_factor": 1.00,
                "hold_factor": 1.00,
                "color": "#2563EB" # Blue
            },
            "FF_1P21V_M40C": {
                "name": "Fast-Fast (Worst Hold)",
                "voltage": 1.21,
                "temp": -40,
                "delay_factor": 0.68,
                "hold_factor": 1.35,
                "color": "#16A34A" # Green
            }
        }

    def analyze_all_corners(self, clock_period: float, nominal_critical_path: float, logic_depth: int) -> Dict[str, Any]:
        """
        Computes Setup & Hold slack across all 3 PVT corners.
        """
        corner_results = {}
        
        for corner_id, cfg in self.corners.items():
            # Derated delay calculation
            derated_delay = nominal_critical_path * cfg["delay_factor"]
            
            # Setup Slack: WNS_setup = Clock_Period - Critical_Path_Delay - Setup_Time
            setup_time = 0.08  # 80ps setup time constraint
            wns_setup = clock_period - derated_delay - setup_time
            
            # Hold Slack: WNS_hold = Min_Path_Delay - Hold_Time
            min_path_delay = (derated_delay / (logic_depth if logic_depth > 0 else 1)) * 1.2 * (1.0 / cfg["hold_factor"])
            hold_time = 0.05   # 50ps hold time constraint
            wns_hold = min_path_delay - hold_time
            
            # Calculate TNS & Failing Endpoints
            is_setup_viol = wns_setup < 0
            is_hold_viol = wns_hold < 0
            
            failing_endpoints = max(0, int(abs(wns_setup) * 15)) if is_setup_viol else 0
            tns = round(wns_setup * failing_endpoints, 3) if is_setup_viol else 0.0
            
            corner_results[corner_id] = {
                "corner_name": cfg["name"],
                "voltage": cfg["voltage"],
                "temperature": cfg["temp"],
                "derated_delay": round(derated_delay, 3),
                "wns_setup": round(wns_setup, 3),
                "wns_hold": round(wns_hold, 3),
                "tns": tns,
                "failing_endpoints": failing_endpoints,
                "setup_violation": is_setup_viol,
                "hold_violation": is_hold_viol,
                "color": cfg["color"]
            }
            
        return corner_results

    def generate_mcmm_comparison_chart(self, corner_results: Dict[str, Any]) -> go.Figure:
        """
        Generates a 3-Corner Setup vs Hold Slack Comparison Bar Chart.
        """
        corners = [res["corner_name"] for res in corner_results.values()]
        setup_slacks = [res["wns_setup"] for res in corner_results.values()]
        hold_slacks = [res["wns_hold"] for res in corner_results.values()]
        
        fig = go.Figure()
        
        # Setup Slack Trace
        fig.add_trace(go.Bar(
            x=corners,
            y=setup_slacks,
            name="Setup Slack (WNS Setup)",
            marker_color=["#EF4444" if s < 0 else "#3B82F6" for s in setup_slacks],
            text=[f"{s:+.3f} ns" for s in setup_slacks],
            textposition="auto"
        ))

        # Hold Slack Trace
        fig.add_trace(go.Bar(
            x=corners,
            y=hold_slacks,
            name="Hold Slack (WNS Hold)",
            marker_color=["#F59E0B" if h < 0 else "#10B981" for h in hold_slacks],
            text=[f"{h:+.3f} ns" for h in hold_slacks],
            textposition="auto"
        ))
        
        # Zero Slack Limit Line
        fig.add_hline(y=0.0, line_dash="dash", line_color="#111827", annotation_text="Slack Limit (0.00 ns)")

        fig.update_layout(
            title="⚡ Multi-Corner STA: Setup (WNS) vs Hold Slack Across PVT Corners",
            xaxis_title="PVT Operating Corner",
            yaxis_title="Timing Slack (ns)",
            barmode="group",
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=360,
            margin=dict(l=40, r=40, t=50, b=40),
            font=dict(family="Consolas, monospace", size=12)
        )
        return fig
