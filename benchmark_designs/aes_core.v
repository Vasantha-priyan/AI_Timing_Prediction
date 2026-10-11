// AES SubBytes & MixColumns Core Benchmark
module aes_core (
    input wire clk,
    input wire rst,
    input wire [31:0] state_in,
    input wire [31:0] key_in,
    output reg [31:0] state_out
);
    reg [31:0] key_reg;
    reg [31:0] temp_state;

    function [7:0] sbox;
        input [7:0] in_byte;
        begin
            sbox = in_byte ^ 8'h63 ^ ((in_byte << 1) | (in_byte >> 7));
        end
    endfunction

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            key_reg <= 32'h0;
            temp_state <= 32'h0;
            state_out <= 32'h0;
        end else begin
            key_reg <= key_in;
            temp_state[7:0]   <= sbox(state_in[7:0])   ^ key_reg[7:0];
            temp_state[15:8]  <= sbox(state_in[15:8])  ^ key_reg[15:8];
            temp_state[23:16] <= sbox(state_in[23:16]) ^ key_reg[23:16];
            temp_state[31:24] <= sbox(state_in[31:24]) ^ key_reg[31:24];

            state_out[7:0]   <= temp_state[7:0]   ^ temp_state[15:8];
            state_out[15:8]  <= temp_state[15:8]  ^ temp_state[23:16];
            state_out[23:16] <= temp_state[23:16] ^ temp_state[31:24];
            state_out[31:24] <= temp_state[31:24] ^ temp_state[7:0];
        end
    end
endmodule
