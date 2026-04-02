import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

async def tick(dut):
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)


@cocotb.test()
async def test_write_read(dut):

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    dut.wb_addr.value = 4 #wb_addr[11:2 = 1 -> mem[1]]
    dut.wb_dat_m2s.value = 42
    dut.wb_we.value = 1
    dut.wb_stb.value = 1
    dut.wb_cyc.value = 1
    await tick(dut)

    assert dut.wb_ack.value == 1

    dut.wb_we.value = 0

    await tick(dut)

    assert dut.wb_dat_s2m.value == 42


@cocotb.test()
async def test_different_addresses(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    dut.wb_addr.value = 4
    dut.wb_dat_m2s.value = 1
    dut.wb_we.value = 1
    dut.wb_stb.value = 1
    dut.wb_cyc.value = 1
    await tick(dut)

    assert dut.wb_ack.value == 1

    dut.wb_we.value = 0

    await tick(dut)

    assert dut.wb_dat_s2m.value == 1

    await tick(dut)

    dut.wb_addr.value = 8
    dut.wb_dat_m2s.value = 2
    dut.wb_we.value = 1
    dut.wb_stb.value = 1
    dut.wb_cyc.value = 1
    await tick(dut)

    assert dut.wb_ack.value == 1
    dut.wb_we.value = 0
    
    await tick(dut)

    assert dut.wb_dat_s2m.value == 2


@cocotb.test()
async def test_ack(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await tick(dut)

    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    assert dut.wb_ack.value == 1

    await tick(dut)

    dut.wb_cyc.value = 0
    dut.wb_stb.value = 0

    await tick(dut)

    assert dut.wb_ack.value == 0