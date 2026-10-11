// Sample User-Uploaded Custom Verilog Module
module sample_custom_design (
    input wire clk,
    input wire rst,
    input wire [7:0] in_a,
    input wire [7:0] in_b,
    output reg [15:0] out_product,
    output reg overflow
);
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            out_product <= 16'd0;
            overflow <= 1'b0;
        end else begin
            out_product <= in_a * in_b;
            overflow <= (in_a * in_b > 16'hFF00);
        end
    end
endmodule
