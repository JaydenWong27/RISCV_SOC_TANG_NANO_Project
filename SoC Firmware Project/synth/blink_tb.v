`timescale 1ns/1ps

module blink_tb;
    reg clk = 0;
    wire led;

    top dut (
        .clk(clk),
        .led(led)
    );

    always #5 clk = ~clk;

    initial begin
        $dumpfile("blink.vcd");
        $dumpvars(0, blink_tb);

        // Jump close to the toggle point so sim finishes fast.
        dut.counter = 24'd13_499_995;

        #200;
        $finish;
    end
endmodule
