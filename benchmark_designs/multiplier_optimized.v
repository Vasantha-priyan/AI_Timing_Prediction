// Optimized 8x8 Pipelined Multiplier (Best Case - Pipelined Register Stages & Reduced Delay)
module multiplier_optimized (
    input wire clk,
    input wire rst,
    input wire [7:0] A,
    input wire [7:0] B,
    output reg [15:0] P
);
    reg [7:0] a_reg, b_reg;
    reg [15:0] mult_stage1, mult_stage2;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            a_reg <= 8'd0;
            b_reg <= 8'd0;
            mult_stage1 <= 16'd0;
            mult_stage2 <= 16'd0;
            P <= 16'd0;
        end else begin
            a_reg <= A;
            b_reg <= B;
            mult_stage1 <= a_reg * b_reg;
            mult_stage2 <= mult_stage1;
            P <= mult_stage2;
        end
    end
endmodule
