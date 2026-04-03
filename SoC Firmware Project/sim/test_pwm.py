import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

async def tick(dut):
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

async def reset (dut):
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
async def test_PWM_high(dut):

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await reset(dut)


    dut.wb_dat_m2s.value = 0xFF
    dut.wb_addr.value = 0x00
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_dat_m2s.value = 0x0F
    dut.wb_addr.value = 0x04
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_dat_m2s.value = 0x01
    dut.wb_addr.value = 0x08
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_we.value = 0

    await tick(dut)

    assert dut.pwm_out.value == 1




@cocotb.test()
async def test_PWM_Low(dut):

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await reset(dut)


    dut.wb_dat_m2s.value = 0xFF
    dut.wb_addr.value = 0x00
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_dat_m2s.value = 0x0F
    dut.wb_addr.value = 0x04
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_dat_m2s.value = 0x01
    dut.wb_addr.value = 0x08
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_we.value = 0

    for _ in range(16):
        await tick(dut)

    assert dut.pwm_out.value == 0




@cocotb.test()
async def test_counter_reset_period(dut):
    
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await reset(dut)


    dut.wb_dat_m2s.value = 0x04
    dut.wb_addr.value = 0x00
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_dat_m2s.value = 0x02
    dut.wb_addr.value = 0x04
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_dat_m2s.value = 0x01
    dut.wb_addr.value = 0x08
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_we.value = 0

    for _ in range(5):
        await tick(dut)

    assert dut.pwm_out.value == 1




@cocotb.test()
async def test_Disabled_PWM_Low(dut):
    
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await reset(dut)


    dut.wb_dat_m2s.value = 0xFF
    dut.wb_addr.value = 0x00
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_dat_m2s.value = 0x0F
    dut.wb_addr.value = 0x04
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_dat_m2s.value = 0x00
    dut.wb_addr.value = 0x08
    dut.wb_we.value = 1
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1

    await tick(dut)

    dut.wb_we.value = 0

    for _ in range(5):
        await tick(dut)

    assert dut.pwm_out.value == 0


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


