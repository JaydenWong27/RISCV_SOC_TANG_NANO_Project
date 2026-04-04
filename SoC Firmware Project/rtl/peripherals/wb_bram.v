module wb_bram (
    input wire clk,
    input wire rst,
    input wire [31:0] wb_addr,
    input wire [31:0] wb_dat_m2s,
    input wire wb_cyc, 
    input wire wb_stb,
    input wire wb_we,
    input wire [3:0] wb_sel,

    output wire [31:0] wb_dat_s2m,
    output wire wb_ack

);

reg [31:0] mem [0:8191];
initial $readmemh("firmware.hex", mem);

always @(posedge clk) begin
    if(wb_stb && wb_cyc && wb_we) begin
        mem[wb_addr[14:2]] <= wb_dat_m2s;
    end
end

assign wb_dat_s2m = mem[wb_addr[14:2]]; // read
assign wb_ack = wb_stb && wb_cyc; // always ack 



endmodule