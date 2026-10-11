"""
EDA Flow Runner Module
Orchestrates Yosys, OpenROAD, and OpenSTA tool runs.
Supports both native binary execution (Linux/WSL) and realistic prototype simulation mode (Cross-platform).
"""

import os
import sys
import shutil
import subprocess
import logging
import random
from typing import Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("EDA_Runner")

BENCHMARK_PROFILES = {
    "mux_2to1": {"base_cells": 4, "ffs": 0, "base_depth": 1, "base_area": 12.0},
    "mux_4to1": {"base_cells": 12, "ffs": 0, "base_depth": 2, "base_area": 32.0},
    "cmos_transistor_mux": {"base_cells": 16, "ffs": 0, "base_depth": 3, "base_area": 45.0},
    "alu_4bit": {"base_cells": 45, "ffs": 9, "base_depth": 5, "base_area": 120.5},
    "counter_8bit": {"base_cells": 62, "ffs": 8, "base_depth": 4, "base_area": 145.2},
    "uart": {"base_cells": 280, "ffs": 42, "base_depth": 8, "base_area": 580.0},
    "spi_controller": {"base_cells": 190, "ffs": 31, "base_depth": 7, "base_area": 410.0},
    "fifo": {"base_cells": 450, "ffs": 128, "base_depth": 9, "base_area": 1150.0},
    "fir_filter": {"base_cells": 850, "ffs": 140, "base_depth": 14, "base_area": 2100.0},
    "multiplier_unoptimized": {"base_cells": 680, "ffs": 0, "base_depth": 18, "base_area": 1750.0},
    "multiplier_optimized": {"base_cells": 740, "ffs": 48, "base_depth": 7, "base_area": 1900.0},
    "multiplier_4x4": {"base_cells": 120, "ffs": 0, "base_depth": 8, "base_area": 320.0},
    "multiplier_8x8": {"base_cells": 620, "ffs": 48, "base_depth": 16, "base_area": 1650.0},
    "multiplier_16x16": {"base_cells": 2400, "ffs": 96, "base_depth": 24, "base_area": 5800.0},
    "multiplier_booth": {"base_cells": 780, "ffs": 48, "base_depth": 18, "base_area": 1950.0},
    "multiplier_wallace": {"base_cells": 710, "ffs": 48, "base_depth": 15, "base_area": 1820.0},
    "multiplier": {"base_cells": 620, "ffs": 48, "base_depth": 16, "base_area": 1650.0},
    "aes_core": {"base_cells": 1850, "ffs": 128, "base_depth": 22, "base_area": 4500.0},
    "picorv32": {"base_cells": 3400, "ffs": 512, "base_depth": 28, "base_area": 8900.0},
}

