# OpenSTA Static Timing Analysis Script
create_clock -name clk -period $::env(CLOCK_PERIOD) [get_ports clk]
set_input_delay -clock clk 0.2 [all_inputs]
set_output_delay -clock clk 0.2 [all_outputs]
report_checks -path_delay max -format full_clock_expanded -digits 4
report_worst_slack -max
report_tns
