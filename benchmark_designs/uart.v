// UART Receiver and Transmitter Benchmark Core
module uart (
    input wire clk,
    input wire rst,
    input wire rx,
    input wire tx_start,
    input wire [7:0] tx_data,
    output reg tx,
    output reg tx_busy,
    output reg rx_ready,
    output reg [7:0] rx_data
);
    // Prescaler / Baud generator logic
    reg [15:0] baud_cnt;
    reg baud_tick;
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            baud_cnt <= 16'd0;
            baud_tick <= 1'b0;
        end else begin
            if (baud_cnt == 16'd434) begin
                baud_cnt <= 16'd0;
                baud_tick <= 1'b1;
            end else begin
                baud_cnt <= baud_cnt + 1'b1;
                baud_tick <= 1'b0;
            end
        end
    end

    // FSM for TX
    reg [3:0] tx_state;
    reg [7:0] tx_shift;
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            tx <= 1'b1;
            tx_busy <= 1'b0;
            tx_state <= 4'd0;
            tx_shift <= 8'd0;
        end else if (tx_start && !tx_busy) begin
            tx_busy <= 1'b1;
            tx_shift <= tx_data;
            tx_state <= 4'd1;
            tx <= 1'b0;
        end else if (tx_busy && baud_tick) begin
            if (tx_state >= 4'd1 && tx_state <= 4'd8) begin
                tx <= tx_shift[0];
                tx_shift <= tx_shift >> 1;
                tx_state <= tx_state + 1'b1;
            end else if (tx_state == 4'd9) begin
                tx <= 1'b1;
                tx_state <= 4'd10;
            end else begin
                tx_busy <= 1'b0;
                tx_state <= 4'd0;
            end
        end
    end

    // FSM for RX
    reg [3:0] rx_state;
    reg [7:0] rx_shift;
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            rx_ready <= 1'b0;
            rx_state <= 4'd0;
            rx_data <= 8'd0;
            rx_shift <= 8'd0;
        end else if (baud_tick) begin
            case (rx_state)
                4'd0: if (!rx) rx_state <= 4'd1;
                4'd1, 4'd2, 4'd3, 4'd4, 4'd5, 4'd6, 4'd7, 4'd8: begin
                    rx_shift <= {rx, rx_shift[7:1]};
                    rx_state <= rx_state + 1'b1;
                end
                4'd9: begin
                    rx_data <= rx_shift;
                    rx_ready <= 1'b1;
                    rx_state <= 4'd0;
                end
                default: rx_state <= 4'd0;
            endcase
        end else begin
            rx_ready <= 1'b0;
        end
    end
endmodule
