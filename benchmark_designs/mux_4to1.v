// 4:1 Multiplexer Benchmark Module
module mux_4to1 (
    input wire [3:0] in,
    input wire [1:0] sel,
    output reg y
);
    always @(*) begin
        case (sel)
            2'b00: y = in[0];
            2'b01: y = in[1];
            2'b10: y = in[2];
            2'b11: y = in[3];
            default: y = 1'b0;
        endcase
    end
endmodule
