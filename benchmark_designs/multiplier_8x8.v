// 8x8 Pipelined Array Multiplier Benchmark
module multiplier_8x8 (
    input wire clk,
    input wire rst,
    input wire [7:0] A,
    input wire [7:0] B,
    output reg [15:0] P
);
    reg [7:0] a_reg;
    reg [7:0] b_reg;
    reg [15:0] mult_stage1;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            a_reg <= 8'd0;
            b_reg <= 8'd0;
            mult_stage1 <= 16'd0;
            P <= 16'd0;
        end else begin
            a_reg <= A;
            b_reg <= B;
            mult_stage1 <= a_reg * b_reg;
            P <= mult_stage1;
        end
    end
endmodule
