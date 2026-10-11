"""
2D Multi-Layer GCell Routing Congestion & Metal Layer Heatmap Generator
Simulates physical layout GCell routing tracks across metal layers (M1 to M7) in OpenROAD.
Highlights layout congestion hotspots, pin density bottlenecks, and routing overflows.
"""

import numpy as np
from typing import Dict, Any
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class LayoutCongestionMapper:
    """
    Enterprise GCell Routing Congestion Mapper for OpenROAD 2.0 Physical Design Sign-off.
    """
    def __init__(self, grid_size: int = 16):
        self.grid_size = grid_size

    def generate_congestion_grid(self, congestion_level: float = 75.0, seed: int = 42) -> Dict[str, Any]:
        """
        Generates 2D GCell routing congestion density matrix (0% - 100%) and Metal Layer breakdown.
        """
        np.random.seed(seed)
        
        # Base background routing density
        base_matrix = np.random.uniform(20.0, 50.0, size=(self.grid_size, self.grid_size))
        
        # Add high congestion hotspots near center/critical paths
        cx, cy = self.grid_size // 2, self.grid_size // 2
        hotspot_radius = 4
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                dist = np.sqrt((i - cx)**2 + (j - cy)**2)
                if dist <= hotspot_radius:
                    boost = (congestion_level / 100.0) * (1.0 - (dist / hotspot_radius)) * 55.0
                    base_matrix[i, j] += boost

        # Cap matrix values to [10.0, 100.0]
        congestion_matrix = np.clip(base_matrix, 10.0, 98.0)
        
        # Calculate Metal Layer Track Utilization (M1 to M7)
        metal_layers = {
            "M1 (Pin/StdCell)": round(float(np.mean(congestion_matrix) * 1.15), 1),
            "M2 (Horizontal)": round(float(np.mean(congestion_matrix) * 1.05), 1),
            "M3 (Vertical)": round(float(np.mean(congestion_matrix) * 0.95), 1),
            "M4 (Horizontal)": round(float(np.mean(congestion_matrix) * 0.85), 1),
            "M5 (Vertical)": round(float(np.mean(congestion_matrix) * 0.70), 1),
            "M6 (Power/Clock)": round(float(np.mean(congestion_matrix) * 0.50), 1),
            "M7 (Global Clock)": round(float(np.mean(congestion_matrix) * 0.35), 1),
        }
        
        # Count hotspot GCells exceeding 80% threshold
        hotspot_gcells = int(np.sum(congestion_matrix > 80.0))
        max_overflow = round(float(np.max(congestion_matrix)), 1)
        avg_utilization = round(float(np.mean(congestion_matrix)), 1)

        return {
            "matrix": congestion_matrix,
            "metal_layers": metal_layers,
            "hotspot_gcells": hotspot_gcells,
            "max_overflow_pct": max_overflow,
            "avg_utilization_pct": avg_utilization
        }

    def generate_congestion_heatmap_chart(self, grid_data: Dict[str, Any]) -> go.Figure:
        """
        Generates 2D GCell Routing Congestion Heatmap & Metal Layer Utilization Bar Subplots.
        """
        matrix = grid_data["matrix"]
        metal_layers = grid_data["metal_layers"]
        
        fig = make_subplots(
            rows=1, cols=2,
            column_widths=[0.60, 0.40],
            subplot_titles=("🗺️ 2D GCell Layout Routing Congestion Heatmap", "📊 Metal Layer Track Utilization (M1 - M7)"),
            horizontal_spacing=0.12
        )

        # 1. 2D Heatmap
        fig.add_trace(
            go.Heatmap(
                z=matrix,
                colorscale=[
                    [0.0, "#10B981"],   # Green (<40%)
                    [0.4, "#3B82F6"],   # Blue (40-60%)
                    [0.7, "#F59E0B"],   # Yellow/Orange (60-80%)
                    [1.0, "#EF4444"]    # Red (>80% Congested Hotspot)
                ],
                zmin=0, zmax=100,
                colorbar=dict(title="Track Util %", len=0.8, x=0.54),
                hovertemplate="GCell X: %{x}<br>GCell Y: %{y}<br>Congestion: %{z:.1f}%<extra></extra>"
            ),
            row=1, col=1
        )

        # 2. Metal Layer Bar Chart
        m_names = list(metal_layers.keys())
        m_vals = list(metal_layers.values())
        colors = ["#EF4444" if v > 80 else "#F59E0B" if v > 65 else "#3B82F6" for v in m_vals]

        fig.add_trace(
            go.Bar(
                x=m_vals,
                y=m_names,
                orientation='h',
                marker_color=colors,
                text=[f"{v:.1f}%" for v in m_vals],
                textposition="auto"
            ),
            row=1, col=2
        )

        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=380,
            margin=dict(l=40, r=40, t=60, b=40),
            font=dict(family="Consolas, monospace", size=11),
            showlegend=False
        )
        return fig
