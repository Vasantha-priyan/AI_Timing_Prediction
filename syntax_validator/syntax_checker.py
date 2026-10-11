"""
Verilog Syntax Validation Module
Performs structural, keyword, and bracket matching syntax validation on input Verilog RTL files.
"""

import re
import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger("SyntaxChecker")

class VerilogSyntaxChecker:
    def __init__(self):
        self.keywords = {
            "module", "endmodule", "input", "output", "inout", "wire", "reg",
            "always", "initial", "assign", "case", "endcase", "if", "else",
            "begin", "end", "parameter", "localparam", "function", "endfunction"
        }

    def validate_code(self, code_content: str) -> Dict[str, Any]:
        """
        Validates Verilog code string and returns validation status and list of issues.
        """
        errors: List[str] = []
        warnings: List[str] = []

        lines = code_content.splitlines()

        # 1. Module & Endmodule Count Match
        module_matches = re.findall(r"\bmodule\s+(\w+)", code_content)
        endmodule_matches = re.findall(r"\bendmodule\b", code_content)

        if not module_matches:
            errors.append("Syntax Error: No 'module' declaration found in Verilog code.")
        if len(module_matches) != len(endmodule_matches):
            errors.append(f"Syntax Error: Mismatch between 'module' ({len(module_matches)}) and 'endmodule' ({len(endmodule_matches)}) declarations.")

        # 2. Balanced Parentheses, Brackets, and Braces
        paren_balance = 0
        bracket_balance = 0
        brace_balance = 0

        for line_num, line in enumerate(lines, 1):
            # Strip comments
            clean_line = re.sub(r"//.*$", "", line)
            
            for char in clean_line:
                if char == '(': paren_balance += 1
                elif char == ')': paren_balance -= 1
                elif char == '[': bracket_balance += 1
                elif char == ']': bracket_balance -= 1
                elif char == '{': brace_balance += 1
                elif char == '}': brace_balance -= 1

            if paren_balance < 0:
                errors.append(f"Line {line_num}: Unmatched closing parenthesis ')'")
                paren_balance = 0
            if bracket_balance < 0:
                errors.append(f"Line {line_num}: Unmatched closing bracket ']'")
                bracket_balance = 0
            if brace_balance < 0:
                errors.append(f"Line {line_num}: Unmatched closing brace '}}'")
                brace_balance = 0

        if paren_balance != 0:
            errors.append(f"Syntax Error: Unclosed parenthesis '(' in code.")
        if bracket_balance != 0:
            errors.append(f"Syntax Error: Unclosed bracket '[' in code.")
        if brace_balance != 0:
            errors.append(f"Syntax Error: Unclosed brace '{{' in code.")

        # 3. Check Begin/End Block Balancing
        begin_count = len(re.findall(r"\bbegin\b", code_content))
        end_count = len(re.findall(r"\bend\b", code_content)) - len(re.findall(r"\bendmodule\b|\bendcase\b|\bendfunction\b", code_content))
        if begin_count != end_count and end_count >= 0:
            warnings.append(f"Notice: 'begin' count ({begin_count}) does not match 'end' count ({end_count}). Check block nesting.")

        top_module = module_matches[0] if module_matches else "unknown"

        is_valid = (len(errors) == 0)
        return {
            "valid": is_valid,
            "top_module": top_module,
            "module_count": len(module_matches),
            "errors": errors,
            "warnings": warnings,
            "total_lines": len(lines)
        }

if __name__ == "__main__":
    checker = VerilogSyntaxChecker()
    sample_v = "module mux (input a, input b, input sel, output y); assign y = sel ? b : a; endmodule"
    res = checker.validate_code(sample_v)
    print("Syntax Check Result:", res)
