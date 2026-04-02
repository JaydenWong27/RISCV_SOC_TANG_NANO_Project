module rv32i_core (
    input wire clk,
    input wire rst,
    input wire [31:0] instr_data,
    input wire instr_ack,
    input wire [31:0] wb_dat_s2m,
    input wire wb_ack,
    input wire timer_irq,

    output wire [31:0] instr_addr,
    output wire instr_cyc,
    output wire instr_stb,
    output wire [31:0] wb_addr,
    output wire [31:0] wb_dat_m2s,
    output wire wb_cyc,
    output wire wb_stb,
    output wire wb_we,
    output wire [3:0] wb_sel
);

//decode outputs
wire[4:0] decode_rs1, decode_rs2, decode_rd;
wire [31:0] decode_imm;
wire[3:0] decode_alu_op;
wire decode_reg_write, decode_mem_read, decode_mem_write;
wire decode_branch, decode_jump, decode_mem_to_reg;

//regfile outputs
wire[31:0] regfile_rs1_data, regfile_rs2_data;

//ALU
wire [31:0] alu_a, alu_b, alu_result;
wire alu_zero;


// Program Counter
reg [31:0] pc;

//IF/ID pipeline register
reg [31:0] if_id_instr; //IF/ID
reg [31:0] if_id_pc;

//ID/EX pipeline register
reg[31:0] id_ex_pc;
reg [31:0] id_ex_rs1_data;
reg [31:0] id_ex_rs2_data;
reg [31:0] id_ex_imm;
reg [4:0] id_ex_rd;
reg [3:0] id_ex_alu_op;
reg id_ex_reg_write;
reg id_ex_mem_read;
reg id_ex_mem_write;
reg id_ex_branch;
reg id_ex_jump;
reg id_ex_mem_to_reg;
reg id_ex_use_imm;

// EX/MEM pipeline register
reg [31:0] ex_mem_alu_result;
reg [31:0] ex_mem_rs2_data;
reg [4:0] ex_mem_rd;
reg ex_mem_reg_write;
reg ex_mem_mem_read;
reg ex_mem_mem_write;
reg ex_mem_mem_to_reg;

// MEM/WB pipeline register
reg [31:0] mem_wb_alu_result;
reg [31:0] mem_wb_mem_data;
reg [4:0] mem_wb_rd;
reg mem_wb_reg_write;
reg mem_wb_mem_to_reg;


//writeback signals
wire[4:0] wb_rd;
wire[31:0] wb_rd_data;
wire wb_reg_write;

//hazard input wires
wire [4:0] hazard_ex_mw_rd;
wire hazard_ex_mw_reg_write;
wire hazard_ex_mw_mem_read;
wire [4:0] hazard_id_rs1;
wire [4:0] hazard_id_rs2;
wire hazard_branch_taken;
wire hazard_stall;
wire hazard_flush;

//branch target
wire [31:0] branch_target;

assign hazard_branch_taken = id_ex_branch && alu_zero;

//ALU inputs
assign alu_a = id_ex_rs1_data;
assign alu_b = (id_ex_use_imm)? id_ex_imm : id_ex_rs2_data;

// Writeback: mux between ALU result and memory data
assign wb_rd_data = mem_wb_mem_to_reg ? mem_wb_mem_data : mem_wb_alu_result;
assign wb_rd = mem_wb_rd;
assign wb_reg_write = mem_wb_reg_write;

//Hazard input: connect pipeline stage signals to hazard unit
assign hazard_ex_mw_rd = id_ex_rd;
assign hazard_ex_mw_reg_write = id_ex_reg_write;
assign hazard_ex_mw_mem_read = id_ex_mem_read;
assign hazard_id_rs1 = decode_rs1;
assign hazard_id_rs2 = decode_rs2;

// Fetch signals to instruction memory
assign instr_addr = pc;
assign instr_cyc  = 1;
assign instr_stb  = 1;


assign branch_target = id_ex_pc + id_ex_imm;

//wishbone data memory outputs

assign wb_addr = ex_mem_alu_result;
assign wb_dat_m2s = ex_mem_rs2_data;
assign wb_we = ex_mem_mem_write;
assign wb_cyc = ex_mem_mem_read | ex_mem_mem_write;
assign wb_stb = ex_mem_mem_read | ex_mem_mem_write;
assign wb_sel = 4'b1111;



 rv32i_decode decode(
    .instr(if_id_instr),
    .rs1(decode_rs1),
    .rs2(decode_rs2),
    .rd(decode_rd),
    .imm(decode_imm),
    .alu_op(decode_alu_op),
    .reg_write(decode_reg_write),
    .mem_read(decode_mem_read),
    .mem_write(decode_mem_write),
    .branch(decode_branch),
    .jump(decode_jump),
    .mem_to_reg(decode_mem_to_reg)
);

