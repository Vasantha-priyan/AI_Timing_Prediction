// 4-Tap FIR Filter Benchmark Core
module fir_filter (
    input wire clk,
    input wire rst,
    input wire signed [7:0] sample_in,
    output reg signed [15:0] filter_out
);
    localparam signed [7:0] C0 = 8'sd5;
    localparam signed [7:0] C1 = 8'sd12;
    localparam signed [7:0] C2 = 8'sd12;
    localparam signed [7:0] C3 = 8'sd5;

    reg signed [7:0] x0, x1, x2, x3;
    reg signed [15:0] p0, p1, p2, p3;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            x0 <= 8'sd0; x1 <= 8'sd0; x2 <= 8'sd0; x3 <= 8'sd0;
            p0 <= 16'sd0; p1 <= 16'sd0; p2 <= 16'sd0; p3 <= 16'sd0;
            filter_out <= 16'sd0;
        end else begin
            x0 <= sample_in;
            x1 <= x0;
            x2 <= x1;
            x3 <= x2;

            p0 <= x0 * C0;
            p1 <= x1 * C1;
            p2 <= x2 * C2;
            p3 <= x3 * C3;

            filter_out <= p0 + p1 + p2 + p3;
        end
    end
endmodule
