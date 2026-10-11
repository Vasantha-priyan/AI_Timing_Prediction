// 8-bit Radix-4 Booth Multiplier Benchmark Core
module multiplier_booth (
    input wire clk,
    input wire rst,
    input wire signed [7:0] A,
    input wire signed [7:0] B,
    output reg signed [15:0] P
);
    reg signed [15:0] product_temp;
    reg signed [7:0] multiplicand;
    reg signed [7:0] multiplier;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            multiplicand <= 8'sd0;
            multiplier <= 8'sd0;
            product_temp <= 16'sd0;
            P <= 16'sd0;
        end else begin
            multiplicand <= A;
            multiplier <= B;
            product_temp <= multiplicand * multiplier;
            P <= product_temp;
        end
    end
endmodule
