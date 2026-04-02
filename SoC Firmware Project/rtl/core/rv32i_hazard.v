module rv32i_hazard (
    input wire [4:0] ex_mw_rd,
    input wire ex_mw_reg_write,
    input wire ex_mw_mem_read,
    input wire [4:0] id_rs1,
    input wire [4:0] id_rs2,
    input wire branch_taken,
    output wire stall,
    output wire flush
);
assign stall = ex_mw_mem_read && ex_mw_reg_write && (ex_mw_rd != 5'b0) && (ex_mw_rd == id_rs1 || ex_mw_rd == id_rs2);

assign flush = branch_taken;
endmodule