// 16x16-bit Pipelined Multiplier Benchmark
module multiplier_16x16 (
    input wire clk,
    input wire rst,
    input wire [15:0] A,
    input wire [15:0] B,
    output reg [31:0] P
);
    reg [15:0] a_reg;
    reg [15:0] b_reg;
    reg [31:0] mult_stage1;
    reg [31:0] mult_stage2;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            a_reg <= 16'd0;
            b_reg <= 16'd0;
            mult_stage1 <= 32'd0;
            mult_stage2 <= 32'd0;
            P <= 32'd0;
        end else begin
            a_reg <= A;
            b_reg <= B;
            mult_stage1 <= a_reg * b_reg;
            mult_stage2 <= mult_stage1;
            P <= mult_stage2;
        end
    end
endmodule