rv32i_regfile regfile(
    .clk(clk),
    .rst(rst),
    .rs1_addr(decode_rs1),
    .rs2_addr(decode_rs2),
    .rs1_data(regfile_rs1_data),
    .rs2_data(regfile_rs2_data),
    .rd_addr(wb_rd),
    .rd_data(wb_rd_data),
    .rd_we(wb_reg_write)
);

rv32i_alu alu(
    .a(alu_a),
    .b(alu_b),
    .op(id_ex_alu_op),
    .result(alu_result),
    .zero(alu_zero)
);

rv32i_hazard hazard (
    .ex_mw_rd(hazard_ex_mw_rd),
    .ex_mw_reg_write(hazard_ex_mw_reg_write),
    .ex_mw_mem_read(hazard_ex_mw_mem_read),
    .id_rs1(hazard_id_rs1),
    .id_rs2(hazard_id_rs2),
    .branch_taken(hazard_branch_taken),
    .stall(hazard_stall),
    .flush(hazard_flush)
);

always @(posedge clk) begin
    if (rst)
        pc <= 0;
    else if (hazard_stall)
        pc <= pc; // freeze if there is hazard
    else if (hazard_branch_taken)
        pc <= branch_target; // jump to branch
    else
        pc <= pc + 4; // normal; next instruction
end

//IF/ID block : latches fetched instruction
always @(posedge clk) begin
    if (rst || hazard_flush) begin
        if_id_instr <= 32'h00000013; // flush then do nothing
        if_id_pc <= 0;
    end else if (!hazard_stall) begin
        if_id_instr <= instr_data; //latch new instructions , normal then grab instruction from memory
        if_id_pc <= pc;
    end
end

//ID/EX block: latches decode outputs
always @(posedge clk) begin
    if (rst || hazard_flush) begin
        id_ex_rs1_data <= 0;
        id_ex_rs2_data <= 0;
        id_ex_imm <= 0;
        id_ex_rd <= 0;
        id_ex_alu_op <= 0;
        id_ex_reg_write <= 0; // flush then zero everything out
        id_ex_mem_read <= 0;
        id_ex_mem_write <= 0;
        id_ex_branch <= 0;
        id_ex_jump <= 0;
        id_ex_mem_to_reg <= 0;
        id_ex_pc <= 0;
        id_ex_use_imm <= 0;
    end else if (!hazard_stall) begin
        id_ex_rs1_data <= regfile_rs1_data; //latch register value
        id_ex_rs2_data <= regfile_rs2_data; 
        id_ex_imm <= decode_imm;
        id_ex_rd <= decode_rd; //latch destination register
        id_ex_alu_op <= decode_alu_op; //latch what operation to do
        id_ex_reg_write <= decode_reg_write;
        id_ex_mem_read <= decode_mem_read;
        id_ex_mem_write <= decode_mem_write;
        id_ex_branch <= decode_branch;
        id_ex_jump <= decode_jump;
        id_ex_mem_to_reg <= decode_mem_to_reg;
        id_ex_pc <= if_id_pc;
        id_ex_use_imm <= (if_id_instr[6:0] != 7'b0110011);
    end
end
//ex/mem block :latches ALU result

always @(posedge clk) begin 
    if (rst) begin
        ex_mem_alu_result <= 0; // save what ALU computed
        ex_mem_rs2_data <= 0;
        ex_mem_rd <= 0; //keep track of destination register
        ex_mem_reg_write <= 0;
        ex_mem_mem_read <= 0;
        ex_mem_mem_write <= 0;
        ex_mem_mem_to_reg <= 0;
    end else begin
        ex_mem_alu_result <= alu_result;
        ex_mem_rs2_data <= id_ex_rs2_data;
        ex_mem_rd <= id_ex_rd;
        ex_mem_reg_write <= id_ex_reg_write;
        ex_mem_mem_read <= id_ex_mem_read;
        ex_mem_mem_write <= id_ex_mem_write;
        ex_mem_mem_to_reg <= id_ex_mem_to_reg;
    end
 end

//mem/wb block then latches memory data
 always @(posedge clk) begin
    if (rst) begin
        mem_wb_alu_result <= 0;
        mem_wb_mem_data <= 0;
        mem_wb_rd <= 0;
        mem_wb_reg_write <= 0;
        mem_wb_mem_to_reg <= 0;
    end else begin
        mem_wb_alu_result <= ex_mem_alu_result; // ALU result passes through
        mem_wb_mem_data <= wb_dat_s2m; //memory data arrives here
        mem_wb_rd <= ex_mem_rd; //still tracking destination
        mem_wb_reg_write <= ex_mem_reg_write;
        mem_wb_mem_to_reg <= ex_mem_mem_to_reg;
    end
 end

endmodule