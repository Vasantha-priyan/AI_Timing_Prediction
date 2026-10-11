// SPI Master Controller Benchmark
module spi_controller (
    input wire clk,
    input wire rst,
    input wire start,
    input wire [7:0] tx_byte,
    output reg [7:0] rx_byte,
    output reg done,
    output reg sclk,
    output reg mosi,
    input wire miso,
    output reg cs_n
);
    reg [3:0] bit_cnt;
    reg [7:0] tx_reg;
    reg [7:0] rx_reg;
    reg [1:0] state;

    localparam IDLE = 2'b00, TRANSFER = 2'b01, FINISH = 2'b10;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            state <= IDLE;
            cs_n <= 1'b1;
            sclk <= 1'b0;
            mosi <= 1'b0;
            done <= 1'b0;
            bit_cnt <= 4'd0;
            tx_reg <= 8'd0;
            rx_reg <= 8'd0;
            rx_byte <= 8'd0;
        end else begin
            case (state)
                IDLE: begin
                    done <= 1'b0;
                    cs_n <= 1'b1;
                    sclk <= 1'b0;
                    if (start) begin
                        state <= TRANSFER;
                        tx_reg <= tx_byte;
                        cs_n <= 1'b0;
                        bit_cnt <= 4'd7;
                    end
                end
                TRANSFER: begin
                    sclk <= ~sclk;
                    if (sclk) begin
                        mosi <= tx_reg[bit_cnt];
                    end else begin
                        rx_reg[bit_cnt] <= miso;
                        if (bit_cnt == 4'd0) begin
                            state <= FINISH;
                        end else begin
                            bit_cnt <= bit_cnt - 1'b1;
                        end
                    end
                end
                FINISH: begin
                    cs_n <= 1'b1;
                    sclk <= 1'b0;
                    rx_byte <= rx_reg;
                    done <= 1'b1;
                    state <= IDLE;
                end
                default: state <= IDLE;
            endcase
        end
    end
endmodule
