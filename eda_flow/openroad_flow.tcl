# OpenROAD Physical Design Flow Script
initialize_floorplan -die_area "0 0 100 100" -core_area "10 10 90 90" -site "unithd"
place_pins -hor_layers "met2" -ver_layers "met3"
global_placement -density $::env(PLACEMENT_DENSITY)
detailed_placement
clock_tree_synthesis -wire_unit 20
global_route
detail_route
report_checks -path_delay max -fields {slew cap input fanout}
report_design_area
report_routing_congestion
