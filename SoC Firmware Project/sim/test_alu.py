import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer

@cocotb.test()
async def test_add(dut):
    dut.a.value = 5
    dut.b.value = 3
    dut.op.value = 0b0000
    await Timer(1, unit="ns")
    assert dut.result.value == 8, f"ADD failed: got {dut.result.value}"

@cocotb.test()
async def test_sub(dut):
    dut.a.value = 10
    dut.b.value = 4
    dut.op.value = 0b0001
    await Timer(1, unit="ns")
    assert dut.result.value == 6, f"SUB failed = got {dut.result.value}"

@cocotb.test()
async def test_and(dut):
    dut.a.value = 7
    dut.b.value = 1
    dut.op.value = 0b0010
    await Timer(1, unit="ns")
    assert dut.result.value == 1, f"AND failed = got {dut.result.value}"

@cocotb.test()
async def test_or(dut):
    dut.a.value = 7
    dut.b.value = 8
    dut.op.value = 0b0011
    await Timer(1, unit="ns")
    assert dut.result.value == 15, f"OR failed = got {dut.result.value}"

@cocotb.test()
async def test_xor(dut):
    dut.a.value = 5
    dut.b.value = 3
    dut.op.value = 0b0100
    await Timer(1, unit="ns")
    assert dut.result.value == 6, f"XOR failed = {dut.result.value}"

@cocotb.test()
async def test_shiftleft(dut):
    dut.a.value = 2
    dut.b.value = 1
    dut.op.value = 0b0101
    await Timer(1,unit="ns")
    assert dut.result.value == 4, f"Shift left failed = {dut.result.value}"

@cocotb.test()
async def test_shiftright(dut):
    dut.a.value = 4
    dut.b.value = 1
    dut.op.value = 0b0110
    await Timer(1,unit="ns")
    assert dut.result.value == 2, f"Shift right failed = {dut.result.value}"

@cocotb.test()
async def test_sra(dut):
    dut.a.value = 0xFFFFFFFC   # -4 in two's complement
    dut.b.value = 1
    dut.op.value = 0b0111      # SRA
    await Timer(1, unit="ns")
    assert dut.result.value == 0xFFFFFFFE, f"SRA failed: got {dut.result.value}"

@cocotb.test()
async def test_slt_signed(dut):
    dut.a.value  = 0xFFFFFFFF
    dut.b.value  = 0x00000001
    dut.op.value = 0b1000
    await Timer(1, unit="ns")
    assert dut.result.value == 1,  "SLT: -1 should be less than +1"

@cocotb.test()
async def test_SLTU(dut):
    dut.a.value=0xFFFFFFFF
    dut.b.value = 0x1
    dut.op.value = 0b1001
    await Timer(1, unit="ns")
    assert dut.result.value == 0, f"SLTU: SLTU failed = {dut.result.value}"
