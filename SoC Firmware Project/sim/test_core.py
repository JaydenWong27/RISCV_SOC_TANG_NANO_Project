import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

# Helper: tick the clock and wait for falling edge so signals settle
async def tick(dut):
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)  # signals are stable here

# Helper: reset the core for 2 cycles then release
async def reset(dut):
    dut.rst.value = 1
    dut.instr_data.value = 0x00000013  # feed NOPs during reset
    dut.wb_dat_s2m.value = 0
    dut.wb_ack.value = 0
    dut.instr_ack.value = 1
    await tick(dut)
    await tick(dut)
    dut.rst.value = 0


@cocotb.test()
async def test_pc_increments(dut):
    """
    Most basic test: after reset, the PC should increment by 4
    every clock cycle when there are no hazards.

    The core sends instr_addr = pc to instruction memory.
    We check that it counts 0 → 4 → 8 → 12.
    """
    # Start the clock: 10ns period
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await reset(dut)

    # After reset PC = 0, so instr_addr should be 0
    assert dut.instr_addr.value == 0, f"Expected 0, got {dut.instr_addr.value}"

    # Tick once → PC should become 4
    dut.instr_data.value = 0x00000013  # feed NOP each cycle
    await tick(dut)
    assert dut.instr_addr.value == 4, f"Expected 4, got {dut.instr_addr.value}"

    # Tick again → PC should become 8
    await tick(dut)
    assert dut.instr_addr.value == 8, f"Expected 8, got {dut.instr_addr.value}"

    # Tick again → PC should become 12
    await tick(dut)
    assert dut.instr_addr.value == 12, f"Expected 12, got {dut.instr_addr.value}"


@cocotb.test()
async def test_addi_writes_register(dut):
    """
    Feed ADDI x1, x0, 5 into the pipeline and check that after
    enough cycles the result (5) ends up written to the regfile.

    ADDI x1, x0, 5 = 0x00500093
    x0 is always 0, so result = 0 + 5 = 5
    After 5 pipeline stages, the result should be in x1.

    We verify indirectly: feed a second instruction that reads x1
    (ADD x2, x1, x0 = 0x00108133) and check that the regfile
    gets written correctly by watching wb_rd and wb_rd_data
    (the writeback wires).
    """
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    await reset(dut)

    # Cycle 1: feed ADDI x1, x0, 5
    dut.instr_data.value = 0x00500093  # ADDI x1, x0, 5
    dut.instr_ack.value = 1
    await tick(dut)

    # Cycles 2-4: feed NOPs to push ADDI to writeback
    # 3 NOPs = 3 more cycles → ADDI reaches WB on cycle 4
    dut.instr_data.value = 0x00000013  # NOP
    for _ in range(3):
        await tick(dut)

    # By now the ADDI should have reached writeback
    # wb_rd should be 1 (x1) and wb_rd_data should be 5
    assert dut.wb_rd.value == 1, \
        f"Expected rd=1, got {dut.wb_rd.value}"
    assert dut.wb_rd_data.value == 5, \
        f"Expected rd_data=5, got {dut.wb_rd_data.value}"


@cocotb.test()
async def test_add_two_registers(dut):
    cocotb.start_soon(Clock(dut.clk, 10 , units ="ns").start())
    await reset (dut)

    #cycle 1: add two register
    dut.instr_data.value = 0x003100B3
    dut.instr_ack.value = 1
    await tick(dut)

    #Cycles 2-4: #feed NOP's to push ADD to writeback
    #3 NOPs = 3 more cycles to ADD reahces WB on cycle

    dut.instr_data.value = 0x00000013 
    for _ in range (3):
        await tick(dut)

    assert dut.wb_rd.value  == 1, \
        f"Expected rd = 1 , got {dut.wb_rd.value}"
    
    assert dut.wb_rd_data.value == 0, \
        f"Expected rd_data = 5, got {dut.wb_rd_data.value}"


@cocotb.test()
async def test_load_stall(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await reset(dut)

    # Cycle 1: LW enters IF
    dut.instr_data.value = 0x00002083  # LW x1, 0(x0)
    await tick(dut)

    # Cycle 2: LW in ID, ADD enters IF, no stall yet, LW not in EX yet
    dut.instr_data.value = 0x00008133  # ADD x2, x1, x0
    await tick(dut)

    # Cycle 3: LW now in EX, ADD in ID, hazard fires HERE
    # Record PC before this tick, it should NOT change
    pc_before = int(dut.instr_addr.value)
    dut.instr_data.value = 0x00000013  # NOP
    await tick(dut)

    pc_after = int(dut.instr_addr.value)
    assert pc_after == pc_before, \
        f"expected stall (pc frozen), but pc moved from {pc_before} to {pc_after}"


@cocotb.test()
async def test_branch_taken(dut):
    """
    Feed ADDI x1, x0, 0 then BEQ x1, x0, 8.
    x1 == x0 (both 0) so the branch is taken.
    PC should jump to (branch_PC + 8) instead of continuing +4.

    Sequence:
      Cycle 1: ADDI x1, x0, 0  → x1 = 0  (same as x0)
      Cycle 2: BEQ x1, x0, 8   → branch condition is true
      Cycles 3-4: NOPs in pipeline behind the branch

    BEQ enters EX on cycle 3 — that's when alu_zero fires and
    hazard_branch_taken goes high, flushing IF/ID and jumping PC.

    BEQ was fetched at PC=4, so branch target = 4 + 8 = 12.
    After the jump, instr_addr should be 12, not 8.
    """
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    await reset(dut)

    # Cycle 1: ADDI x1, x0, 0,  x1 = 0
    # i_alu(0, 0, 0b000, 1) = 0x00000093
    dut.instr_data.value = 0x00000093
    await tick(dut)

    # Cycle 2: BEQ x1, x0, 8,  b_type(8, 0, 1, 0b000) = 0x00008463
    # BEQ fetched at PC=4, so target = 4 + 8 = 12
    dut.instr_data.value = 0x00008463
    await tick(dut)

    # Cycle 3: BEQ reaches EX, alu_zero fires, branch taken
    # PC should jump to 12
    dut.instr_data.value = 0x00000013  # NOP
    await tick(dut)

    # After the jump, instr_addr should be 12
    assert int(dut.instr_addr.value) == 12, \
        f"Expected PC=12 after branch, got {int(dut.instr_addr.value)}"
