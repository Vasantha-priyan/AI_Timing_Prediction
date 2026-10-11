`timescale 1ns / 1ps

module baugh_wooley_4bit (
    input  wire signed [3:0] A,
    input  wire signed [3:0] B,
    output wire signed [7:0] P
);

    wire [7:0] pp0;
    wire [7:0] pp1;
    wire [7:0] pp2;
    wire [7:0] pp3;

    // Partial-product row 0
    assign pp0 = {
        4'b0000,
        ~(A[0] & B[3]),
        (A[0] & B[2]),
        (A[0] & B[1]),
        (A[0] & B[0])
    };

    // Partial-product row 1
    assign pp1 = {
        3'b000,
        ~(A[1] & B[3]),
        (A[1] & B[2]),
        (A[1] & B[1]),
        (A[1] & B[0]),
        1'b0
    };

    // Partial-product row 2
    assign pp2 = {
        2'b00,
        ~(A[2] & B[3]),
        (A[2] & B[2]),
        (A[2] & B[1]),
        (A[2] & B[0]),
        2'b00
    };

    // Partial-product row 3
    assign pp3 = {
        (A[3] & B[3]),
        ~(A[3] & B[2]),
        ~(A[3] & B[1]),
        ~(A[3] & B[0]),
        3'b000
    };

    // Baugh-Wooley correction
    assign P = pp0 + pp1 + pp2 + pp3 + 8'b10010000;

endmodule
verilog code.