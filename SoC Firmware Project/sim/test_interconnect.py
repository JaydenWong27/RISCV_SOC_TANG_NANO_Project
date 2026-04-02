import cocotb 
from cocotb.clock import Clock
from cocotb.triggers import Timer

@cocotb.test()
async def test_ram_(dut):
    dut.wb_addr.value = 0x00000000
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1
    dut.wb_we.value = 0
    dut.wb_sel.value = 0b1111
    dut.wb_dat_m2s.value = 0

    dut.ram_dat_s2m.value = 0
    dut.ram_ack.value = 0
    dut.uart_dat_s2m.value = 0
    dut.uart_ack.value = 0
    dut.gpio_dat_s2m.value = 0
    dut.gpio_ack.value = 0
    dut.pwm_dat_s2m.value = 0
    dut.pwm_ack.value = 0
    dut.timer_dat_s2m.value = 0
    dut.timer_ack.value = 0

    await Timer(1, unit="ns")

    assert dut.ram_stb.value == 1
    assert dut.uart_stb.value == 0
    assert dut.gpio_stb.value == 0
    assert dut.pwm_stb.value == 0
    assert dut.timer_stb.value == 0


@cocotb.test()
async def test_uart(dut):
    dut.wb_addr.value = 0x10000000
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1
    dut.wb_we.value = 0
    dut.wb_sel.value = 0b1111
    dut.wb_dat_m2s.value = 0

    dut.ram_dat_s2m.value = 0
    dut.ram_ack.value = 0
    dut.uart_dat_s2m.value = 0
    dut.uart_ack.value = 0
    dut.gpio_dat_s2m.value = 0
    dut.gpio_ack.value = 0
    dut.pwm_dat_s2m.value = 0
    dut.pwm_ack.value = 0
    dut.timer_dat_s2m.value = 0
    dut.timer_ack.value = 0

    await Timer(1, unit = "ns")

    assert dut.ram_stb.value == 0
    assert dut.uart_stb.value == 1
    assert dut.gpio_stb.value == 0
    assert dut.pwm_stb.value == 0
    assert dut.timer_stb.value == 0

@cocotb.test()
async def test_gpio(dut):
    dut.wb_addr.value = 0x10001000
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1
    dut.wb_we.value = 0
    dut.wb_sel.value = 0b1111
    dut.wb_dat_m2s.value = 0

    dut.ram_dat_s2m.value = 0
    dut.ram_ack.value = 0
    dut.uart_dat_s2m.value = 0
    dut.uart_ack.value = 0
    dut.gpio_dat_s2m.value = 0
    dut.gpio_ack.value = 0
    dut.pwm_dat_s2m.value = 0
    dut.pwm_ack.value = 0
    dut.timer_dat_s2m.value = 0
    dut.timer_ack.value = 0

    await Timer(1,unit="ns")

    assert dut.ram_stb.value == 0
    assert dut.uart_stb.value == 0
    assert dut.gpio_stb.value == 1
    assert dut.pwm_stb.value == 0
    assert dut.timer_stb.value == 0

@cocotb.test()
async def test_PWM(dut):
    dut.wb_addr.value = 0x10002000
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1
    dut.wb_we.value = 0
    dut.wb_sel.value = 0b1111
    dut.wb_dat_m2s.value = 0

    dut.ram_dat_s2m.value = 0
    dut.ram_ack.value = 0
    dut.uart_dat_s2m.value = 0
    dut.uart_ack.value = 0
    dut.gpio_dat_s2m.value = 0
    dut.gpio_ack.value = 0
    dut.pwm_dat_s2m.value = 0
    dut.pwm_ack.value = 0
    dut.timer_dat_s2m.value = 0
    dut.timer_ack.value = 0
    
    await Timer(1,unit="ns")

    assert dut.ram_stb.value == 0
    assert dut.uart_stb.value == 0
    assert dut.gpio_stb.value == 0
    assert dut.pwm_stb.value == 1
    assert dut.timer_stb.value == 0

@cocotb.test()
async def test_timer(dut):
    dut.wb_addr.value = 0x10003000
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1
    dut.wb_we.value = 0
    dut.wb_sel.value = 0b1111
    dut.wb_dat_m2s.value = 0

    dut.ram_dat_s2m.value = 0
    dut.ram_ack.value = 0
    dut.uart_dat_s2m.value = 0
    dut.uart_ack.value = 0
    dut.gpio_dat_s2m.value = 0
    dut.gpio_ack.value = 0
    dut.pwm_dat_s2m.value = 0
    dut.pwm_ack.value = 0
    dut.timer_dat_s2m.value = 0
    dut.timer_ack.value = 0
    
    await Timer(1,unit ="ns")

    assert dut.ram_stb.value == 0
    assert dut.uart_stb.value == 0
    assert dut.gpio_stb.value == 0
    assert dut.pwm_stb.value == 0
    assert dut.timer_stb.value == 1


@cocotb.test()
async def no_select (dut):
    dut.wb_addr.value = 0x50002000
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1
    dut.wb_we.value = 0
    dut.wb_sel.value = 0b1111
    dut.wb_dat_m2s.value = 0

    dut.ram_dat_s2m.value = 0
    dut.ram_ack.value = 0
    dut.uart_dat_s2m.value = 0
    dut.uart_ack.value = 0
    dut.gpio_dat_s2m.value = 0
    dut.gpio_ack.value = 0
    dut.pwm_dat_s2m.value = 0
    dut.pwm_ack.value = 0
    dut.timer_dat_s2m.value = 0
    dut.timer_ack.value = 0

    await Timer(1, unit="ns")

    assert dut.ram_stb.value == 0
    assert dut.uart_stb.value == 0
    assert dut.gpio_stb.value == 0
    assert dut.pwm_stb.value == 0
    assert dut.timer_stb.value == 0

@cocotb.test()
async def return_data_mux_test(dut):
    dut.wb_addr.value = 0x00000000
    dut.wb_cyc.value = 1
    dut.wb_stb.value = 1
    dut.wb_we.value = 0
    dut.wb_sel.value = 0b1111
    dut.wb_dat_m2s.value = 0

    dut.ram_dat_s2m.value = 0xDEADBEEF
    dut.ram_ack.value = 0
    dut.uart_dat_s2m.value = 0
    dut.uart_ack.value = 0
    dut.gpio_dat_s2m.value = 0
    dut.gpio_ack.value = 0
    dut.pwm_dat_s2m.value = 0
    dut.pwm_ack.value = 0
    dut.timer_dat_s2m.value = 0
    dut.timer_ack.value = 0

    await Timer(1, unit="ns")

    assert dut.ram_stb.value == 1
    assert dut.uart_stb.value == 0
    assert dut.gpio_stb.value == 0
    assert dut.pwm_stb.value == 0
    assert dut.timer_stb.value == 0
    assert dut.wb_dat_s2m.value == 0xDEADBEEF