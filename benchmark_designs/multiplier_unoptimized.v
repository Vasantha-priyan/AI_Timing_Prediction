// Unoptimized 8x8 Combinational Multiplier (Worst Case - High Logic Depth & Fanout)
module multiplier_unoptimized (
    input wire [7:0] A,
    input wire [7:0] B,
    output wire [15:0] P
);
    // Unpipelined 16-level combinational array multiplier
    assign P = A * B;
endmodule
