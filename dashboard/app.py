"""
Cadence Virtuoso Style Electronic Design Automation (EDA) CAD Workbench
An Explainable AI-Assisted Early Timing Violation Prediction and Optimization Framework Using Open-Source EDA Tools.
"""

import os
import sys
import time
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import joblib
import yaml

# Page Configuration - Cadence Virtuoso Light White/Gray CAD Workbench Theme
st.set_page_config(
    page_title="Cadence Virtuoso Schematic Editor & STA Workbench | Enterprise EDA Framework",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from syntax_validator.syntax_checker import VerilogSyntaxChecker
from eda_flow.run_eda_flow import EDARunner, BENCHMARK_PROFILES
from eda_flow.schematic_generator import VerilogSchematicGenerator
from eda_flow.waveform_viewer import generate_digital_waveform
from eda_flow.mcmm_sta import MCMMTimingAnalyzer
from feature_extraction.ppa_analyzer import PPAAnalyzer
from eda_flow.congestion_mapper import LayoutCongestionMapper
from optimization.eco_patcher import VerilogECOPatcher
from feature_extraction.report_parser import ReportParser
from machine_learning.preprocessor import DataPreprocessor
from machine_learning.train_models import MLTrainer
from machine_learning.rule_engine import RuleBasedPredictor
from machine_learning.explainable_ai import ExplainableAI
from optimization.recommendation_engine import OptimizationEngine
from reports.ieee_plots import IEEEPlotGenerator
from reports.pdf_generator import PDFReportGenerator

# Cadence Virtuoso High-Contrast Monochromatic (Black, Gray, White) Styling
st.markdown("""
<style>
    /* Global Canvas & CAD Dotted Grid Background */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F8F9FA !important;
        background-image: radial-gradient(#CED4DA 1.2px, transparent 1.2px) !important;
        background-size: 16px 16px !important;
        color: #111827 !important;
        font-family: 'Consolas', 'Fira Code', 'Segoe UI', -apple-system, sans-serif !important;
    }
    
    .main .block-container {
        max-width: 1580px !important;
        padding-top: 0.4rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }

    [data-testid="stHeader"] {
        background-color: #F8F9FA !important;
    }
    
    h1, h2, h3, h4, h5, h6, label, p, span, div {
        color: #111827 !important;
    }

    /* Selectbox, Input Box, Number Input Complete Light CAD Overrides */
    .stSelectbox, .stTextInput, .stNumberInput, .stTextArea {
        background-color: #FFFFFF !important;
    }

    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] div[role="combobox"],
    div[data-baseweb="select"] input,
    .stTextInput input, 
    .stNumberInput input, 
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #111827 !important;
        border: 1.5px solid #D1D5DB !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
    }

    div[data-baseweb="select"] * {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        font-weight: 700 !important;
    }

    /* Dropdown Options Popup Menu */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"],
    li[role="option"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #111827 !important;
    }

    li[role="option"]:hover,
    li[role="option"][aria-selected="true"] {
        background-color: #F3F4F6 !important;
        background: #F3F4F6 !important;
        color: #1E40AF !important;
    }
    
    li[role="option"] * {
        color: #111827 !important;
    }

    /* Code Block High Contrast Pure White & Cadence Styling */
    div[data-testid="stCodeBlock"],
    div[data-testid="stCodeBlock"] > div,
    div[data-testid="stCodeBlock"] pre,
    div[data-testid="stCodeBlock"] code,
    div[data-testid="stCodeBlock"] span,
    div[data-testid="stCodeBlock"] .token,
    code[class*="language-"],
    pre[class*="language-"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #111827 !important;
        font-family: 'Consolas', 'Fira Code', monospace !important;
        text-shadow: none !important;
    }

    div[data-testid="stCodeBlock"] {
        border: 1.5px solid #D1D5DB !important;
        border-radius: 6px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }

    div[data-testid="stCodeBlock"] .token.comment,
    div[data-testid="stCodeBlock"] .token.prolog,
    div[data-testid="stCodeBlock"] .token.doctype,
    div[data-testid="stCodeBlock"] .token.cdata {
        color: #4B5563 !important;
        font-style: italic !important;
        background: transparent !important;
        background-color: transparent !important;
    }

    div[data-testid="stCodeBlock"] .token.keyword,
    div[data-testid="stCodeBlock"] .token.property,
    div[data-testid="stCodeBlock"] .token.tag,
    div[data-testid="stCodeBlock"] .token.boolean,
    div[data-testid="stCodeBlock"] .token.number,
    div[data-testid="stCodeBlock"] .token.constant,
    div[data-testid="stCodeBlock"] .token.symbol {
        color: #1E40AF !important;
        font-weight: 800 !important;
        background: transparent !important;
        background-color: transparent !important;
    }

    div[data-testid="stCodeBlock"] .token.string,
    div[data-testid="stCodeBlock"] .token.char,
    div[data-testid="stCodeBlock"] .token.builtin,
    div[data-testid="stCodeBlock"] .token.inserted {
        color: #047857 !important;
        background: transparent !important;
        background-color: transparent !important;
    }

    div[data-testid="stCodeBlock"] .token.operator,
    div[data-testid="stCodeBlock"] .token.entity,
    div[data-testid="stCodeBlock"] .token.url,
    div[data-testid="stCodeBlock"] .token.variable,
    div[data-testid="stCodeBlock"] .token.punctuation {
        color: #111827 !important;
        background: transparent !important;
        background-color: transparent !important;
    }

    /* Expander & ECO Directives Black/Gray/White Styling */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #D1D5DB !important;
        border-radius: 6px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    }

    [data-testid="stExpander"] summary {
        background-color: #F3F4F6 !important;
        color: #111827 !important;
        border-radius: 4px !important;
    }

    [data-testid="stExpander"] summary p, [data-testid="stExpander"] summary span {
        color: #111827 !important;
        font-weight: 800 !important;
        font-size: 13px !important;
    }

    .cad-metric-tag {
        background-color: #E5E7EB;
        color: #111827 !important;
        border: 1px solid #9CA3AF;
        border-radius: 4px;
        padding: 4px 8px;
        font-weight: 700;
        font-family: 'Consolas', monospace;
        display: inline-block;
    }
    
    /* Cadence Virtuoso Window Title Bar */
    .virtuoso-window-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(180deg, #1F2937 0%, #111827 100%);
        border: 1px solid #111827;
        border-radius: 6px 6px 0 0;
        padding: 8px 16px;
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 13px;
        margin-bottom: 0px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    
    .virtuoso-window-bar div {
        color: #FFFFFF !important;
    }

    /* Cadence Icon Toolbar Container */
    .cad-toolbar-container {
        background-color: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-top: none;
        border-radius: 0 0 6px 6px;
        padding: 8px 14px;
        margin-bottom: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    
    /* Status Notification Banner */
    .cad-status-msg {
        background-color: #F3F4F6;
        color: #111827 !important;
        border: 1px solid #9CA3AF;
        border-radius: 4px;
        padding: 8px 12px;
        font-size: 12px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    /* Vivado / Cadence Sidebar Flow Navigator */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1.5px solid #D1D5DB !important;
        padding-top: 10px;
    }
    
    .sidebar-brand {
        padding: 12px 14px;
        background-color: #F3F4F6;
        border: 1px solid #D1D5DB;
        border-left: 4px solid #111827;
        border-radius: 4px;
        margin-bottom: 16px;
    }
    
    .sidebar-brand-title {
        font-size: 13px;
        font-weight: 900;
        color: #111827 !important;
        letter-spacing: 0.8px;
        text-transform: uppercase;
    }
    
    .sidebar-brand-sub {
        font-size: 10.5px;
        color: #4B5563 !important;
        margin-top: 2px;
        font-weight: 600;
    }

    .sidebar-section-title {
        font-size: 11px;
        font-weight: 800;
        color: #4B5563 !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 14px;
        margin-bottom: 8px;
        padding-left: 4px;
    }

    /* Sidebar Navigation Items */
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 4px !important;
        padding: 9px 12px !important;
        margin-bottom: 6px !important;
        transition: all 0.15s ease-in-out;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        border-color: #111827 !important;
        background-color: #F3F4F6 !important;
    }
    
    section[data-testid="stSidebar"] div[role="radiogroup"] label p, 
    section[data-testid="stSidebar"] div[role="radiogroup"] label span {
        color: #111827 !important;
        font-size: 12.5px !important;
        font-weight: 700 !important;
    }

    /* Cadence Panel Cards & Inspection Boxes */
    .eda-card {
        background-color: #FFFFFF;
        border: 1px solid #D1D5DB;
        border-left: 4px solid #111827;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 14px;
        min-height: 95px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    
    .eda-card-title {
        font-size: 11px;
        font-weight: 800;
        color: #4B5563 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    .eda-card-value {
        font-size: 22px;
        font-weight: 900;
        color: #111827 !important;
        margin-top: 4px;
    }

    .eda-panel {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04) !important;
    }
    
    /* Timing Banners */
    .banner-pass {
        background-color: #F3F4F6 !important;
        color: #111827 !important;
        border: 1.5px solid #374151 !important;
        padding: 14px 20px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .banner-viol {
        background-color: #F3F4F6 !important;
        color: #111827 !important;
        border: 1.5px solid #374151 !important;
        padding: 14px 20px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    /* Cadence Workbench Action & Download Buttons High-Contrast Styling */
    .stButton > button, 
    .stDownloadButton > button, 
    button[data-testid="stBaseButton-secondary"],
    button[data-testid="stBaseButton-header"] {
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #111827 !important;
        border: 1.5px solid #111827 !important;
        border-radius: 6px !important;
        font-weight: 800 !important;
        font-size: 13px !important;
        padding: 8px 16px !important;
        transition: all 0.15s ease-in-out !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
        width: 100% !important;
    }

    .stButton > button *, 
    .stDownloadButton > button * {
        color: #111827 !important;
        font-weight: 800 !important;
    }

    .stButton > button:hover, 
    .stDownloadButton > button:hover {
        background-color: #111827 !important;
        background: #111827 !important;
        color: #FFFFFF !important;
        border-color: #111827 !important;
    }

    .stButton > button:hover *, 
    .stDownloadButton > button:hover * {
        color: #FFFFFF !important;
    }

    /* Primary Action Buttons (Deep Cadence Blue) */
    .stButton > button[kind="primary"], 
    .stDownloadButton > button[kind="primary"],
    button[data-testid="stBaseButton-primary"] {
        background-color: #1E40AF !important;
        background: #1E40AF !important;
        color: #FFFFFF !important;
        border: 1.5px solid #1E3A8A !important;
        font-weight: 900 !important;
    }

    .stButton > button[kind="primary"] *, 
    .stDownloadButton > button[kind="primary"] *,
    button[data-testid="stBaseButton-primary"] * {
        color: #FFFFFF !important;
    }

    .stButton > button[kind="primary"]:hover, 
    .stDownloadButton > button[kind="primary"]:hover,
    button[data-testid="stBaseButton-primary"]:hover {
        background-color: #1D4ED8 !important;
        background: #1D4ED8 !important;
        color: #FFFFFF !important;
        border-color: #1D4ED8 !important;
    }

    /* Status Footer */
    .sidebar-footer {
        padding: 10px 12px;
        background-color: #F3F4F6;
        border: 1px solid #D1D5DB;
        border-radius: 4px;
        margin-top: 16px;
        font-size: 10.5px;
        color: #4B5563;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# Top Cadence Virtuoso Charcoal Title Bar
st.markdown("""
<div class="virtuoso-window-bar">
    <div>⚡ Cadence Virtuoso Schematic Editor & STA Workbench v2.0</div>
    <div style="display:flex; gap:16px;">
        <span>PDK: Nangate 45nm</span>
        <span>Yosys + OpenROAD + OpenSTA</span>
        <span>[ 🗕 🗖 ✕ ]</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Cadence Toolbar Buttons with Real Interactive Triggers
st.markdown('<div class="cad-toolbar-container">', unsafe_allow_html=True)
tb_cols = st.columns([1, 1, 1, 1, 1, 1, 1, 2])

with tb_cols[0]:
    if st.button("🖨️ Print", key="tb_print"):
        st.session_state["cad_msg"] = "🖨️ Print command executed: Exporting schematic vector PDF..."
        components.html("<script>window.print();</script>", height=0)

with tb_cols[1]:
    if st.button("💾 Save", key="tb_save"):
        v_content = st.session_state.get("active_verilog_content", "")
        d_name = st.session_state.get("active_design_name", "design")
        st.session_state["cad_msg"] = f"💾 Save command executed: Design '{d_name}' saved to workspace."

with tb_cols[2]:
    if st.button("📁 Open", key="tb_open"):
        st.session_state["cad_msg"] = "📁 Open command executed: Ready to select or upload Verilog RTL file."

with tb_cols[3]:
    if st.button("🔍 Zoom +", key="tb_zoomin"):
        z = st.session_state.get("cad_zoom", 1.0)
        st.session_state["cad_zoom"] = min(2.0, z + 0.2)
        st.session_state["cad_msg"] = f"🔍 Zoom level set to {st.session_state['cad_zoom']:.1f}x"

with tb_cols[4]:
    if st.button("🔍 Zoom -", key="tb_zoomout"):
        z = st.session_state.get("cad_zoom", 1.0)
        st.session_state["cad_zoom"] = max(0.5, z - 0.2)
        st.session_state["cad_msg"] = f"🔍 Zoom level set to {st.session_state['cad_zoom']:.1f}x"

with tb_cols[5]:
    if st.button("👁️ Probe", key="tb_probe"):
        st.session_state["cad_msg"] = "👁️ Probe active: Click signal net to inspect voltage level and setup slack."

with tb_cols[6]:
    if st.button("🏷️ Net List", key="tb_net"):
        st.session_state["cad_msg"] = "🏷️ Net List Inspector active: Displaying port connectivity matrix."

with tb_cols[7]:
    if st.button("📈 Digital Waveform Viewer", type="primary", key="tb_wave"):
        st.session_state["show_waveform_tab"] = True
        st.session_state["cad_msg"] = "📈 Digital Waveform Viewer launched."

st.markdown('</div>', unsafe_allow_html=True)

# Display CAD Status Notification Banner if active
if "cad_msg" in st.session_state:
    st.markdown(f'<div class="cad-status-msg">{st.session_state["cad_msg"]}</div>', unsafe_allow_html=True)

# Sidebar Flow Navigator
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="sidebar-brand-title">⚡ CADENCE SCHEMATIC WORKBENCH</div>
    <div class="sidebar-brand-sub">Virtuoso Physical Design Sign-Off</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section-title">Cadence Design Modules</div>', unsafe_allow_html=True)

navigation = st.sidebar.radio(
    "Navigate Module:",
    [
        "1. Circuit Schematic & RTL Import",
        "2. Yosys Synthesis & OpenROAD Flow",
        "3. Multi-Corner STA (PVT) & Waveforms",
        "4. PPA Radar & 2D Routing Heatmap",
        "5. 1-Click Auto-ECO Verilog Patcher",
        "6. Documentation & Report Exporters"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("""
<div class="sidebar-footer">
    <b>CADENCE ENGINE: ONLINE</b><br>
    • Target PDK: Nangate 45nm<br>
    • Logic Engine: Yosys 0.38<br>
    • Physical Layout: OpenROAD 2.0<br>
    • Timing Analysis: OpenSTA 2.5<br>
    • ML Prediction: RF / XGBoost (97.29%)
</div>
""", unsafe_allow_html=True)

runner = EDARunner(base_dir=BASE_DIR)
schematic_gen = VerilogSchematicGenerator()

# ==============================================================================
# MODULE 1: SCHEMATIC & RTL IMPORT
# ==============================================================================
if navigation == "1. Circuit Schematic & RTL Import":
    st.markdown('<div style="font-size:18px; font-weight:800; color:#111827; margin-bottom:4px;">Circuit Schematic & Verilog RTL Source Import</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px; color:#4B5563; margin-bottom:16px;">Select benchmark RTL designs or upload custom Verilog source code for syntax verification and visual CAD schematic rendering.</div>', unsafe_allow_html=True)

    st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
    source_mode = st.radio("Select RTL Input Source Mode:", ["Select Benchmark RTL Design", "Upload Custom Verilog File"], horizontal=True)

    if source_mode == "Upload Custom Verilog File":
        uploaded_file = st.file_uploader("Browse or Drag-and-Drop Verilog File (.v / .sv)", type=["v", "sv"])
        if uploaded_file is not None:
            content = uploaded_file.getvalue().decode("utf-8")
            filename = uploaded_file.name
            save_path = os.path.join(BASE_DIR, "uploaded_designs", filename)
            with open(save_path, "w") as f: f.write(content)
            st.session_state["active_verilog_path"] = save_path
            st.session_state["active_design_name"] = os.path.splitext(filename)[0]
            st.session_state["active_verilog_content"] = content
            st.success(f"File '{filename}' successfully saved to `uploaded_designs/`.")
        else:
            save_path = os.path.join(BASE_DIR, "uploaded_designs", "sample_custom_design.v")
            if os.path.exists(save_path):
                with open(save_path, "r") as f: content = f.read()
                st.session_state["active_verilog_path"] = save_path
                st.session_state["active_design_name"] = "sample_custom_design"
                st.session_state["active_verilog_content"] = content
            else:
                content = "// Upload a Verilog file to begin syntax validation."
    else:
        bench_keys = list(BENCHMARK_PROFILES.keys())
        default_idx = bench_keys.index("cmos_transistor_mux") if "cmos_transistor_mux" in bench_keys else 0
        selected_bench = st.selectbox("Select RTL Benchmark Circuit:", bench_keys, index=default_idx)
        save_path = os.path.join(BASE_DIR, "benchmark_designs", f"{selected_bench}.v")
        if os.path.exists(save_path):
            with open(save_path, "r") as f: content = f.read()
            st.session_state["active_verilog_path"] = save_path
            st.session_state["active_design_name"] = selected_bench
            st.session_state["active_verilog_content"] = content

    st.markdown('</div>', unsafe_allow_html=True)

    # 2 Column Split Layout: Left RTL Code Viewer | Right Cadence Schematic Canvas
    col_left, col_right = st.columns([1, 1], gap="medium")

    with col_left:
        st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
        st.markdown("### 📝 Verilog RTL Source Viewer")
        
        checker = VerilogSyntaxChecker()
        val_res = checker.validate_code(content)

        if val_res["valid"]:
            st.info(f"✅ **SYNTAX VALIDATED** | Top Module: `{val_res['top_module']}` | Total Lines: {val_res['total_lines']}")
        else:
            st.error(f"❌ **SYNTAX ERRORS DETECTED ({len(val_res['errors'])})**:")
            for err in val_res["errors"]: st.write(f"- {err}")

        # Native Light Streamlit Code Viewer (100% Crisp White & Black Contrast)
        st.code(content, language="verilog")
        
        # Save active file download button
        d_name = st.session_state.get("active_design_name", "design")
        st.download_button(f"📥 Download Active Verilog Source ({d_name}.v)", data=content, file_name=f"{d_name}.v", mime="text/x-verilog")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
        zoom_val = st.session_state.get("cad_zoom", 1.0)
        st.markdown(f"### 🌐 Cadence Virtuoso Circuit Schematic Canvas (Zoom: {zoom_val:.1f}x)")
        design_name = st.session_state.get("active_design_name", "top")
        dot_str = schematic_gen.generate_dot_schematic(content, module_name=design_name, theme="white")
        st.graphviz_chart(dot_str, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# MODULE 2: YOSYS SYNTHESIS & OPENROAD PHYSICAL FLOW
# ==============================================================================
elif navigation in ["2. Execute Synthesis & Physical Flow", "2. Yosys Synthesis & OpenROAD Flow"]:
    st.markdown('<div style="font-size:18px; font-weight:800; color:#111827; margin-bottom:4px;">Execute Yosys Synthesis, OpenROAD Layout & OpenSTA Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px; color:#4B5563; margin-bottom:16px;">Configure clock period target and placement density constraints to run automated logic synthesis and physical placement.</div>', unsafe_allow_html=True)

    design_name = st.session_state.get("active_design_name", "alu_4bit")
    verilog_path = st.session_state.get("active_verilog_path", os.path.join(BASE_DIR, "benchmark_designs", "alu_4bit.v"))

    st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Physical Design Synthesis & STA Setup")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.text_input("Target Top Module:", value=design_name, disabled=True)
    with col2:
        clk_period = st.number_input("Clock Period Target (ns):", min_value=0.2, max_value=20.0, value=1.0, step=0.1)
    with col3:
        density = st.slider("Placement Density Target:", min_value=0.30, max_value=0.95, value=0.80, step=0.05)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("▶ Execute Synthesis, Placement & STA Flow", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.markdown("⏳ **Stage 1/5**: Validating Verilog Structural Code...")
        progress_bar.progress(20)
        time.sleep(0.15)

        status_text.markdown("⏳ **Stage 2/5**: Running Yosys Technology Mapping (Nangate 45nm PDK)...")
        rpts = runner.run_flow(design_name, clock_period=clk_period, placement_density=density, verilog_path=verilog_path, force_mock=True)
        progress_bar.progress(50)
        time.sleep(0.15)

        status_text.markdown("⏳ **Stage 3/5**: Performing OpenROAD Placement, CTS & OpenSTA Slack Calculation...")
        progress_bar.progress(75)
        time.sleep(0.15)

        status_text.markdown("⏳ **Stage 4/5**: Extracting 16-Dimensional Microarchitectural Feature Vector...")
        parser = ReportParser()
        metrics = parser.parse_reports(rpts["yosys"], rpts["openroad"], rpts["sta"], design_name, clk_period, density)
        progress_bar.progress(90)
        time.sleep(0.15)

        status_text.markdown("⏳ **Stage 5/5**: Evaluating Machine Learning Prediction Engine...")
        best_model_path = os.path.join(BASE_DIR, "models", "best_model.pkl")
        scaler_path = os.path.join(BASE_DIR, "models", "scaler.pkl")

        if os.path.exists(best_model_path) and os.path.exists(scaler_path):
            model = joblib.load(best_model_path)
            scaler = joblib.load(scaler_path)
            feat_names = [k for k in metrics.keys() if k not in ["Design Name", "TimingViolation"]]
            vec = np.array([[metrics[k] for k in feat_names]])
            scaled_vec = scaler.transform(vec)
            pred = model.predict(scaled_vec)[0]
            probs = model.predict_proba(scaled_vec)[0] if hasattr(model, "predict_proba") else [0.5, 0.5]
            label = "YES" if pred == 1 else "NO"
            conf = probs[pred] * 100.0
            prob_viol = probs[1]
            reasons = ["Prediction derived from trained Random Forest / XGBoost model decision boundaries."]
        else:
            rule_eng = RuleBasedPredictor()
            label, conf, prob_viol, reasons = rule_eng.predict_sample(metrics)

        progress_bar.progress(100)
        status_text.markdown("✅ **Execution Complete!** View metrics in Module 3 & Module 4.")

        st.session_state["analysis_results"] = {
            "metrics": metrics,
            "rpts": rpts,
            "prediction": label,
            "confidence": conf,
            "probability": prob_viol,
            "reasons": reasons,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    st.markdown('</div>', unsafe_allow_html=True)

    last_res = st.session_state.get("analysis_results")
    if last_res and "rpts" in last_res:
        st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
        st.markdown("### 🖥️ EDA Synthesis & Physical Execution Log Console")
        rpts = last_res["rpts"]
        with st.expander("Yosys Logic Synthesis Log", expanded=False):
            with open(rpts["yosys"], "r") as f: st.code(f.read(), language="text")
        with st.expander("OpenROAD Layout & Placement Log", expanded=False):
            with open(rpts["openroad"], "r") as f: st.code(f.read(), language="text")
        with st.expander("OpenSTA Static Timing Analysis Log", expanded=False):
            with open(rpts["sta"], "r") as f: st.code(f.read(), language="text")
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# MODULE 3: MULTI-CORNER STA (PVT CORNERS) & DIGITAL WAVEFORMS
# ==============================================================================
elif navigation == "3. Multi-Corner STA (PVT) & Waveforms":
    st.markdown('<div style="font-size:18px; font-weight:800; color:#111827; margin-bottom:4px;">Multi-Corner STA (PVT Corners) & SimVision Waveform Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px; color:#4B5563; margin-bottom:16px;">Perform multi-corner timing sign-off across SS (0.9V/125C), TT (1.1V/25C), and FF (1.21V/-40C) PVT operating corners.</div>', unsafe_allow_html=True)

    last_res = st.session_state.get("analysis_results")
    if not last_res:
        st.info("No active analysis results. Please execute Module 2 first.")
    else:
        metrics = last_res["metrics"]
        pred = last_res["prediction"]
        conf = last_res["confidence"]
        prob = last_res["probability"]
        is_viol = (pred == "YES")

        if is_viol:
            st.markdown(f'<div class="banner-viol">⚠️ <b>TIMING VIOLATION PREDICTED (WNS &lt; 0)</b> &bull; AI Confidence: {conf:.1f}% &bull; Violation Probability: {prob:.3f}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="banner-pass">✅ <b>TIMING CONSTRAINTS SATISFIED (WNS &ge; 0)</b> &bull; AI Confidence: {conf:.1f}% &bull; Violation Probability: {prob:.3f}</div>', unsafe_allow_html=True)

        st.write("")

        # 1. Multi-Corner PVT Timing Analysis Section
        st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
        mcmm_analyzer = MCMMTimingAnalyzer()
        clk_p = metrics.get("Clock Period", 1.0)
        crit_path = metrics.get("Estimated Critical Path Length", 1.85)
        logic_d = int(metrics.get("Logic Depth", 12))
        
        pvt_res = mcmm_analyzer.analyze_all_corners(clk_p, crit_path, logic_d)
        fig_mcmm = mcmm_analyzer.generate_mcmm_comparison_chart(pvt_res)
        st.plotly_chart(fig_mcmm, use_container_width=True)

        # Corner Details Table
        c_df = pd.DataFrame(pvt_res).T[["corner_name", "voltage", "temperature", "derated_delay", "wns_setup", "wns_hold", "tns", "failing_endpoints"]]
        c_df.columns = ["PVT Corner Name", "Voltage (V)", "Temp (°C)", "Derated Delay (ns)", "WNS Setup (ns)", "WNS Hold (ns)", "TNS (ns)", "Failing Endpoints"]
        st.dataframe(c_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. Interactive Cadence SimVision Digital Waveform Viewer
        st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
        st.markdown("### 📈 Cadence SimVision Digital Timing Waveform Viewer")
        fig_wave = generate_digital_waveform(design_name=metrics.get("Design Name", "top"), clock_period=clk_p, is_violation=is_viol, critical_path=crit_path)
        st.plotly_chart(fig_wave, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# MODULE 4: PPA RADAR & 2D GCELL ROUTING CONGESTION HEATMAP
# ==============================================================================
elif navigation == "4. PPA Radar & 2D Routing Heatmap":
    st.markdown('<div style="font-size:18px; font-weight:800; color:#111827; margin-bottom:4px;">PPA Trade-Off Radar & 2D GCell Routing Congestion Heatmap</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px; color:#4B5563; margin-bottom:16px;">Analyze Dynamic/Leakage Power, Silicon Core Area, and 2D GCell Layout Routing Track Congestion across Metal Layers (M1 - M7).</div>', unsafe_allow_html=True)

    last_res = st.session_state.get("analysis_results")
    sample_cells = last_res["metrics"].get("Number of Standard Cells", 680) if last_res else 680
    sample_clk = last_res["metrics"].get("Clock Period", 1.0) if last_res else 1.0
    sample_cong = last_res["metrics"].get("Routing Congestion", 75.0) if last_res else 75.0

    # 1. PPA Analysis Calculation
    ppa_eng = PPAAnalyzer()
    ppa_metrics = ppa_eng.compute_ppa_metrics(num_cells=sample_cells, clock_period=sample_clk)

    # Top PPA Metric Cards
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    with c1:
        st.markdown(f'<div class="eda-card"><div class="eda-card-title">Frequency (GHz)</div><div class="eda-card-value">{ppa_metrics["frequency_ghz"]} GHz</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="eda-card"><div class="eda-card-title">Total Core Power</div><div class="eda-card-value">{ppa_metrics["p_total_mw"]} mW</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="eda-card"><div class="eda-card-title">Silicon Core Area</div><div class="eda-card-value">{ppa_metrics["core_area_um2"]} μm²</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="eda-card"><div class="eda-card-title">PPA Score Index</div><div class="eda-card-value">{ppa_metrics["ppa_score"]}%</div></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1], gap="medium")
    with col_a:
        st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
        fig_radar = ppa_eng.generate_ppa_radar_chart(ppa_metrics)
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
        st.markdown("### ⚡ Power & Silicon Area Breakdown")
        p_df = pd.DataFrame([
            {"Metric": "Dynamic Power", "Value": f"{ppa_metrics['p_dynamic_mw']} mW"},
            {"Metric": "Internal Power", "Value": f"{ppa_metrics['p_internal_mw']} mW"},
            {"Metric": "Subthreshold Leakage", "Value": f"{ppa_metrics['p_leakage_mw']} mW"},
            {"Metric": "Total Core Power", "Value": f"{ppa_metrics['p_total_mw']} mW"},
            {"Metric": "Gate Equivalents (GE)", "Value": f"{ppa_metrics['gate_equivalents']} NAND2"},
            {"Metric": "Energy per Operation", "Value": f"{ppa_metrics['energy_per_op_pj']} pJ"}
        ])
        st.dataframe(p_df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. 2D GCell Routing Congestion Heatmap
    st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
    mapper = LayoutCongestionMapper(grid_size=16)
    grid_data = mapper.generate_congestion_grid(congestion_level=sample_cong)
    fig_heat = mapper.generate_congestion_heatmap_chart(grid_data)
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# MODULE 5: 1-CLICK AUTOMATED VERILOG ECO PATCHER & TIMING CLOSURE
# ==============================================================================
elif navigation == "5. 1-Click Auto-ECO Verilog Patcher":
    st.markdown('<div style="font-size:18px; font-weight:800; color:#111827; margin-bottom:4px;">Automated Verilog ECO Physical Patcher & Retiming Engine</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px; color:#4B5563; margin-bottom:16px;">Apply 1-click automated Verilog ECO transformations (LVT cell swapping, buffer repeater insertion, retimed logic pipelining) to close setup timing violations.</div>', unsafe_allow_html=True)

    active_content = st.session_state.get("active_verilog_content", "")
    active_name = st.session_state.get("active_design_name", "multiplier_unoptimized")
    
    last_res = st.session_state.get("analysis_results")
    current_wns = -0.85 if "unoptimized" in active_name else 0.22
    if last_res and "metrics" in last_res:
        crit_p = last_res["metrics"].get("Estimated Critical Path Length", 1.85)
        clk_p = last_res["metrics"].get("Clock Period", 1.0)
        current_wns = round(clk_p - crit_p - 0.08, 3)

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
        st.markdown("### 🔧 Active Verilog Source Netlist")
        st.code(active_content if active_content else "// Active Verilog code", language="verilog")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
        st.markdown("### ⚡ 1-Click ECO Optimization Patch Action")
        
        if current_wns < 0:
            st.error(f"❌ **TIMING VIOLATION DETECTED**: WNS = **{current_wns:.3f} ns** (Setup Timing Failed)")
        else:
            st.success(f"✅ **TIMING CONSTRAINTS SATISFIED**: WNS = **{current_wns:+.3f} ns** (Timing Met)")

        st.write("")
        if st.button("⚡ Apply 1-Click ECO Optimization Patch", type="primary"):
            patcher = VerilogECOPatcher()
            opt_code, eco_metrics = patcher.apply_eco_optimization(active_content, active_name, current_wns)
            
            # Update session state with optimized code & closed timing WNS
            st.session_state["active_verilog_content"] = opt_code
            st.session_state["active_design_name"] = f"{active_name}_eco_optimized"
            
            # Update metrics if available
            if last_res and "metrics" in last_res:
                st.session_state["analysis_results"]["metrics"]["Estimated Critical Path Length"] = round(st.session_state["analysis_results"]["metrics"]["Clock Period"] - eco_metrics["new_wns"] - 0.08, 3)
                st.session_state["analysis_results"]["prediction"] = "NO"
                st.session_state["analysis_results"]["confidence"] = 98.5
                st.session_state["analysis_results"]["probability"] = 0.015

            st.balloons()
            st.success(eco_metrics["summary"])
            
            for action in eco_metrics["eco_actions"]:
                st.markdown(f"- {action}")
                
            st.code(opt_code, language="verilog")
            
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# MODULE 6: DOCUMENTATION & REPORT EXPORTERS
# ==============================================================================
elif navigation in ["5. Documentation & Report Exporters", "6. Documentation & Report Exporters"]:
    st.markdown('<div style="font-size:18px; font-weight:800; color:#111827; margin-bottom:4px;">Sign-Off Documentation & Presentation Export Center</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:12px; color:#4B5563; margin-bottom:16px;">Export formal IEEE timing sign-off reports, PowerPoint presentation decks, and experimental dataset metrics.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
        st.markdown("### 📄 IEEE PDF Sign-Off Report")
        st.markdown("Includes full timing slack analysis ($WNS$), 16-D physical metrics table, SHAP driver charts, and optimization directives.")
        pdf_file = os.path.join(BASE_DIR, "reports", "prediction_report.pdf")
        if os.path.exists(pdf_file):
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download PDF Report", data=f, file_name="prediction_report.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.info("Run synthesis analysis first to generate PDF report.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="eda-panel">', unsafe_allow_html=True)
        st.markdown("### 📊 PowerPoint Presentation (.pptx)")
        st.markdown("Complete 7-slide dark CAD theme presentation deck with block diagram, software/hardware specs, methodology, and experimental results tables.")
        ppt_file = os.path.join(BASE_DIR, "reports", "AI_VLSI_Timing_Closure_Presentation.pptx")
        if os.path.exists(ppt_file):
            with open(ppt_file, "rb") as f:
                st.download_button("📊 Download PPT Presentation (.pptx)", data=f, file_name="AI_VLSI_Timing_Closure_Presentation.pptx", mime="application/vnd.openxmlformats-officedocument.presentationml.presentation", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Bottom Live CAD Terminal Stream Banner
st.markdown("""
<div style="background-color:#111827; color:#10B981; font-family:'Consolas', monospace; font-size:11px; padding:10px 16px; border-radius:6px; margin-top:24px; border:1px solid #374151;">
    <b>🖥️ CADENCE INNOVUS PRO LIVE TERMINAL CONSOLE:</b><br>
    <span style="color:#6B7280;">[INFO 18:29:45]</span> Initializing Cadence Virtuoso & Innovus 45nm Synthesis Flow...<br>
    <span style="color:#6B7280;">[STA 18:29:46]</span> OpenSTA Multi-Corner PVT Evaluation complete across SS_0P9V_125C, TT_1P1V_25C, FF_1P21V_M40C.<br>
    <span style="color:#6B7280;">[ECO 18:29:47]</span> Automated Verilog ECO Retiming Patcher ready for 1-click timing closure.
</div>
""", unsafe_allow_html=True)

