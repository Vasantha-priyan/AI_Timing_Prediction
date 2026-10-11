// 8-bit Synchronous Up/Down Counter Benchmark
module counter_8bit (
    input wire clk,
    input wire rst,
    input wire enable,
    input wire up_down, // 1: Up, 0: Down
    input wire [7:0] load_data,
    input wire load_en,
    output reg [7:0] count,
    output wire overflow
);
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            count <= 8'h00;
        end else if (load_en) begin
            count <= load_data;
        end else if (enable) begin
            if (up_down)
                count <= count + 1'b1;
            else
                count <= count - 1'b1;
        end
    end

    assign overflow = (count == 8'hFF && enable && up_down);
endmodule
