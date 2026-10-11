"""
Unit Tests for Verilog Syntax Validation Module
"""

import os
import sys
import pytest

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from syntax_validator.syntax_checker import VerilogSyntaxChecker

def test_valid_verilog():
    checker = VerilogSyntaxChecker()
    valid_code = "module mux21 (input a, input b, input sel, output y); assign y = sel ? b : a; endmodule"
    res = checker.validate_code(valid_code)
    assert res["valid"] is True
    assert res["top_module"] == "mux21"
    assert len(res["errors"]) == 0

def test_invalid_verilog():
    checker = VerilogSyntaxChecker()
    invalid_code = "module bad_mux (input a, input b; assign y = a;"
    res = checker.validate_code(invalid_code)
    assert res["valid"] is False
    assert len(res["errors"]) > 0
