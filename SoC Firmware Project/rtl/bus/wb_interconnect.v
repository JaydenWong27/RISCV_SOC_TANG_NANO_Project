module wb_interconnect (
    input wire [31:0] wb_addr,
    input wire [31:0] wb_dat_m2s,
    input wire wb_cyc,
    input wire wb_stb,
    input wire wb_we,
    input wire [3:0] wb_sel,

    output wire [31:0] wb_dat_s2m,
    output wire wb_ack,

    output wire ram_stb,
    output wire uart_stb,
    output wire pwm_stb,
    output wire gpio_stb,
    output wire timer_stb,

    input wire [31:0] ram_dat_s2m,
    input wire ram_ack,
    input wire[31:0] uart_dat_s2m,
    input wire uart_ack,
    input wire [31:0] gpio_dat_s2m,
    input wire gpio_ack,
    input wire [31:0] pwm_dat_s2m,
    input wire pwm_ack,
    input wire [31:0] timer_dat_s2m,
    input wire timer_ack

);

wire sel_ram = (wb_addr[31:28] == 4'h0);
wire sel_uart = (wb_addr[31:28] == 4'h1 && (wb_addr[15:12] == 4'h0));
wire sel_pwm = (wb_addr[31:28] == 4'h1 && (wb_addr[15:12] == 4'h2));
wire sel_gpio = (wb_addr[31:28] == 4'h1 && (wb_addr[15:12] == 4'h1));
wire sel_timer = (wb_addr[31:28] == 4'h1) && (wb_addr[15:12] == 4'h3);

assign ram_stb = wb_stb && wb_cyc && sel_ram;
assign uart_stb = wb_stb && wb_cyc && sel_uart;
assign pwm_stb = wb_stb && wb_cyc && sel_pwm;
assign gpio_stb = wb_stb && wb_cyc && sel_gpio;
assign timer_stb = wb_stb && wb_cyc && sel_timer;

assign wb_dat_s2m = sel_ram ? ram_dat_s2m : sel_uart ? uart_dat_s2m : sel_gpio ? gpio_dat_s2m : sel_pwm ? pwm_dat_s2m: sel_timer ? timer_dat_s2m: 32'h0;
assign wb_ack = ram_ack | uart_ack | gpio_ack | pwm_ack | timer_ack;


endmodule