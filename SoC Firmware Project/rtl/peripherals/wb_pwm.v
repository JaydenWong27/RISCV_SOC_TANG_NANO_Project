module wb_pwm (
    input wire clk,
    input wire rst,
    input wire [31:0] wb_addr,
    input wire [31:0] wb_dat_m2s,
    input wire wb_cyc, 
    input wire wb_stb,
    input wire wb_we,
    input wire [3:0] wb_sel,

    output wire [31:0] wb_dat_s2m,
    output wire wb_ack,

    output wire pwm_out
);

    reg [7:0] period;
    reg [7:0] compare;
    reg [7:0] enabled;

    reg [31:0] counter;

    always @(posedge clk) begin
        if (rst) begin
            counter <= 0;
        end else if(enabled[0] && counter == period) begin
            counter <= 0;
        end else if (enabled[0]) begin
            counter <= counter + 1;
        end else begin
            
        end

    end

    always @(posedge clk) begin
        if (rst) begin
            period <= 0;
            compare <= 0;
            enabled <= 0;

        end else if(wb_cyc && wb_stb && wb_we) begin
            if(wb_addr[3:2] == 2'b00) begin
                period <= wb_dat_m2s[7:0];
            end else if (wb_addr[3:2] == 2'b01) begin
                compare <= wb_dat_m2s[7:0];
            end else if (wb_addr[3:2] == 2'b10) begin
                enabled <= wb_dat_m2s[7:0];
            end else begin
                
            end
        end
    end

    assign pwm_out = enabled && (counter < compare);

    assign wb_dat_s2m = (wb_addr[3:2] == 2'b00) ? {24'b0, period} :
                    (wb_addr[3:2] == 2'b01) ? {24'b0, compare} :
                    (wb_addr[3:2] == 2'b10) ? {24'b0, enabled} :
                    32'h0;

    assign wb_ack = wb_stb && wb_cyc;

endmodule