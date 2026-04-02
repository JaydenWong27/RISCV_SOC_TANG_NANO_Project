import cocotb
from cocotb.triggers import Timer

# ── encoding helpers ──────────────────────────────────────────────────────────
# Use these to compute/verify any instruction hex yourself.
# Pass your register numbers and immediates; the function returns the 32-bit word.

def r_type(funct7, rs2, rs1, funct3, rd):
    return (funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | 0x33

def i_alu(imm, rs1, funct3, rd):
    return ((imm & 0xFFF) << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | 0x13

def i_load(imm, rs1, funct3, rd):
    return ((imm & 0xFFF) << 20) | (rs1 << 15) | (funct3 << 12) | (rd << 7) | 0x03

def i_jalr(imm, rs1, rd):
    return ((imm & 0xFFF) << 20) | (rs1 << 15) | (rd << 7) | 0x67

def s_type(imm, rs2, rs1, funct3):
    return (((imm >> 5) & 0x7F) << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | ((imm & 0x1F) << 7) | 0x23

def b_type(imm, rs2, rs1, funct3):
    return (((imm >> 12) & 1) << 31) | (((imm >> 5) & 0x3F) << 25) | \
           (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | \
           (((imm >> 1) & 0xF) << 8) | (((imm >> 11) & 1) << 7) | 0x63

def j_type(imm, rd):
    return (((imm >> 20) & 1) << 31) | (((imm >> 1) & 0x3FF) << 21) | \
           (((imm >> 11) & 1) << 20) | (((imm >> 12) & 0xFF) << 12) | \
           (rd << 7) | 0x6F

def u_type(imm, rd, opcode):
    return (imm & 0xFFFFF000) | (rd << 7) | opcode


# R-type tests (opcode 0110011)
# All use: rd=x1, rs1=x2, rs2=x3
# alu_op codes match rv32i_decode.v:
#   0000=ADD, 0001=SUB, 0010=AND, 0011=OR, 0100=XOR
#   0101=SLL, 0110=SRL, 0111=SRA, 1000=SLT, 1001=SLTU

@cocotb.test()
async def test_r_add(dut):
    # ADD x1, x2, x3  >  r_type(0x00, 3, 2, 0b000, 1) = 0x003100B3
    dut.instr.value = 0x003100B3
    await Timer(1, unit="ns")
    assert dut.rd.value == 1
    assert dut.rs1.value == 2
    assert dut.rs2.value == 3
    assert dut.imm.value == 0
    assert dut.alu_op.value == 0b0000   # ADD
    assert dut.reg_write.value == 1
    assert dut.mem_read.value == 0
    assert dut.mem_write.value == 0
    assert dut.branch.value == 0
    assert dut.jump.value == 0
    assert dut.mem_to_reg.value == 0

@cocotb.test()
async def test_r_sub(dut):
    # SUB x1, x2, x3 to r_type(0x20, 3, 2, 0b000, 1) = 0x403100B3
    dut.instr.value = 0x403100B3
    await Timer(1, unit="ns")
    assert dut.rd.value == 1
    assert dut.rs1.value == 2
    assert dut.rs2.value == 3
    assert dut.imm.value == 0
    assert dut.alu_op.value == 0b0001   # SUB  (funct7[5]=1 -> subtract)
    assert dut.reg_write.value == 1
    assert dut.mem_read.value == 0
    assert dut.mem_write.value == 0
    assert dut.branch.value == 0
    assert dut.jump.value == 0
    assert dut.mem_to_reg.value == 0

@cocotb.test()
async def test_r_and(dut):
    # AND x1, x2, x3  -> r_type(0x00, 3, 2, 0b111, 1) = 0x003170B3
    dut.instr.value = 0x003170B3
    await Timer(1, unit="ns")
    assert dut.rd.value == 1
    assert dut.rs1.value == 2
    assert dut.rs2.value == 3
    assert dut.imm.value == 0
    assert dut.alu_op.value == 0b0010   # AND
    assert dut.reg_write.value == 1
    assert dut.mem_read.value == 0
    assert dut.mem_write.value == 0

@cocotb.test()
async def test_r_or(dut):
    # OR x1, x2, x3  →  r_type(0x00, 3, 2, 0b110, 1) = 0x003160B3
    dut.instr.value = 0x003160B3
    await Timer(1, unit="ns")
    assert dut.rd.value == 1
    assert dut.rs1.value == 2
    assert dut.rs2.value == 3
    assert dut.imm.value == 0
    assert dut.alu_op.value == 0b0011   # OR
    assert dut.reg_write.value == 1

@cocotb.test()
async def test_r_xor(dut):
    # XOR x1, x2, x3  →  r_type(0x00, 3, 2, 0b100, 1) = 0x003140B3
    dut.instr.value = 0x003140B3
    await Timer(1, unit="ns")
    assert dut.rd.value == 1
    assert dut.rs1.value == 2
    assert dut.rs2.value == 3
    assert dut.alu_op.value == 0b0100   # XOR
    assert dut.reg_write.value == 1

@cocotb.test()
async def test_r_sll(dut):
    # SLL x1, x2, x3  →  r_type(0x00, 3, 2, 0b001, 1) = 0x003110B3
    dut.instr.value = 0x003110B3
    await Timer(1, unit="ns")
    assert dut.rd.value == 1
    assert dut.rs1.value == 2
    assert dut.rs2.value == 3
    assert dut.alu_op.value == 0b0101   # SLL
    assert dut.reg_write.value == 1

@cocotb.test()
async def test_r_srl(dut):
    # SRL x1, x2, x3  →  r_type(0x00, 3, 2, 0b101, 1) = 0x003150B3
    dut.instr.value = 0x003150B3
    await Timer(1, unit="ns")
    assert dut.rd.value == 1
    assert dut.rs1.value == 2
    assert dut.rs2.value == 3
    assert dut.alu_op.value == 0b0110   # SRL  (funct7[5]=0)
    assert dut.reg_write.value == 1

@cocotb.test()
async def test_r_sra(dut):
    # SRA x1, x2, x3  →  r_type(0x20, 3, 2, 0b101, 1) = 0x403150B3
    # Same funct3 as SRL but funct7[5]=1 → arithmetic shift
    dut.instr.value = 0x403150B3
    await Timer(1, unit="ns")
    assert dut.rd.value == 1
    assert dut.rs1.value == 2
    assert dut.rs2.value == 3
    assert dut.alu_op.value == 0b0111   # SRA  (funct7[5]=1)
    assert dut.reg_write.value == 1

@cocotb.test()
async def test_r_slt(dut):
    # SLT x1, x2, x3  →  r_type(0x00, 3, 2, 0b010, 1) = 0x003120B3
    dut.instr.value = 0x003120B3
    await Timer(1, unit="ns")
    assert dut.rd.value == 1
    assert dut.rs1.value == 2
    assert dut.rs2.value == 3
    assert dut.alu_op.value == 0b1000   # SLT
    assert dut.reg_write.value == 1

@cocotb.test()
async def test_r_sltu(dut):
    # SLTU x1, x2, x3  →  r_type(0x00, 3, 2, 0b011, 1) = 0x003130B3
    dut.instr.value = 0x003130B3
    await Timer(1, unit="ns")
    assert dut.rd.value == 1
    assert dut.rs1.value == 2
    assert dut.rs2.value == 3
    assert dut.alu_op.value == 0b1001   # SLTU
    assert dut.reg_write.value == 1


# ── I-type ALU tests (opcode 0010011) ─────────────────────────────────────────
# All use: rd=x1, rs1=x2

@cocotb.test()
async def test_addi(dut):
    # ADDI x1, x2, 5  →  i_alu(5, 2, 0b000, 1) = 0x00510093
    dut.instr.value = 0x00510093
    await Timer(1, unit="ns")
    assert dut.rd.value == 1
    assert dut.rs1.value == 2
    assert dut.imm.value == 5
    assert dut.alu_op.value == 0b0000   # ADD
    assert dut.reg_write.value == 1
    assert dut.mem_read.value == 0
    assert dut.mem_write.value == 0
    assert dut.branch.value == 0
    assert dut.jump.value == 0
    assert dut.mem_to_reg.value == 0

@cocotb.test()
async def test_slti(dut):
    # SLTI x1, x2, 10  →  i_alu(10, 2, 0b010, 1) = 0x00A12093
    dut.instr.value = 0x00A12093
    await Timer(1, unit="ns")
    assert dut.rd.value == 1
    assert dut.rs1.value == 2
    assert dut.imm.value == 10
    assert dut.alu_op.value == 0b1000   # SLT
    assert dut.reg_write.value == 1

@cocotb.test()
async def test_sltiu(dut):
    # SLTIU x1, x2, 10  →  i_alu(10, 2, 0b011, 1) = 0x00A13093
    dut.instr.value = 0x00A13093
    await Timer(1, unit="ns")
    assert dut.rd.value      == 1
    assert dut.rs1.value     == 2
    assert dut.imm.value     == 10
    assert dut.alu_op.value  == 0b1001   # SLTU
    assert dut.reg_write.value  == 1

@cocotb.test()
async def test_xori(dut):
    # XORI x1, x2, 10  →  i_alu(10, 2, 0b100, 1) = 0x00A14093
    dut.instr.value = 0x00A14093
    await Timer(1, unit="ns")
    assert dut.rd.value      == 1
    assert dut.rs1.value     == 2
    assert dut.imm.value     == 10
    assert dut.alu_op.value  == 0b0100   # XOR
    assert dut.reg_write.value  == 1

@cocotb.test()
async def test_ori(dut):
    # ORI x1, x2, 10  →  i_alu(10, 2, 0b110, 1) = 0x00A16093
    dut.instr.value = 0x00A16093
    await Timer(1, unit="ns")
    assert dut.rd.value      == 1
    assert dut.rs1.value     == 2
    assert dut.imm.value     == 10
    assert dut.alu_op.value  == 0b0011   # OR
    assert dut.reg_write.value  == 1

@cocotb.test()
async def test_andi(dut):
    # ANDI x1, x2, 10  →  i_alu(10, 2, 0b111, 1) = 0x00A17093
    dut.instr.value = 0x00A17093
    await Timer(1, unit="ns")
    assert dut.rd.value      == 1
    assert dut.rs1.value     == 2
    assert dut.imm.value     == 10
    assert dut.alu_op.value  == 0b0010   # AND
    assert dut.reg_write.value  == 1

@cocotb.test()
async def test_slli(dut):
    # SLLI x1, x2, 2  →  i_alu(2, 2, 0b001, 1) = 0x00211093
    # For shifts, imm[4:0] = shamt, imm[11:5] = funct7 (0 for SLLI)
    dut.instr.value = 0x00211093
    await Timer(1, unit="ns")
    assert dut.rd.value      == 1
    assert dut.rs1.value     == 2
    assert dut.imm.value     == 2        # shamt=2
    assert dut.alu_op.value  == 0b0101   # SLL
    assert dut.reg_write.value  == 1

@cocotb.test()
async def test_srli(dut):
    # SRLI x1, x2, 2  →  i_alu(2, 2, 0b101, 1) = 0x00215093
    dut.instr.value = 0x00215093
    await Timer(1, unit="ns")
    assert dut.rd.value      == 1
    assert dut.rs1.value     == 2
    assert dut.imm.value     == 2
    assert dut.alu_op.value  == 0b0110   # SRL  (funct7[5]=0)
    assert dut.reg_write.value  == 1

@cocotb.test()
async def test_srai(dut):
    # SRAI x1, x2, 2  →  funct7=0x20 in upper bits = 0x40215093
    # imm bits[31:25]=0100000 (marks arithmetic), bits[24:20]=shamt=2
    dut.instr.value = 0x40215093
    await Timer(1, unit="ns")
    assert dut.rs1.value     == 2
    assert dut.rd.value      == 1
    assert dut.alu_op.value  == 0b0111   # SRA  (funct7[5]=1)
    assert dut.reg_write.value  == 1

@cocotb.test()
async def test_addi_negative(dut):
    # ADDI x1, x2, -1  →  i_alu(-1, 2, 0b000, 1) = 0xFFF10093
    # Tests sign-extension: the decoder must output 0xFFFFFFFF for imm
    dut.instr.value = 0xFFF10093
    await Timer(1, unit="ns")
    assert dut.rd.value      == 1
    assert dut.rs1.value     == 2
    assert dut.imm.value     == 0xFFFFFFFF   # -1 sign-extended to 32 bits
    assert dut.alu_op.value  == 0b0000
    assert dut.reg_write.value  == 1


# ── Load test (opcode 0000011) ────────────────────────────────────────────────

@cocotb.test()
async def test_lw(dut):
    # LW x1, 8(x2)  →  i_load(8, 2, 0b010, 1) = 0x00812083
    dut.instr.value = 0x00812083
    await Timer(1, unit="ns")
    assert dut.rd.value      == 1
    assert dut.rs1.value     == 2
    assert dut.imm.value     == 8
    assert dut.reg_write.value  == 1
    assert dut.mem_read.value   == 1    # ← load flag
    assert dut.mem_to_reg.value == 1    # ← write mem data to rd
    assert dut.mem_write.value  == 0
    assert dut.branch.value     == 0
    assert dut.jump.value       == 0


# ── Store test (opcode 0100011) ───────────────────────────────────────────────

@cocotb.test()
async def test_sw(dut):
    # SW x3, 8(x2)  →  s_type(8, 3, 2, 0b010) = 0x00312423
    # S-type splits imm across two fields: imm[11:5] in bits[31:25], imm[4:0] in bits[11:7]
    dut.instr.value = 0x00312423
    await Timer(1, unit="ns")
    assert dut.rs1.value     == 2       # base address register
    assert dut.rs2.value     == 3       # data register being stored
    assert dut.imm.value     == 8       # offset
    assert dut.mem_write.value  == 1    # ← store flag
    assert dut.reg_write.value  == 0    # stores don't write a register
    assert dut.mem_read.value   == 0
    assert dut.branch.value     == 0
    assert dut.jump.value       == 0


# ── Branch test (opcode 1100011) ──────────────────────────────────────────────

@cocotb.test()
async def test_beq(dut):
    # BEQ x1, x2, 8  →  b_type(8, 2, 1, 0b000) = 0x00208463
    # B-type has the trickiest immediate: scrambled across 4 fields
    dut.instr.value = 0x00208463
    await Timer(1, unit="ns")
    assert dut.rs1.value     == 1
    assert dut.rs2.value     == 2
    assert dut.imm.value     == 8       # branch offset (byte-addressed)
    assert dut.branch.value     == 1    # ← branch flag
    assert dut.alu_op.value  == 0b0001  # decoder uses SUB to compare
    assert dut.reg_write.value  == 0
    assert dut.mem_read.value   == 0
    assert dut.mem_write.value  == 0
    assert dut.jump.value       == 0


# ── JAL test (opcode 1101111) ─────────────────────────────────────────────────

@cocotb.test()
async def test_jal(dut):
    # JAL x1, 16  →  j_type(16, 1) = 0x010000EF
    # J-type: also a scrambled immediate (20-bit offset)
    dut.instr.value = 0x010000EF
    await Timer(1, unit="ns")
    assert dut.rd.value      == 1
    assert dut.imm.value     == 16
    assert dut.jump.value       == 1    # ← jump flag
    assert dut.reg_write.value  == 1    # saves return address in rd
    assert dut.mem_read.value   == 0
    assert dut.mem_write.value  == 0
    assert dut.branch.value     == 0


# ── JALR test (opcode 1100111) ────────────────────────────────────────────────

@cocotb.test()
async def test_jalr(dut):
    # JALR x1, 4(x2)  →  i_jalr(4, 2, 1) = 0x004100E7
    # Like JAL but uses I-type immediate (register + offset)
    dut.instr.value = 0x004100E7
    await Timer(1, unit="ns")
    assert dut.rd.value      == 1
    assert dut.rs1.value     == 2
    assert dut.imm.value     == 4
    assert dut.jump.value       == 1
    assert dut.reg_write.value  == 1
    assert dut.mem_read.value   == 0
    assert dut.mem_write.value  == 0
    assert dut.branch.value     == 0


# ── LUI test (opcode 0110111) ─────────────────────────────────────────────────

@cocotb.test()
async def test_lui(dut):
    # LUI x1, 0x12345  →  u_type(0x12345000, 1, 0x37) = 0x123450B7
    # U-type: upper 20 bits become imm[31:12], lower 12 are zero
    dut.instr.value = 0x123450B7
    await Timer(1, unit="ns")
    assert dut.rd.value      == 1
    assert dut.imm.value     == 0x12345000   # lower 12 bits are 0
    assert dut.reg_write.value  == 1
    assert dut.mem_read.value   == 0
    assert dut.mem_write.value  == 0
    assert dut.branch.value     == 0
    assert dut.jump.value       == 0


# ── AUIPC test (opcode 0010111) ───────────────────────────────────────────────

@cocotb.test()
async def test_auipc(dut):
    # AUIPC x1, 0x12345  →  u_type(0x12345000, 1, 0x17) = 0x12345097
    # Same U-type encoding as LUI, different opcode
    dut.instr.value = 0x12345097
    await Timer(1, unit="ns")
    assert dut.rd.value      == 1
    assert dut.imm.value     == 0x12345000
    assert dut.reg_write.value  == 1
    assert dut.mem_read.value   == 0
    assert dut.mem_write.value  == 0
    assert dut.branch.value     == 0
    assert dut.jump.value       == 0
