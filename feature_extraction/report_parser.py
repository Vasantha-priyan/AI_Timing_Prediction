"""
Feature Extraction Parser Module
Extracts microarchitectural, physical layout, and timing constraint metrics from Yosys, OpenROAD, and OpenSTA log files.
"""

import os
import re
import logging
from typing import Dict, Any

logger = logging.getLogger("ReportParser")

class ReportParser:
    def __init__(self):
        pass

    def parse_reports(self, yosys_path: str, openroad_path: str, sta_path: str, design_name: str, clock_period: float, placement_density: float) -> Dict[str, Any]:
        """
        Parses log files and returns a feature metrics dictionary.
        """
        yosys_data = self._parse_yosys(yosys_path)
        openroad_data = self._parse_openroad(openroad_path)
        sta_data = self._parse_sta(sta_path)

        wns = sta_data.get("wns", 0.0)
        timing_violation = "YES" if wns < 0.0 else "NO"
        clock_freq = 1000.0 / float(clock_period) if clock_period > 0 else 0.0

        extracted_record = {
            "Design Name": design_name,
            "Clock Period": float(clock_period),
            "Clock Frequency": float(clock_freq),
            "Number of Standard Cells": int(yosys_data.get("cells", 0)),
            "Number of Flip-Flops": int(yosys_data.get("ffs", 0)),
            "Number of Nets": int(yosys_data.get("nets", 0)),
            "Total Cell Area": float(yosys_data.get("area", 0.0)),
            "Cell Utilization": float(openroad_data.get("utilization", 0.0)),
            "Maximum Fanout": int(yosys_data.get("max_fanout", 0)),
            "Logic Depth": int(yosys_data.get("logic_depth", 0)),
            "Placement Density": float(placement_density),
            "Routing Congestion": float(openroad_data.get("congestion", 0.0)),
            "Estimated Wire Length": float(openroad_data.get("wire_length", 0.0)),
            "Buffer Count": int(openroad_data.get("buffer_count", 0)),
            "Inverter Count": int(openroad_data.get("inverter_count", 0)),
            "Estimated Critical Path Length": float(sta_data.get("critical_path", 0.0)),
            "TimingViolation": timing_violation
        }

        return extracted_record

    def _parse_yosys(self, file_path: str) -> Dict[str, Any]:
        data = {"cells": 0, "ffs": 0, "nets": 0, "area": 0.0, "max_fanout": 0, "logic_depth": 0}
        if not os.path.exists(file_path): return data
        with open(file_path, "r") as f: content = f.read()

        cells_match = re.search(r"Number of cells:\s+(\d+)", content)
        if cells_match: data["cells"] = int(cells_match.group(1))

        ffs_match = re.search(r"\$_DFF_P_\s+(\d+)", content)
        if ffs_match: data["ffs"] = int(ffs_match.group(1))

        nets_match = re.search(r"Number of wires:\s+(\d+)", content)
        if nets_match: data["nets"] = int(nets_match.group(1))

        area_match = re.search(r"Chip area for module '.*?':\s+([\d\.]+)", content)
        if area_match: data["area"] = float(area_match.group(1))

        fanout_match = re.search(r"Maximum fanout:\s+(\d+)", content)
        if fanout_match: data["max_fanout"] = int(fanout_match.group(1))

        depth_match = re.search(r"Logic depth:\s+(\d+)", content)
        if depth_match: data["logic_depth"] = int(depth_match.group(1))

        return data

    def _parse_openroad(self, file_path: str) -> Dict[str, Any]:
        data = {"utilization": 0.0, "wire_length": 0.0, "congestion": 0.0, "buffer_count": 0, "inverter_count": 0}
        if not os.path.exists(file_path): return data
        with open(file_path, "r") as f: content = f.read()

        util_match = re.search(r"Achieved Cell Utilization:\s+([\d\.]+)%", content)
        if util_match: data["utilization"] = float(util_match.group(1)) / 100.0

        wl_match = re.search(r"Estimated Total Wire Length:\s+([\d\.]+)", content)
        if wl_match: data["wire_length"] = float(wl_match.group(1))

        cong_match = re.search(r"Routing Congestion:\s+([\d\.]+)%", content)
        if cong_match: data["congestion"] = float(cong_match.group(1))

        buf_match = re.search(r"Buffer Count:\s+(\d+)", content)
        if buf_match: data["buffer_count"] = int(buf_match.group(1))

        inv_match = re.search(r"Inverter Count:\s+(\d+)", content)
        if inv_match: data["inverter_count"] = int(inv_match.group(1))

        return data

    def _parse_sta(self, file_path: str) -> Dict[str, Any]:
        data = {"critical_path": 0.0, "wns": 0.0}
        if not os.path.exists(file_path): return data
        with open(file_path, "r") as f: content = f.read()

        cp_match = re.search(r"Critical Path Delay:\s+([\d\.]+)", content)
        if cp_match: data["critical_path"] = float(cp_match.group(1))

        wns_match = re.search(r"Worst Negative Slack \(WNS\):\s+([-\d\.]+)", content)
        if wns_match: data["wns"] = float(wns_match.group(1))

        return data
