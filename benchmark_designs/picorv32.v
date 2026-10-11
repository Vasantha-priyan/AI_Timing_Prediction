// PicoRV32 Lightweight RISC-V Benchmark Core Structure
module picorv32 (
    input wire clk,
    input wire resetn,
    output reg trap,
    output reg mem_valid,
    output reg [31:0] mem_addr,
    output reg [31:0] mem_wdata,
    output reg [3:0] mem_wstrb,
    input wire mem_ready,
    input wire [31:0] mem_rdata
);
    reg [31:0] pc;
    reg [31:0] regfile [0:31];
    reg [31:0] instr;
    reg [2:0] state;

    localparam FETCH = 3'b000, DECODE = 3'b001, EXECUTE = 3'b010, WRITEBACK = 3'b011;

    always @(posedge clk or negedge resetn) begin
        if (!resetn) begin
            pc <= 32'h0000_0000;
            trap <= 1'b0;
            mem_valid <= 1'b0;
            state <= FETCH;
            mem_addr <= 32'h0;
            mem_wdata <= 32'h0;
            mem_wstrb <= 4'h0;
        end else begin
            case (state)
                FETCH: begin
                    mem_valid <= 1'b1;
                    mem_addr <= pc;
                    mem_wstrb <= 4'b0000;
                    if (mem_ready) begin
                        instr <= mem_rdata;
                        mem_valid <= 1'b0;
                        state <= DECODE;
                    end
                end
                DECODE: begin
                    state <= EXECUTE;
                end
                EXECUTE: begin
                    pc <= pc + 4;
                    state <= WRITEBACK;
                end
                WRITEBACK: begin
                    state <= FETCH;
                end
                default: state <= FETCH;
            endcase
        end
    end
endmodule
