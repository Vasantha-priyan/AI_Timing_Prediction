// Synchronous FIFO Benchmark Module
module fifo #(
    parameter DATA_WIDTH = 8,
    parameter DEPTH = 16
)(
    input wire clk,
    input wire rst,
    input wire wr_en,
    input wire rd_en,
    input wire [DATA_WIDTH-1:0] din,
    output reg [DATA_WIDTH-1:0] dout,
    output wire full,
    output wire empty,
    output reg [4:0] fifo_cnt
);
    reg [DATA_WIDTH-1:0] mem [0:DEPTH-1];
    reg [3:0] wr_ptr;
    reg [3:0] rd_ptr;

    assign full  = (fifo_cnt == DEPTH);
    assign empty = (fifo_cnt == 0);

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            wr_ptr <= 0;
            rd_ptr <= 0;
            fifo_cnt <= 0;
            dout <= 0;
        end else begin
            if (wr_en && !full) begin
                mem[wr_ptr] <= din;
                wr_ptr <= wr_ptr + 1'b1;
            end
            if (rd_en && !empty) begin
                dout <= mem[rd_ptr];
                rd_ptr <= rd_ptr + 1'b1;
            end
            case ({wr_en && !full, rd_en && !empty})
                2'b10: fifo_cnt <= fifo_cnt + 1'b1;
                2'b01: fifo_cnt <= fifo_cnt - 1'b1;
                default: fifo_cnt <= fifo_cnt;
            endcase
        end
    end
endmodule
