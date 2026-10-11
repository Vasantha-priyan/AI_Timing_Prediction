// 4x4-bit Combinational Array Multiplier Benchmark
module multiplier_4x4 (
    input wire [3:0] A,
    input wire [3:0] B,
    output wire [7:0] P
);
    assign P = A * B;
endmodule
