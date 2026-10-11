// 4-bit Arithmetic Logic Unit (ALU) Benchmark
module alu_4bit (
    input wire [3:0] A,
    input wire [3:0] B,
    input wire [2:0] ALU_Sel,
    input wire clk,
    input wire rst,
    output reg [3:0] ALU_Out,
    output reg CarryOut,
    output reg Zero
);
    reg [4:0] result;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            ALU_Out  <= 4'b0000;
            CarryOut <= 1'b0;
            Zero     <= 1'b1;
        end else begin
            case (ALU_Sel)
                3'b000: result = A + B;                   // Addition
                3'b001: result = A - B;                   // Subtraction
                3'b010: result = {1'b0, A & B};           // AND
                3'b011: result = {1'b0, A | B};           // OR
                3'b100: result = {1'b0, A ^ B};           // XOR
                3'b101: result = {1'b0, ~(A | B)};        // NOR
                3'b110: result = {1'b0, (A < B) ? 4'b0001 : 4'b0000}; // SLT
                3'b111: result = {1'b0, A << 1};          // Shift Left
                default: result = 5'b00000;
            endcase
            ALU_Out  <= result[3:0];
            CarryOut <= result[4];
            Zero     <= (result[3:0] == 4'b0000);
        end
    end
endmodule
