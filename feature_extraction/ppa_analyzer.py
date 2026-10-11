"""
Power, Performance, and Area (PPA) Analysis & Trade-off Explorer
Calculates Dynamic Power, Leakage Power, Internal Power, Total Silicon Area, Gate Equivalents,
and renders PPA Radar Trade-off Maps for 45nm CMOS Technology.
"""

import numpy as np
from typing import Dict, Any
import plotly.graph_objects as go

class PPAAnalyzer:
    """
    Enterprise PPA Analysis Engine for VLSI Physical Sign-off.
    """
    def __init__(self):
        # 45nm Nangate PDK Physical Coefficients
        self.c_load_per_gate = 1.2e-15 # 1.2 fF average load capacitance per gate
        self.leakage_per_gate = 15.0e-9 # 15 nW leakage per gate at 25C
        self.gate_area_nand2 = 1.41 # 1.41 um^2 area of 2-input NAND gate

    def compute_ppa_metrics(self, num_cells: int, clock_period: float, voltage: float = 1.10, activity_factor: float = 0.15) -> Dict[str, Any]:
        """
        Calculates detailed Dynamic Power, Leakage Power, Internal Power, Total Area, and GE count.
        """
        freq_hz = (1.0 / (clock_period * 1e-9)) if clock_period > 0 else 1.0e9
        
        # 1. Total Load Capacitance (Farads)
        c_total = num_cells * self.c_load_per_gate
        
        # 2. Dynamic Switching Power: P_dyn = alpha * C_total * V^2 * f
        p_dynamic_mw = (activity_factor * c_total * (voltage ** 2) * freq_hz) * 1e3
        
        # 3. Internal Power (cell internal capacitance charging/short-circuit)
        p_internal_mw = p_dynamic_mw * 0.35
        
        # 4. Leakage Subthreshold Power: P_leak = num_cells * I_leak * V
        p_leakage_mw = (num_cells * self.leakage_per_gate * voltage) * 1e3
        
        # 5. Total Core Power (mW)
        p_total_mw = p_dynamic_mw + p_internal_mw + p_leakage_mw
        
        # 6. Silicon Die Core Area & Gate Equivalents (GE)
        core_area_um2 = num_cells * self.gate_area_nand2 * 1.35 # 1.35 placement utilization buffer
        gate_equivalents = int(core_area_um2 / self.gate_area_nand2)
        
        # 7. Energy per Operation (pJ)
        energy_per_op_pj = (p_total_mw * clock_period)
        
        # 8. PPA Index Score (0 - 100%)
        # Lower power, lower area, higher frequency yield higher PPA efficiency score
        power_score = max(0.0, 100.0 - (p_total_mw * 2.5))
        area_score = max(0.0, 100.0 - (core_area_um2 / 50.0))
        freq_score = min(100.0, (freq_hz / 1e9) * 50.0)
        ppa_score = round((power_score * 0.4) + (area_score * 0.3) + (freq_score * 0.3), 1)

        return {
            "frequency_ghz": round(freq_hz / 1e9, 3),
            "p_dynamic_mw": round(p_dynamic_mw, 3),
            "p_internal_mw": round(p_internal_mw, 3),
            "p_leakage_mw": round(p_leakage_mw, 3),
            "p_total_mw": round(p_total_mw, 3),
            "core_area_um2": round(core_area_um2, 2),
            "gate_equivalents": gate_equivalents,
            "energy_per_op_pj": round(energy_per_op_pj, 3),
            "ppa_score": ppa_score,
            "power_breakdown": {
                "Dynamic": round(p_dynamic_mw, 3),
                "Internal": round(p_internal_mw, 3),
                "Leakage": round(p_leakage_mw, 3)
            }
        }

    def generate_ppa_radar_chart(self, ppa_metrics: Dict[str, Any]) -> go.Figure:
        """
        Generates an interactive PPA Radar Chart comparing Normalized Performance, Power Efficiency, Area Efficiency, and Timing Margin.
        """
        categories = ['Frequency (GHz)', 'Power Efficiency', 'Area Efficiency', 'Timing Slack Margin', 'Gate Efficiency']
        
        freq_norm = min(100.0, ppa_metrics["frequency_ghz"] * 50.0)
        power_norm = max(10.0, 100.0 - (ppa_metrics["p_total_mw"] * 3.0))
        area_norm = max(10.0, 100.0 - (ppa_metrics["core_area_um2"] / 40.0))
        slack_norm = 85.0 if ppa_metrics["ppa_score"] > 50 else 35.0
        gate_norm = min(100.0, (ppa_metrics["gate_equivalents"] / 1000.0) * 80.0)
        
        values = [freq_norm, power_norm, area_norm, slack_norm, gate_norm]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Observed Design PPA',
            fillcolor='rgba(37, 99, 235, 0.25)',
            line=dict(color='#2563EB', width=2)
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10))
            ),
            title="🎯 PPA Radar Trade-Off Explorer (Power, Performance, Area Normalized)",
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            height=360,
            margin=dict(l=40, r=40, t=50, b=40),
            font=dict(family="Consolas, monospace", size=11)
        )
        return fig
