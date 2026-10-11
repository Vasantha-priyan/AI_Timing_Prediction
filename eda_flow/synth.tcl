# Yosys Logic Synthesis TCL Script
read_verilog $::env(VERILOG_FILE)
hierarchy -top $::env(TOP_MODULE)
proc; opt; fsm; opt; techmap; opt;
flatten
abc -g AND,OR,XOR,MUX
clean
write_verilog -noattr eda_flow/reports/netlist_$::env(TOP_MODULE).v
stat -top $::env(TOP_MODULE)
