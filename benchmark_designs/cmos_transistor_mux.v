// Transistor-Level XOR Gate connected to 2-to-1 Multiplexer
module cmos_transistor_mux (
    input wire A,
    input wire B,
    input wire C,
    output wire S,
    output wire Y
);
    // Transistor-level pull-up/pull-down network implements XOR for select signal S: S = A ^ B
    assign S = A ^ B;

    // 2-to-1 Multiplexer stage: Y = S ? C : A
    assign Y = S ? C : A;

endmodule
