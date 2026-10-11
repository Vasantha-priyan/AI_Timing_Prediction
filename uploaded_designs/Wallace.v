`timescale 1ns/1ps
//=========================================================
// 4x4 Unsigned Wallace Tree Multiplier
//=========================================================

module wallace_tree_multiplier (
    input  [3:0] A,
    input  [3:0] B,
    output [7:0] P
);

wire pp00,pp01,pp02,pp03;
wire pp10,pp11,pp12,pp13;
wire pp20,pp21,pp22,pp23;
wire pp30,pp31,pp32,pp33;

// Partial Products
assign pp00 = A[0] & B[0];
assign pp01 = A[0] & B[1];
assign pp02 = A[0] & B[2];
assign pp03 = A[0] & B[3];

assign pp10 = A[1] & B[0];
assign pp11 = A[1] & B[1];
assign pp12 = A[1] & B[2];
assign pp13 = A[1] & B[3];

assign pp20 = A[2] & B[0];
assign pp21 = A[2] & B[1];
assign pp22 = A[2] & B[2];
assign pp23 = A[2] & B[3];

assign pp30 = A[3] & B[0];
assign pp31 = A[3] & B[1];
assign pp32 = A[3] & B[2];
assign pp33 = A[3] & B[3];

// Wallace Reduction
wire s1,c1,s2,c2,s3,c3;
wire s4,c4,s5,c5,s6,c6;
wire s7,c7,s8,c8;

// Product Bit 0
assign P[0] = pp00;

// Stage 1
half_adder HA1(pp01,pp10,P[1],c1);

full_adder FA1(pp02,pp11,pp20,s1,c2);
full_adder FA2(pp03,pp12,pp21,s2,c3);
full_adder FA3(pp13,pp22,pp31,s3,c4);

// Stage 2
half_adder HA2(s1,c1,P[2],c5);

full_adder FA4(s2,c2,pp30,s4,c6);
full_adder FA5(s3,c3,pp32,s5,c7);
half_adder HA3(c4,pp23,s6,c8);

// Final Addition
wire c9,c10,c11;

full_adder FA6(s4,c5,P[3],P[3],c9);
full_adder FA7(s5,c6,c9,P[4],c10);
full_adder FA8(s6,c7,c10,P[5],c11);
full_adder FA9(pp33,c8,c11,P[6],P[7]);

endmodule

//=========================================================
// Half Adder
//=========================================================
module half_adder(
    input a,
    input b,
    output sum,
    output carry
);

assign sum = a ^ b;
assign carry = a & b;

endmodule

//=========================================================
// Full Adder
//=========================================================
module full_adder(
    input a,
    input b,
    input cin,
    output sum,
    output cout
);

assign sum = a ^ b ^ cin;
assign cout = (a & b) | (b & cin) | (a & cin);

endmodule
