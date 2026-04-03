import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

async def tick(dut):
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

async def reset (dut):
    dut.rst.value = 1
    dut.uart_rx.value = 1
    dut.wb_cyc.value = 0
    dut.wb_stb.value = 0
    dut.wb_we.value = 0
    dut.wb_addr.value = 0
    dut.wb_dat_m2s.value = 0
    await tick(dut)
    await tick(dut)
    dut.rst.value = 0


@cocotb.test()
async def test_tx_count(dut):

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await reset(dut)

    dut.wb_dat_m2s.value = 0x55
    dut.wb_addr.value = 0x00
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_we.value = 0
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    for _ in range(235):
        await tick(dut)

    assert dut.uart_tx.value == 0


    for _ in range(235):
        await tick(dut)

    assert dut.uart_tx.value == 1


    for _ in range(235):
        await tick(dut)

    assert dut.uart_tx.value == 0

    for _ in range(235):
        await tick(dut)

    assert dut.uart_tx.value == 1

    for _ in range(235):
        await tick(dut)

    assert dut.uart_tx.value == 0

    for _ in range(235):
        await tick(dut)

    assert dut.uart_tx.value == 1

    for _ in range(235):
        await tick(dut)

    assert dut.uart_tx.value == 0

    for _ in range(235):
        await tick(dut)

    assert dut.uart_tx.value == 1

    for _ in range(235):
        await tick(dut)

    assert dut.uart_tx.value == 0

    for _ in range(235):
        await tick(dut)

    assert dut.uart_tx.value == 1

@cocotb.test()
async def test_rx_count(dut):

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await reset(dut)

    dut.uart_rx.value = 1

    dut.uart_rx.value = 0

    for _ in range(235):
        await tick(dut)

    dut.uart_rx.value = 1

    for _ in range(235):
        await tick(dut)

    dut.uart_rx.value = 0


    for _ in range(235):
        await tick(dut)

    dut.uart_rx.value = 1


    for _ in range(235):
        await tick(dut)

    dut.uart_rx.value = 0

    for _ in range(235):
        await tick(dut)

    dut.uart_rx.value = 1

    for _ in range(235):
        await tick(dut)

    dut.uart_rx.value = 0

    for _ in range(235):
        await tick(dut)

    dut.uart_rx.value = 1

    for _ in range(235):
        await tick(dut)

    dut.uart_rx.value = 0

    for _ in range (235):
        await tick(dut)

    dut.uart_rx.value = 1

    for _ in range (235):
        await tick(dut)

    dut.wb_addr.value = 0x08
    dut.wb_we.value = 0
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1
     
    await tick(dut)

    assert dut.wb_dat_s2m.value == 0x55




