module wb_timer (
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
    output wire timer_irq
);



    reg [7:0] control;
    reg [7:0] limit;
    reg [7:0] value;
    reg [7:0] status;


    always @(posedge clk) begin
        if (rst) begin
            value <= 0;
            status <= 0;
        end else if(control[0] && value == limit) begin
            status <= 1;
            value <= 0;
        end else if (control[0]) begin
            value <= value + 1;
        end else begin
            
        end

    end

    always @(posedge clk) begin
        if (rst) begin
            control <= 0;
            limit <= 0;

        end else if(wb_cyc && wb_stb && wb_we) begin
            if(wb_addr[3:2] == 2'b00) begin
                control <= wb_dat_m2s[7:0];
            end else if (wb_addr[3:2] == 2'b01) begin
                limit <= wb_dat_m2s[7:0];
            end else begin
                
            end
        end
    end


    assign wb_dat_s2m = (wb_addr[3:2] == 2'b00) ? {24'b0, control} :
                (wb_addr[3:2] == 2'b01) ? {24'b0, limit} :
                (wb_addr[3:2] == 2'b10) ? {24'b0, value} :
                (wb_addr[3:2] == 2'b11) ? {24'b0, status}:
                32'h0;

    
    assign wb_ack = wb_stb && wb_cyc;

    assign timer_irq = status[0];
endmodule