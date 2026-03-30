import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_add(dut):
    await Timer(1, unit="ns")
