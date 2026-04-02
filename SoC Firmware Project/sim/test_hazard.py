import cocotb 
from cocotb.triggers import Timer

@cocotb.test()
async def none(dut):
    dut.ex_mw_rd.value = 0
    dut.ex_mw_reg_write.value = 0
    dut.ex_mw_mem_read.value = 0
    dut.id_rs1.value = 0
    dut.id_rs2.value = 0
    dut.branch_taken.value = 0
    await Timer(1, unit="ns")
    assert dut.stall.value == 0
    assert dut.flush.value == 0

@cocotb.test()
async def load_use_hazard_stall_fire(dut):
    dut.ex_mw_mem_read.value = 1
    dut.ex_mw_reg_write.value = 1
    dut.ex_mw_rd.value = 1
    dut.id_rs1.value = 1
    dut.id_rs2.value = 0
    dut.branch_taken.value = 0
    await Timer(1, unit="ns")
    assert dut.stall.value == 1
    assert dut.flush.value == 0

@cocotb.test()
async def load_use_hazard_on_rs2(dut):
    dut.ex_mw_mem_read.value = 1
    dut.ex_mw_reg_write.value = 1
    dut.ex_mw_rd.value = 2
    dut.id_rs1.value = 0
    dut.id_rs2.value = 2
    dut.branch_taken.value = 0
    await Timer(1, unit="ns")
    assert dut.stall.value == 1
    assert dut.flush.value == 0

@cocotb.test()
async def load_to_zero(dut):
    dut.ex_mw_mem_read.value = 1
    dut.ex_mw_reg_write.value = 1
    dut.ex_mw_rd.value = 0
    dut.id_rs1.value = 0
    dut.id_rs2.value = 0
    dut.branch_taken.value = 0
    await Timer(1, unit="ns")
    assert dut.stall.value == 0
    assert dut.flush.value == 0

@cocotb.test()
async def branch_taken_flush_fire(dut):
    dut.ex_mw_mem_read.value = 0
    dut.ex_mw_reg_write.value = 0  
    dut.ex_mw_rd.value = 0
    dut.id_rs1.value = 0
    dut.id_rs2.value = 0
    dut.branch_taken.value = 1
    await Timer(1, unit="ns")
    assert dut.stall.value == 0
    assert dut.flush.value == 1

@cocotb.test()
async def branch_taken_and_load_hazard(dut):
    dut.ex_mw_mem_read.value = 1
    dut.ex_mw_reg_write.value = 1
    dut.ex_mw_rd.value = 1
    dut.id_rs1.value = 1
    dut.id_rs2.value = 0
    dut.branch_taken.value = 1
    await Timer(1, unit="ns")
    assert dut.stall.value == 1
    assert dut.flush.value == 1

@cocotb.test()
async def load_in_register_no_stall_no_register_match(dut):
    dut.ex_mw_mem_read.value = 1
    dut.ex_mw_reg_write.value = 1
    dut.ex_mw_rd.value = 5
    dut.id_rs1.value = 1
    dut.id_rs2.value = 2
    dut.branch_taken.value = 0
    await Timer(1, unit="ns")
    assert dut.stall.value == 0
    assert dut.flush.value == 0

