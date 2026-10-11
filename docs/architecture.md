# Framework Architecture & System Specifications

## Overview
The **Explainable AI-Assisted Early Timing Violation Prediction and Optimization Framework** integrates open-source EDA tools (Yosys, OpenROAD, OpenSTA) with Machine Learning (Random Forest, Decision Tree, XGBoost) and SHAP Explainable AI.

```
   +-----------------------+
   | Uploaded / Benchmark  | Verilog RTL Files (.v / .sv)
   +-----------+-----------+
               |
               v
   +-----------------------+
   | Syntax Validator      | Structural, Keyword, and Bracket Checking
   +-----------+-----------+
               |
               v
   +-----------------------+
   | Yosys Synthesis       | Logic Mapping & Gate Netlist Generation
   +-----------+-----------+
               |
               v
   +-----------------------+
   | OpenROAD Layout       | Floorplanning, Placement, CTS, Detailed Routing
   +-----------+-----------+
               |
               v
   +-----------------------+
   | OpenSTA Timing Anal.  | Static Timing Analysis & WNS Slack Calculation
   +-----------+-----------+
               |
               v
   +-----------------------+
   | Feature Extractor     | Extract 16 Physical & Microarchitectural Metrics
   +-----------+-----------+
               |
               v
   +-----------------------+
   | Machine Learning      | Random Forest / Decision Tree / XGBoost
   +-----------+-----------+
               |
               v
   +-----------------------+
   | SHAP Explainable AI   | Feature Driver Ranking & SHAP Waterfalls
   +-----------+-----------+
               |
               v
   +-----------------------+
   | Optimization Engine   | Cell Upsizing, Pipelining, Buffer Insertion Directives
   +-----------+-----------+
               |
               v
   +-----------------------+
   | Dashboard & Reports   | Streamlit Web App & ReportLab PDF Exporter
   +-----------------------+
```

## Microarchitectural & Physical Features (16)
1. Design Name
2. Clock Period (ns)
3. Clock Frequency (MHz)
4. Number of Standard Cells
5. Number of Flip-Flops
6. Number of Nets
7. Total Cell Area ($\mu m^2$)
8. Cell Utilization (%)
9. Maximum Fanout
10. Logic Depth (Gates)
11. Placement Density Target
12. Routing Congestion (%)
13. Estimated Wire Length ($\mu m$)
14. Buffer Count
15. Inverter Count
16. Estimated Critical Path Length (ns)

Target Label: `TimingViolation` (YES/NO based on OpenSTA Worst Negative Slack $WNS < 0$).
*Note: WNS is strictly excluded from input feature training vectors.*