class EDARunner:
    def __init__(self, base_dir: str = "."):
        self.base_dir = os.path.abspath(base_dir)
        self.reports_dir = os.path.join(self.base_dir, "eda_flow", "reports")
        os.makedirs(self.reports_dir, exist_ok=True)
        
        self.has_yosys = shutil.which("yosys") is not None
        self.has_openroad = shutil.which("openroad") is not None
        self.has_opensta = shutil.which("sta") is not None
        self.is_prototype_mode = not (self.has_yosys and self.has_openroad and self.has_opensta)

    def run_flow(self, design_name: str, clock_period: float, placement_density: float = 0.65, verilog_path: str = None, force_mock: bool = False) -> Dict[str, str]:
        logger.info(f"Running EDA Flow for design={design_name}, T_clk={clock_period}ns, density={placement_density}")
        
        if not force_mock and not self.is_prototype_mode:
            return self._run_native_eda(design_name, clock_period, placement_density, verilog_path)
        else:
            return self._generate_synthetic_reports(design_name, clock_period, placement_density, verilog_path)

    def _run_native_eda(self, design_name: str, clock_period: float, placement_density: float, verilog_path: str) -> Dict[str, str]:
        if verilog_path is None:
            verilog_path = os.path.join(self.base_dir, "benchmark_designs", f"{design_name}.v")

        yosys_rpt = os.path.join(self.reports_dir, f"{design_name}_yosys.log")
        openroad_rpt = os.path.join(self.reports_dir, f"{design_name}_openroad.log")
        sta_rpt = os.path.join(self.reports_dir, f"{design_name}_sta.log")

        env = os.environ.copy()
        env["VERILOG_FILE"] = verilog_path
        env["TOP_MODULE"] = design_name
        env["CLOCK_PERIOD"] = str(clock_period)
        env["PLACEMENT_DENSITY"] = str(placement_density)

        try:
            cmd_yosys = ["yosys", "-s", os.path.join(self.base_dir, "eda_flow", "synth.tcl")]
            with open(yosys_rpt, "w") as f:
                subprocess.run(cmd_yosys, env=env, stdout=f, stderr=subprocess.STDOUT, check=True)

            cmd_or = ["openroad", "-exit", os.path.join(self.base_dir, "eda_flow", "openroad_flow.tcl")]
            with open(openroad_rpt, "w") as f:
                subprocess.run(cmd_or, env=env, stdout=f, stderr=subprocess.STDOUT, check=True)

            cmd_sta = ["sta", "-exit", os.path.join(self.base_dir, "eda_flow", "sta.tcl")]
            with open(sta_rpt, "w") as f:
                subprocess.run(cmd_sta, env=env, stdout=f, stderr=subprocess.STDOUT, check=True)

            return {"yosys": yosys_rpt, "openroad": openroad_rpt, "sta": sta_rpt, "mode": "NATIVE"}
        except subprocess.CalledProcessError as e:
            logger.warning(f"Native EDA tool execution failed: {e}. Switching to Prototype Simulation Mode.")
            return self._generate_synthetic_reports(design_name, clock_period, placement_density, verilog_path)

    def _generate_synthetic_reports(self, design_name: str, clock_period: float, placement_density: float, verilog_path: str = None) -> Dict[str, str]:
        if design_name in BENCHMARK_PROFILES:
            prof = BENCHMARK_PROFILES[design_name]
        else:
            lines = 50
            if verilog_path and os.path.exists(verilog_path):
                with open(verilog_path, "r") as f: lines = len(f.readlines())
            prof = {"base_cells": lines * 5, "ffs": int(lines * 0.8), "base_depth": min(30, int(lines * 0.15)), "base_area": lines * 25.0}

        density_factor = placement_density / 0.65
        cell_count = int(prof["base_cells"] * (1.0 + 0.05 * (1.0 / clock_period)))
        ff_count = prof["ffs"]
        net_count = cell_count + random.randint(5, 20)
        total_area = prof["base_area"] * (cell_count / max(1, prof["base_cells"]))
        cell_utilization = min(0.95, placement_density * (1.0 + random.uniform(-0.03, 0.03)))
        max_fanout = random.randint(8, 18) + int(cell_count / 250)
        logic_depth = prof["base_depth"] + random.randint(0, 2)
        
        est_wire_length = cell_count * 12.5 * (1.0 + (cell_utilization ** 2))
        routing_congestion = min(100.0, cell_utilization * 100.0 + random.uniform(2.0, 12.0))
        
        buffer_count = int(cell_count * 0.12 * density_factor)
        inverter_count = int(cell_count * 0.18)
        
        gate_delay = logic_depth * 0.14
        wire_delay = (est_wire_length / 1000.0) * 0.08 * (1.0 + routing_congestion / 100.0)
        critical_path_estimate = gate_delay + wire_delay + random.uniform(0.05, 0.15)
        
        setup_time = 0.10
        wns = clock_period - (critical_path_estimate + setup_time)

        # 1. Yosys Report Content
        yosys_rpt = os.path.join(self.reports_dir, f"{design_name}_yosys.log")
        with open(yosys_rpt, "w") as f:
            f.write(f"=== Yosys Logic Synthesis Report for {design_name} [PROTOTYPE MODE] ===\n")
            f.write(f"Number of wires:                 {net_count}\n")
            f.write(f"Number of cells:                 {cell_count}\n")
            f.write(f"   $_DFF_P_                      {ff_count}\n")
            f.write(f"   $_BUF_                        {buffer_count}\n")
            f.write(f"   $_NOT_                        {inverter_count}\n")
            f.write(f"Chip area for module '{design_name}': {total_area:.4f}\n")
            f.write(f"Maximum fanout:                  {max_fanout}\n")
            f.write(f"Logic depth:                     {logic_depth}\n")

        # 2. OpenROAD Report Content
        openroad_rpt = os.path.join(self.reports_dir, f"{design_name}_openroad.log")
        with open(openroad_rpt, "w") as f:
            f.write(f"=== OpenROAD Physical Design Report [PROTOTYPE MODE] ===\n")
            f.write(f"Design Name: {design_name}\n")
            f.write(f"Placement Density Target: {placement_density:.4f}\n")
            f.write(f"Achieved Cell Utilization: {cell_utilization * 100:.2f}%\n")
            f.write(f"Estimated Total Wire Length: {est_wire_length:.2f} um\n")
            f.write(f"Routing Congestion: {routing_congestion:.2f}%\n")
            f.write(f"Buffer Count: {buffer_count}\n")
            f.write(f"Inverter Count: {inverter_count}\n")

        # 3. OpenSTA Report Content
        sta_rpt = os.path.join(self.reports_dir, f"{design_name}_sta.log")
        with open(sta_rpt, "w") as f:
            f.write(f"=== OpenSTA Timing Report [PROTOTYPE MODE] ===\n")
            f.write(f"Clock Period Constraint: {clock_period:.4f} ns\n")
            f.write(f"Clock Frequency: {1000.0 / clock_period:.2f} MHz\n")
            f.write(f"Critical Path Delay: {critical_path_estimate:.4f} ns\n")
            f.write(f"Worst Negative Slack (WNS): {wns:.4f} ns\n")
            if wns < 0:
                f.write("TIMING VIOLATION DETECTED: YES\n")
            else:
                f.write("TIMING VIOLATION DETECTED: NO\n")

        return {"yosys": yosys_rpt, "openroad": openroad_rpt, "sta": sta_rpt, "mode": "PROTOTYPE"}

if __name__ == "__main__":
    runner = EDARunner()
    res = runner.run_flow("multiplier_8x8", clock_period=2.0, placement_density=0.65, force_mock=True)
    print("EDA Run Completed:", res)
