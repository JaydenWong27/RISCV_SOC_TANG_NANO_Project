import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_write_read(dut):
 # start the clock, 10ns period = 100MHz
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
  # reset first, always reset before testing
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0

    # write 99 into register x1
    dut.rd_addr.value = 1
    dut.rd_data.value = 99
    dut.rd_we.value = 1
    await RisingEdge(dut.clk)

    # stop writing
    dut.rd_we.value = 0

    #reading it back
    dut.rs1_addr.value = 1
    await RisingEdge(dut.clk) # wait one cycle for read to settle

    assert dut.rs1_data.value == 99, f"got {dut.rs1_data.value}"

@cocotb.test()
async def test_writeto0(dut):
    cocotb.start_soon(Clock(dut.clk,10, units="ns").start())

    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0

    dut.rd_addr.value = 0
    dut.rd_data.value = 98
    dut.rd_we.value = 1
    await RisingEdge(dut.clk)

    dut.rd_we.value = 0

    dut.rs1_addr.value = 0
    await RisingEdge(dut.clk)

    assert dut.rs1_data.value == 0, f"got {dut.rs1_data.value}"

@cocotb.test()
async def test_reset(dut):
    cocotb.start_soon(Clock(dut.clk,10, units="ns").start())

    dut.rst.value = 1
    await RisingEdge(dut.clk)
    dut.rst.value = 0

    dut.rd_addr.value = 2
    dut.rd_data.value = 97
    dut.rd_we.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk) # wait one cycle for read to settle

    dut.rd_we.value = 0

    dut.rs1_addr.value = 2
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk) # wait one cycle for read to settle

    dut.rst.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk) # wait one cycle for read to settle
    dut.rst.value = 0

    assert dut.rs1_data.value == 0, f"got {dut.rs1_data.value}"