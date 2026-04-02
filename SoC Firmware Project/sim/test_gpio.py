import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

async def tick(dut):
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)


async def reset(dut):
    dut.rst.value = 1
    dut.wb_cyc.value = 0
    dut.wb_stb.value = 0
    dut.wb_we.value = 0
    dut.wb_addr.value = 0
    dut.wb_dat_m2s.value = 0
    await tick(dut)
    await tick(dut)
    dut.rst.value = 0


@cocotb.test()
async def test_output_pin(dut):

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await reset(dut)


    dut.wb_dat_m2s.value = 0xFF
    dut.wb_addr.value = 0x04
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_dat_m2s.value = 0x01
    dut.wb_addr.value = 0x00


    await tick(dut)

    assert (int(dut.gpio_pins.value) & 0x01) == 1




@cocotb.test()
async def test_direction_control(dut):

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await reset(dut)

    dut.wb_dat_m2s.value = 0x00
    dut.wb_addr.value = 0x04
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_dat_m2s.value = 0xFF
    dut.wb_addr.value = 0x00
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)


    dut.wb_dat_m2s.value = 0x00
    dut.wb_addr.value = 0x00

    await tick(dut)

    assert 'Z' in str(dut.gpio_pins.value)

@cocotb.test()
async def test_input_read(dut):

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await reset(dut)

    dut.wb_dat_m2s.value = 0x00
    dut.wb_addr.value = 0x04
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.gpio_pins.value = 0b00000101

    await tick(dut)

    dut.wb_addr.value = 0x08
    dut.wb_we.value = 0
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    assert dut.wb_dat_s2m.value == 0x00000005




@cocotb.test()
async def test_ack(dut):

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await reset(dut)


    dut.wb_dat_m2s.value = 0x00
    dut.wb_addr.value = 0x00
    dut.wb_we.value = 0
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut) 

    assert dut.wb_ack.value == 1

    await tick(dut)

    dut.wb_dat_m2s.value = 0x00
    dut.wb_addr.value = 0x00
    dut.wb_we.value = 0
    dut.wb_cyc.value = 0
    dut.wb_stb.value = 0

    await tick(dut)
    
    assert dut.wb_ack.value == 0



