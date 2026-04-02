module wb_gpio (
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

    inout wire [7:0] gpio_pins
);

reg [7:0] gpio_out;
reg [7:0] gpio_dir;
reg [7:0] gpio_in;

always @(posedge clk) begin
    if (rst) begin
        gpio_out <= 0;
        gpio_dir <= 0;
        gpio_in <= 0;
    end else if(wb_cyc && wb_stb && wb_we) begin
        if(wb_addr[3:2] == 2'b00) begin
            gpio_out <= wb_dat_m2s[7:0];
        end else if (wb_addr[3:2] == 2'b01) begin
            gpio_dir <= wb_dat_m2s[7:0];
        end
    end
    gpio_in <= gpio_pins;
end


assign wb_dat_s2m = (wb_addr[3:2] == 2'b00) ? {24'b0, gpio_out} :
                    (wb_addr[3:2] == 2'b01) ? {24'b0, gpio_dir} :
                    (wb_addr[3:2] == 2'b10) ? {24'b0, gpio_in} :
                    32'h0;

genvar i;

    generate
        for(i = 0; i < 8; i = i + 1)begin
             assign gpio_pins[i] = gpio_dir[i] ? gpio_out[i] : 1'bz;
        end

    endgenerate

assign wb_ack = wb_stb && wb_cyc;




endmodule
