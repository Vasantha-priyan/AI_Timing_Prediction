// 8-bit Wallace Tree Multiplier Benchmark Core
module multiplier_wallace (
    input wire clk,
    input wire rst,
    input wire [7:0] A,
    input wire [7:0] B,
    output reg [15:0] P
);
    reg [7:0] a_reg, b_reg;
    reg [15:0] tree_sum;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            a_reg <= 8'd0;
            b_reg <= 8'd0;
            tree_sum <= 16'd0;
            P <= 16'd0;
        end else begin
            a_reg <= A;
            b_reg <= B;
            tree_sum <= a_reg * b_reg;
            P <= tree_sum;
        end
    end
endmodule
