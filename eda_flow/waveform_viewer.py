"""
Cadence SimVision / ModelSim Style Digital Timing Waveform Generator
Generates interactive digital signal step waveforms and setup slack timing windows using Plotly.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_digital_waveform(design_name: str, clock_period: float = 1.0, is_violation: bool = False, critical_path: float = 1.85):
    """
    Generates an interactive Plotly digital timing waveform figure representing CLK, A, B, S, and Y/P output signals,
    along with setup time arrival and WNS slack margins.
    """
    # Time axis (0 to 5 clock cycles)
    cycles = 5
    t_end = cycles * clock_period
    time_pts = np.linspace(0, t_end, 500)

    # 1. Clock Signal (CLK)
    clk = np.where((time_pts % clock_period) < (clock_period / 2.0), 1, 0)

    # 2. Input Signal A
    sig_A = np.where(time_pts < (1.5 * clock_period), 0, 1)

    # 3. Input Signal B
    sig_B = np.where((time_pts >= 0.5 * clock_period) & (time_pts < 2.5 * clock_period), 1, 0)

    # 4. Transistor Select Signal S (XOR: A ^ B)
    sig_S = np.bitwise_xor(sig_A.astype(int), sig_B.astype(int))

    # 5. Output Signal Y / P (Propagated after critical path delay)
    delay = critical_path if is_violation else min(critical_path, clock_period * 0.78)
    sig_Y = np.where(time_pts >= (1.5 * clock_period + delay), 1, 0)

    fig = make_subplots(
        rows=5, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        subplot_titles=("CLK (System Clock)", "Input A", "Input B", "Node S (CMOS Select Line = A ⊕ B)", f"Output Y / P (Propagated Delay = {delay:.2f} ns)")
    )

    # Custom Cadence SimVision Color Palette
    color_clk = "#005580"
    color_a = "#2E7D32"
    color_b = "#1565C0"
    color_s = "#E65100"
    color_y = "#D32F2F" if is_violation else "#2E7D32"

    fig.add_trace(go.Scatter(x=time_pts, y=clk, mode='lines', name='CLK', line=dict(color=color_clk, width=2.5, shape='vh')), row=1, col=1)
    fig.add_trace(go.Scatter(x=time_pts, y=sig_A, mode='lines', name='Input A', line=dict(color=color_a, width=2.5, shape='vh')), row=2, col=1)
    fig.add_trace(go.Scatter(x=time_pts, y=sig_B, mode='lines', name='Input B', line=dict(color=color_b, width=2.5, shape='vh')), row=3, col=1)
    fig.add_trace(go.Scatter(x=time_pts, y=sig_S, mode='lines', name='Node S', line=dict(color=color_s, width=2.5, shape='vh')), row=4, col=1)
    fig.add_trace(go.Scatter(x=time_pts, y=sig_Y, mode='lines', name='Output Y', line=dict(color=color_y, width=3.0, shape='vh')), row=5, col=1)

    # Highlight Setup Time & Slack Margin Window
    setup_target = clock_period * 2.0
    actual_arrival = 1.5 * clock_period + delay
    slack = setup_target - actual_arrival

    slack_color = "rgba(239, 68, 68, 0.25)" if is_violation else "rgba(16, 185, 129, 0.25)"
    slack_border = "#EF4444" if is_violation else "#10B981"

    fig.add_vrect(
        x0=1.5 * clock_period, x1=actual_arrival,
        fillcolor=slack_color, line_color=slack_border, line_dash="dash",
        annotation_text=f"Path Delay ({delay:.2f} ns) | WNS = {slack:.2f} ns ({'VIOLATION' if is_violation else 'PASS'})",
        annotation_position="top left",
        row="all", col=1
    )

    fig.update_layout(
        title=f"<b>Cadence SimVision Interactive Waveform Window — {design_name}</b>",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F8F9FA",
        font=dict(family="Consolas, Segoe UI, sans-serif", size=11, color="#212529"),
        height=580,
        margin=dict(l=50, r=40, t=60, b=40),
        showlegend=False
    )

    for i in range(1, 6):
        fig.update_yaxes(range=[-0.2, 1.2], tickvals=[0, 1], ticktext=["0", "1"], gridcolor="#E0E0E0", row=i, col=1)
        fig.update_xaxes(gridcolor="#E0E0E0", row=i, col=1)

    fig.update_xaxes(title_text="Time (nanoseconds)", row=5, col=1)

    return fig
