module top(
    input  wire clk,
    output reg  led = 1'b0
);

    reg [23:0] counter = 24'd0;

    always @(posedge clk) begin
        if (counter == 24'd13_499_999) begin
            counter <= 24'd0;
            led <= ~led;
        end else begin
            counter <= counter + 1'b1;
        end
    end

endmodule
