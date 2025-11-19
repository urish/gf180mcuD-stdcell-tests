"""
Comprehensive Standard Cell Unknown State Test Bench

Tests all gf180mcu standard cells with unknown ('x') states to verify proper
unknown value propagation according to these rules:
- x | 1 == 1  (OR with 1 is always 1)
- x & 0 == 0  (AND with 0 is always 0)
- x | 0 == x  (result is unknown)
- x & 1 == x  (result is unknown)

Gate types tested:
- AND gates: and2_1, and3_1, and4_1
- OR gates: or2_1, or3_1, or4_1
- NAND gates: nand2_1, nand3_1, nand4_1
- NOR gates: nor2_1, nor3_1, nor4_1
- XOR/XNOR gates: xor2_1, xor3_1, xnor2_1
- Inverter: clkinv_1
- Multiplexer: mux2_2
- AOI gates: aoi21_1, aoi22_1, aoi211_1, aoi221_1, aoi222_1
- OAI gates: oai21_1, oai22_1, oai211_1, oai221_1, oai222_1, oai31_1, oai32_1
"""

import cocotb
from cocotb.triggers import Timer

# Helper function for output checking
async def check_output(dut, signal_dict, expected, output_signal, description):
    """
    Set inputs and check output.
    signal_dict: {signal_name: value} dictionary of inputs to set
    expected: expected output value (0, 1, or 'x')
    output_signal: the output signal to check
    description: test description
    """
    for signal_name, value in signal_dict.items():
        getattr(dut, signal_name).value = value

    await Timer(10, unit="ns")
    actual = output_signal.value

    if expected == 'x':
        assert actual.is_resolvable == False, \
            f"{description}: Expected unknown, got {actual}"
    else:
        assert actual == expected, \
            f"{description}: Expected {expected}, got {actual}"

# ============================================================================
# AND Gates Tests
# ============================================================================

@cocotb.test()
async def test_and2_1(dut):
    """Test AND2 gate: Z = A1 & A2"""
    dut._log.info("Testing AND2 gate...")

    # Known inputs
    await check_output(dut, {'and2_a1': 0, 'and2_a2': 0}, 0, dut.and2_z, "AND2: 0 & 0")
    await check_output(dut, {'and2_a1': 0, 'and2_a2': 1}, 0, dut.and2_z, "AND2: 0 & 1")
    await check_output(dut, {'and2_a1': 1, 'and2_a2': 0}, 0, dut.and2_z, "AND2: 1 & 0")
    await check_output(dut, {'and2_a1': 1, 'and2_a2': 1}, 1, dut.and2_z, "AND2: 1 & 1")

    # Unknown inputs - deterministic cases (x & 0 = 0)
    await check_output(dut, {'and2_a1': 'x', 'and2_a2': 0}, 0, dut.and2_z, "AND2: x & 0")
    await check_output(dut, {'and2_a1': 0, 'and2_a2': 'x'}, 0, dut.and2_z, "AND2: 0 & x")

    # Unknown inputs - unknown result (x & 1 = x)
    await check_output(dut, {'and2_a1': 'x', 'and2_a2': 1}, 'x', dut.and2_z, "AND2: x & 1")
    await check_output(dut, {'and2_a1': 1, 'and2_a2': 'x'}, 'x', dut.and2_z, "AND2: 1 & x")
    await check_output(dut, {'and2_a1': 'x', 'and2_a2': 'x'}, 'x', dut.and2_z, "AND2: x & x")

@cocotb.test()
async def test_and3_1(dut):
    """Test AND3 gate: Z = A1 & A2 & A3"""
    dut._log.info("Testing AND3 gate...")

    # Known inputs
    await check_output(dut, {'and3_a1': 1, 'and3_a2': 1, 'and3_a3': 1}, 1, dut.and3_z, "AND3: 1 & 1 & 1")
    await check_output(dut, {'and3_a1': 1, 'and3_a2': 1, 'and3_a3': 0}, 0, dut.and3_z, "AND3: 1 & 1 & 0")

    # Unknown inputs - deterministic (any 0 makes output 0)
    await check_output(dut, {'and3_a1': 0, 'and3_a2': 'x', 'and3_a3': 'x'}, 0, dut.and3_z, "AND3: 0 & x & x")
    await check_output(dut, {'and3_a1': 'x', 'and3_a2': 0, 'and3_a3': 'x'}, 0, dut.and3_z, "AND3: x & 0 & x")
    await check_output(dut, {'and3_a1': 'x', 'and3_a2': 'x', 'and3_a3': 0}, 0, dut.and3_z, "AND3: x & x & 0")

    # Unknown inputs - unknown result
    await check_output(dut, {'and3_a1': 1, 'and3_a2': 1, 'and3_a3': 'x'}, 'x', dut.and3_z, "AND3: 1 & 1 & x")
    await check_output(dut, {'and3_a1': 'x', 'and3_a2': 'x', 'and3_a3': 'x'}, 'x', dut.and3_z, "AND3: x & x & x")

@cocotb.test()
async def test_and4_1(dut):
    """Test AND4 gate: Z = A1 & A2 & A3 & A4"""
    dut._log.info("Testing AND4 gate...")

    # Known inputs
    await check_output(dut, {'and4_a1': 1, 'and4_a2': 1, 'and4_a3': 1, 'and4_a4': 1}, 1, dut.and4_z, "AND4: all 1s")

    # Unknown inputs - deterministic
    await check_output(dut, {'and4_a1': 0, 'and4_a2': 'x', 'and4_a3': 'x', 'and4_a4': 'x'}, 0, dut.and4_z, "AND4: 0 & x & x & x")

    # Unknown inputs - unknown result
    await check_output(dut, {'and4_a1': 1, 'and4_a2': 1, 'and4_a3': 1, 'and4_a4': 'x'}, 'x', dut.and4_z, "AND4: 1 & 1 & 1 & x")

# ============================================================================
# OR Gates Tests
# ============================================================================

@cocotb.test()
async def test_or2_1(dut):
    """Test OR2 gate: Z = A1 | A2"""
    dut._log.info("Testing OR2 gate...")

    # Known inputs
    await check_output(dut, {'or2_a1': 0, 'or2_a2': 0}, 0, dut.or2_z, "OR2: 0 | 0")
    await check_output(dut, {'or2_a1': 0, 'or2_a2': 1}, 1, dut.or2_z, "OR2: 0 | 1")
    await check_output(dut, {'or2_a1': 1, 'or2_a2': 0}, 1, dut.or2_z, "OR2: 1 | 0")
    await check_output(dut, {'or2_a1': 1, 'or2_a2': 1}, 1, dut.or2_z, "OR2: 1 | 1")

    # Unknown inputs - deterministic cases (x | 1 = 1)
    await check_output(dut, {'or2_a1': 'x', 'or2_a2': 1}, 1, dut.or2_z, "OR2: x | 1")
    await check_output(dut, {'or2_a1': 1, 'or2_a2': 'x'}, 1, dut.or2_z, "OR2: 1 | x")

    # Unknown inputs - unknown result (x | 0 = x)
    await check_output(dut, {'or2_a1': 'x', 'or2_a2': 0}, 'x', dut.or2_z, "OR2: x | 0")
    await check_output(dut, {'or2_a1': 0, 'or2_a2': 'x'}, 'x', dut.or2_z, "OR2: 0 | x")
    await check_output(dut, {'or2_a1': 'x', 'or2_a2': 'x'}, 'x', dut.or2_z, "OR2: x | x")

@cocotb.test()
async def test_or3_1(dut):
    """Test OR3 gate: Z = A1 | A2 | A3"""
    dut._log.info("Testing OR3 gate...")

    # Known inputs
    await check_output(dut, {'or3_a1': 0, 'or3_a2': 0, 'or3_a3': 0}, 0, dut.or3_z, "OR3: 0 | 0 | 0")
    await check_output(dut, {'or3_a1': 0, 'or3_a2': 0, 'or3_a3': 1}, 1, dut.or3_z, "OR3: 0 | 0 | 1")

    # Unknown inputs - deterministic (any 1 makes output 1)
    await check_output(dut, {'or3_a1': 1, 'or3_a2': 'x', 'or3_a3': 'x'}, 1, dut.or3_z, "OR3: 1 | x | x")
    await check_output(dut, {'or3_a1': 'x', 'or3_a2': 1, 'or3_a3': 'x'}, 1, dut.or3_z, "OR3: x | 1 | x")
    await check_output(dut, {'or3_a1': 'x', 'or3_a2': 'x', 'or3_a3': 1}, 1, dut.or3_z, "OR3: x | x | 1")

    # Unknown inputs - unknown result
    await check_output(dut, {'or3_a1': 0, 'or3_a2': 0, 'or3_a3': 'x'}, 'x', dut.or3_z, "OR3: 0 | 0 | x")
    await check_output(dut, {'or3_a1': 'x', 'or3_a2': 'x', 'or3_a3': 'x'}, 'x', dut.or3_z, "OR3: x | x | x")

@cocotb.test()
async def test_or4_1(dut):
    """Test OR4 gate: Z = A1 | A2 | A3 | A4"""
    dut._log.info("Testing OR4 gate...")

    # Known inputs
    await check_output(dut, {'or4_a1': 0, 'or4_a2': 0, 'or4_a3': 0, 'or4_a4': 0}, 0, dut.or4_z, "OR4: all 0s")

    # Unknown inputs - deterministic
    await check_output(dut, {'or4_a1': 1, 'or4_a2': 'x', 'or4_a3': 'x', 'or4_a4': 'x'}, 1, dut.or4_z, "OR4: 1 | x | x | x")

    # Unknown inputs - unknown result
    await check_output(dut, {'or4_a1': 0, 'or4_a2': 0, 'or4_a3': 0, 'or4_a4': 'x'}, 'x', dut.or4_z, "OR4: 0 | 0 | 0 | x")

# ============================================================================
# NAND Gates Tests
# ============================================================================

@cocotb.test()
async def test_nand2_1(dut):
    """Test NAND2 gate: ZN = !(A1 & A2)"""
    dut._log.info("Testing NAND2 gate...")

    # Known inputs
    await check_output(dut, {'nand2_a1': 0, 'nand2_a2': 0}, 1, dut.nand2_zn, "NAND2: !(0 & 0)")
    await check_output(dut, {'nand2_a1': 0, 'nand2_a2': 1}, 1, dut.nand2_zn, "NAND2: !(0 & 1)")
    await check_output(dut, {'nand2_a1': 1, 'nand2_a2': 0}, 1, dut.nand2_zn, "NAND2: !(1 & 0)")
    await check_output(dut, {'nand2_a1': 1, 'nand2_a2': 1}, 0, dut.nand2_zn, "NAND2: !(1 & 1)")

    # Unknown inputs - deterministic (0 & x = 0, so !(0 & x) = 1)
    await check_output(dut, {'nand2_a1': 'x', 'nand2_a2': 0}, 1, dut.nand2_zn, "NAND2: !(x & 0)")
    await check_output(dut, {'nand2_a1': 0, 'nand2_a2': 'x'}, 1, dut.nand2_zn, "NAND2: !(0 & x)")

    # Unknown inputs - unknown result
    await check_output(dut, {'nand2_a1': 'x', 'nand2_a2': 1}, 'x', dut.nand2_zn, "NAND2: !(x & 1)")
    await check_output(dut, {'nand2_a1': 1, 'nand2_a2': 'x'}, 'x', dut.nand2_zn, "NAND2: !(1 & x)")
    await check_output(dut, {'nand2_a1': 'x', 'nand2_a2': 'x'}, 'x', dut.nand2_zn, "NAND2: !(x & x)")

@cocotb.test()
async def test_nand3_1(dut):
    """Test NAND3 gate: ZN = !(A1 & A2 & A3)"""
    dut._log.info("Testing NAND3 gate...")

    # Known inputs
    await check_output(dut, {'nand3_a1': 1, 'nand3_a2': 1, 'nand3_a3': 1}, 0, dut.nand3_zn, "NAND3: !(1 & 1 & 1)")

    # Unknown inputs - deterministic
    await check_output(dut, {'nand3_a1': 0, 'nand3_a2': 'x', 'nand3_a3': 'x'}, 1, dut.nand3_zn, "NAND3: !(0 & x & x)")

    # Unknown inputs - unknown result
    await check_output(dut, {'nand3_a1': 1, 'nand3_a2': 1, 'nand3_a3': 'x'}, 'x', dut.nand3_zn, "NAND3: !(1 & 1 & x)")

@cocotb.test()
async def test_nand4_1(dut):
    """Test NAND4 gate: ZN = !(A1 & A2 & A3 & A4)"""
    dut._log.info("Testing NAND4 gate...")

    # Known inputs
    await check_output(dut, {'nand4_a1': 1, 'nand4_a2': 1, 'nand4_a3': 1, 'nand4_a4': 1}, 0, dut.nand4_zn, "NAND4: !(all 1s)")

    # Unknown inputs - deterministic
    await check_output(dut, {'nand4_a1': 0, 'nand4_a2': 'x', 'nand4_a3': 'x', 'nand4_a4': 'x'}, 1, dut.nand4_zn, "NAND4: !(0 & x & x & x)")

    # Unknown inputs - unknown result
    await check_output(dut, {'nand4_a1': 1, 'nand4_a2': 1, 'nand4_a3': 1, 'nand4_a4': 'x'}, 'x', dut.nand4_zn, "NAND4: !(1 & 1 & 1 & x)")

# ============================================================================
# NOR Gates Tests
# ============================================================================

@cocotb.test()
async def test_nor2_1(dut):
    """Test NOR2 gate: ZN = !(A1 | A2)"""
    dut._log.info("Testing NOR2 gate...")

    # Known inputs
    await check_output(dut, {'nor2_a1': 0, 'nor2_a2': 0}, 1, dut.nor2_zn, "NOR2: !(0 | 0)")
    await check_output(dut, {'nor2_a1': 0, 'nor2_a2': 1}, 0, dut.nor2_zn, "NOR2: !(0 | 1)")
    await check_output(dut, {'nor2_a1': 1, 'nor2_a2': 0}, 0, dut.nor2_zn, "NOR2: !(1 | 0)")
    await check_output(dut, {'nor2_a1': 1, 'nor2_a2': 1}, 0, dut.nor2_zn, "NOR2: !(1 | 1)")

    # Unknown inputs - deterministic (1 | x = 1, so !(1 | x) = 0)
    await check_output(dut, {'nor2_a1': 'x', 'nor2_a2': 1}, 0, dut.nor2_zn, "NOR2: !(x | 1)")
    await check_output(dut, {'nor2_a1': 1, 'nor2_a2': 'x'}, 0, dut.nor2_zn, "NOR2: !(1 | x)")

    # Unknown inputs - unknown result
    await check_output(dut, {'nor2_a1': 'x', 'nor2_a2': 0}, 'x', dut.nor2_zn, "NOR2: !(x | 0)")
    await check_output(dut, {'nor2_a1': 0, 'nor2_a2': 'x'}, 'x', dut.nor2_zn, "NOR2: !(0 | x)")
    await check_output(dut, {'nor2_a1': 'x', 'nor2_a2': 'x'}, 'x', dut.nor2_zn, "NOR2: !(x | x)")

@cocotb.test()
async def test_nor3_1(dut):
    """Test NOR3 gate: ZN = !(A1 | A2 | A3)"""
    dut._log.info("Testing NOR3 gate...")

    # Known inputs
    await check_output(dut, {'nor3_a1': 0, 'nor3_a2': 0, 'nor3_a3': 0}, 1, dut.nor3_zn, "NOR3: !(0 | 0 | 0)")

    # Unknown inputs - deterministic
    await check_output(dut, {'nor3_a1': 1, 'nor3_a2': 'x', 'nor3_a3': 'x'}, 0, dut.nor3_zn, "NOR3: !(1 | x | x)")

    # Unknown inputs - unknown result
    await check_output(dut, {'nor3_a1': 0, 'nor3_a2': 0, 'nor3_a3': 'x'}, 'x', dut.nor3_zn, "NOR3: !(0 | 0 | x)")

@cocotb.test()
async def test_nor4_1(dut):
    """Test NOR4 gate: ZN = !(A1 | A2 | A3 | A4)"""
    dut._log.info("Testing NOR4 gate...")

    # Known inputs
    await check_output(dut, {'nor4_a1': 0, 'nor4_a2': 0, 'nor4_a3': 0, 'nor4_a4': 0}, 1, dut.nor4_zn, "NOR4: !(all 0s)")

    # Unknown inputs - deterministic
    await check_output(dut, {'nor4_a1': 1, 'nor4_a2': 'x', 'nor4_a3': 'x', 'nor4_a4': 'x'}, 0, dut.nor4_zn, "NOR4: !(1 | x | x | x)")

    # Unknown inputs - unknown result
    await check_output(dut, {'nor4_a1': 0, 'nor4_a2': 0, 'nor4_a3': 0, 'nor4_a4': 'x'}, 'x', dut.nor4_zn, "NOR4: !(0 | 0 | 0 | x)")

# ============================================================================
# XOR/XNOR Gates Tests
# ============================================================================

@cocotb.test()
async def test_xor2_1(dut):
    """Test XOR2 gate: Z = A1 ^ A2"""
    dut._log.info("Testing XOR2 gate...")

    # Known inputs
    await check_output(dut, {'xor2_a1': 0, 'xor2_a2': 0}, 0, dut.xor2_z, "XOR2: 0 ^ 0")
    await check_output(dut, {'xor2_a1': 0, 'xor2_a2': 1}, 1, dut.xor2_z, "XOR2: 0 ^ 1")
    await check_output(dut, {'xor2_a1': 1, 'xor2_a2': 0}, 1, dut.xor2_z, "XOR2: 1 ^ 0")
    await check_output(dut, {'xor2_a1': 1, 'xor2_a2': 1}, 0, dut.xor2_z, "XOR2: 1 ^ 1")

    # Unknown inputs - always unknown for XOR
    await check_output(dut, {'xor2_a1': 'x', 'xor2_a2': 0}, 'x', dut.xor2_z, "XOR2: x ^ 0")
    await check_output(dut, {'xor2_a1': 0, 'xor2_a2': 'x'}, 'x', dut.xor2_z, "XOR2: 0 ^ x")
    await check_output(dut, {'xor2_a1': 'x', 'xor2_a2': 1}, 'x', dut.xor2_z, "XOR2: x ^ 1")
    await check_output(dut, {'xor2_a1': 1, 'xor2_a2': 'x'}, 'x', dut.xor2_z, "XOR2: 1 ^ x")

@cocotb.test()
async def test_xor3_1(dut):
    """Test XOR3 gate: Z = A1 ^ A2 ^ A3"""
    dut._log.info("Testing XOR3 gate...")

    # Known inputs
    await check_output(dut, {'xor3_a1': 0, 'xor3_a2': 0, 'xor3_a3': 0}, 0, dut.xor3_z, "XOR3: 0 ^ 0 ^ 0")
    await check_output(dut, {'xor3_a1': 1, 'xor3_a2': 0, 'xor3_a3': 0}, 1, dut.xor3_z, "XOR3: 1 ^ 0 ^ 0")
    await check_output(dut, {'xor3_a1': 1, 'xor3_a2': 1, 'xor3_a3': 0}, 0, dut.xor3_z, "XOR3: 1 ^ 1 ^ 0")
    await check_output(dut, {'xor3_a1': 1, 'xor3_a2': 1, 'xor3_a3': 1}, 1, dut.xor3_z, "XOR3: 1 ^ 1 ^ 1")

    # Unknown inputs - always unknown
    await check_output(dut, {'xor3_a1': 'x', 'xor3_a2': 0, 'xor3_a3': 0}, 'x', dut.xor3_z, "XOR3: x ^ 0 ^ 0")

@cocotb.test()
async def test_xnor2_1(dut):
    """Test XNOR2 gate: ZN = !(A1 ^ A2)"""
    dut._log.info("Testing XNOR2 gate...")

    # Known inputs
    await check_output(dut, {'xnor2_a1': 0, 'xnor2_a2': 0}, 1, dut.xnor2_zn, "XNOR2: !(0 ^ 0)")
    await check_output(dut, {'xnor2_a1': 0, 'xnor2_a2': 1}, 0, dut.xnor2_zn, "XNOR2: !(0 ^ 1)")
    await check_output(dut, {'xnor2_a1': 1, 'xnor2_a2': 0}, 0, dut.xnor2_zn, "XNOR2: !(1 ^ 0)")
    await check_output(dut, {'xnor2_a1': 1, 'xnor2_a2': 1}, 1, dut.xnor2_zn, "XNOR2: !(1 ^ 1)")

    # Unknown inputs - always unknown for XNOR
    await check_output(dut, {'xnor2_a1': 'x', 'xnor2_a2': 0}, 'x', dut.xnor2_zn, "XNOR2: !(x ^ 0)")
    await check_output(dut, {'xnor2_a1': 1, 'xnor2_a2': 'x'}, 'x', dut.xnor2_zn, "XNOR2: !(1 ^ x)")

# ============================================================================
# Inverter Test
# ============================================================================

@cocotb.test()
async def test_clkinv_1(dut):
    """Test Inverter: ZN = !I"""
    dut._log.info("Testing Inverter...")

    # Known inputs
    await check_output(dut, {'clkinv_i': 0}, 1, dut.clkinv_zn, "INV: !0")
    await check_output(dut, {'clkinv_i': 1}, 0, dut.clkinv_zn, "INV: !1")

    # Unknown input - unknown result
    await check_output(dut, {'clkinv_i': 'x'}, 'x', dut.clkinv_zn, "INV: !x")

# ============================================================================
# Multiplexer Test
# ============================================================================

@cocotb.test()
async def test_mux2_2(dut):
    """Test MUX2: Z = S ? I1 : I0"""
    dut._log.info("Testing MUX2 gate...")

    # Known inputs
    await check_output(dut, {'mux2_i0': 0, 'mux2_i1': 1, 'mux2_s': 0}, 0, dut.mux2_z, "MUX2: S=0 selects I0")
    await check_output(dut, {'mux2_i0': 0, 'mux2_i1': 1, 'mux2_s': 1}, 1, dut.mux2_z, "MUX2: S=1 selects I1")

    # Unknown select - unknown result
    await check_output(dut, {'mux2_i0': 0, 'mux2_i1': 1, 'mux2_s': 'x'}, 'x', dut.mux2_z, "MUX2: S=x")

    # Unknown inputs but same value - deterministic
    await check_output(dut, {'mux2_i0': 1, 'mux2_i1': 1, 'mux2_s': 'x'}, 1, dut.mux2_z, "MUX2: both inputs 1, S=x")
    await check_output(dut, {'mux2_i0': 0, 'mux2_i1': 0, 'mux2_s': 'x'}, 0, dut.mux2_z, "MUX2: both inputs 0, S=x")

    # Known select with unknown input - deterministic
    await check_output(dut, {'mux2_i0': 0, 'mux2_i1': 'x', 'mux2_s': 0}, 0, dut.mux2_z, "MUX2: S=0, I1=x doesn't matter")
    await check_output(dut, {'mux2_i0': 'x', 'mux2_i1': 1, 'mux2_s': 1}, 1, dut.mux2_z, "MUX2: S=1, I0=x doesn't matter")

# ============================================================================
# AOI Gates Tests
# ============================================================================

@cocotb.test()
async def test_aoi21_1(dut):
    """Test AOI21 gate: ZN = !((A1 & A2) | B)"""
    dut._log.info("Testing AOI21 gate...")

    # B=1 cases - output always 0
    await check_output(dut, {'aoi21_a1': 'x', 'aoi21_a2': 'x', 'aoi21_b': 1}, 0, dut.aoi21_zn, "AOI21: B=1, A=x")

    # B=0, A1=0 or A2=0 - output always 1
    await check_output(dut, {'aoi21_a1': 0, 'aoi21_a2': 'x', 'aoi21_b': 0}, 1, dut.aoi21_zn, "AOI21: B=0, A1=0")
    await check_output(dut, {'aoi21_a1': 'x', 'aoi21_a2': 0, 'aoi21_b': 0}, 1, dut.aoi21_zn, "AOI21: B=0, A2=0")

    # B=0, A1=1, A2=1 - output is 0
    await check_output(dut, {'aoi21_a1': 1, 'aoi21_a2': 1, 'aoi21_b': 0}, 0, dut.aoi21_zn, "AOI21: B=0, A1=1, A2=1")

    # B=0, A1=1, A2=x - output is x
    await check_output(dut, {'aoi21_a1': 1, 'aoi21_a2': 'x', 'aoi21_b': 0}, 'x', dut.aoi21_zn, "AOI21: B=0, A1=1, A2=x")

    # B=x, A1=1, A2=1 - output is 0
    await check_output(dut, {'aoi21_a1': 1, 'aoi21_a2': 1, 'aoi21_b': 'x'}, 0, dut.aoi21_zn, "AOI21: B=x, A1=1, A2=1")

    # B=x, other cases - output is x
    await check_output(dut, {'aoi21_a1': 0, 'aoi21_a2': 0, 'aoi21_b': 'x'}, 'x', dut.aoi21_zn, "AOI21: B=x, A1=0, A2=0")

@cocotb.test()
async def test_aoi22_1(dut):
    """Test AOI22 gate: ZN = !((A1 & A2) | (B1 & B2))"""
    dut._log.info("Testing AOI22 gate...")

    # Both AND gates produce 1 - output is 0
    await check_output(dut, {'aoi22_a1': 1, 'aoi22_a2': 1, 'aoi22_b1': 1, 'aoi22_b2': 1}, 0, dut.aoi22_zn, "AOI22: all 1s")

    # One AND gate produces 1, other unknown - output is 0
    await check_output(dut, {'aoi22_a1': 1, 'aoi22_a2': 1, 'aoi22_b1': 'x', 'aoi22_b2': 'x'}, 0, dut.aoi22_zn, "AOI22: A=1, B=x")

    # Both AND gates produce 0 - output is 1
    await check_output(dut, {'aoi22_a1': 0, 'aoi22_a2': 'x', 'aoi22_b1': 0, 'aoi22_b2': 'x'}, 1, dut.aoi22_zn, "AOI22: both ANDs=0")

    # Mixed - output is x
    await check_output(dut, {'aoi22_a1': 0, 'aoi22_a2': 'x', 'aoi22_b1': 1, 'aoi22_b2': 'x'}, 'x', dut.aoi22_zn, "AOI22: A=0, B=x")

@cocotb.test()
async def test_aoi211_1(dut):
    """Test AOI211 gate: ZN = !((A1 & A2) | B | C)"""
    dut._log.info("Testing AOI211 gate...")

    # B=1 or C=1 - output is 0
    await check_output(dut, {'aoi211_a1': 'x', 'aoi211_a2': 'x', 'aoi211_b': 1, 'aoi211_c': 0}, 0, dut.aoi211_zn, "AOI211: B=1")
    await check_output(dut, {'aoi211_a1': 'x', 'aoi211_a2': 'x', 'aoi211_b': 0, 'aoi211_c': 1}, 0, dut.aoi211_zn, "AOI211: C=1")

    # B=0, C=0, A1=0 or A2=0 - output is 1
    await check_output(dut, {'aoi211_a1': 0, 'aoi211_a2': 'x', 'aoi211_b': 0, 'aoi211_c': 0}, 1, dut.aoi211_zn, "AOI211: B=0, C=0, A1=0")

    # B=0, C=0, A1=1, A2=1 - output is 0
    await check_output(dut, {'aoi211_a1': 1, 'aoi211_a2': 1, 'aoi211_b': 0, 'aoi211_c': 0}, 0, dut.aoi211_zn, "AOI211: B=0, C=0, A=1")

@cocotb.test()
async def test_aoi221_1(dut):
    """Test AOI221 gate: ZN = !((A1 & A2) | (B1 & B2) | C)"""
    dut._log.info("Testing AOI221 gate...")

    # C=1 - output is 0
    await check_output(dut, {'aoi221_a1': 'x', 'aoi221_a2': 'x', 'aoi221_b1': 'x', 'aoi221_b2': 'x', 'aoi221_c': 1}, 0, dut.aoi221_zn, "AOI221: C=1")

    # C=0, one AND=1 - output is 0
    await check_output(dut, {'aoi221_a1': 1, 'aoi221_a2': 1, 'aoi221_b1': 0, 'aoi221_b2': 'x', 'aoi221_c': 0}, 0, dut.aoi221_zn, "AOI221: C=0, A=1")

    # C=0, both ANDs=0 - output is 1
    await check_output(dut, {'aoi221_a1': 0, 'aoi221_a2': 'x', 'aoi221_b1': 0, 'aoi221_b2': 'x', 'aoi221_c': 0}, 1, dut.aoi221_zn, "AOI221: all ORs=0")

@cocotb.test()
async def test_aoi222_1(dut):
    """Test AOI222 gate: ZN = !((A1 & A2) | (B1 & B2) | (C1 & C2))"""
    dut._log.info("Testing AOI222 gate...")

    # One AND=1 - output is 0
    await check_output(dut, {'aoi222_a1': 1, 'aoi222_a2': 1, 'aoi222_b1': 'x', 'aoi222_b2': 'x', 'aoi222_c1': 'x', 'aoi222_c2': 'x'}, 0, dut.aoi222_zn, "AOI222: A=1")

    # All ANDs=0 - output is 1
    await check_output(dut, {'aoi222_a1': 0, 'aoi222_a2': 'x', 'aoi222_b1': 0, 'aoi222_b2': 'x', 'aoi222_c1': 0, 'aoi222_c2': 'x'}, 1, dut.aoi222_zn, "AOI222: all ANDs=0")

# ============================================================================
# OAI Gates Tests
# ============================================================================

@cocotb.test()
async def test_oai21_1(dut):
    """Test OAI21 gate: ZN = !((A1 | A2) & B)"""
    dut._log.info("Testing OAI21 gate...")

    # B=0 - output is 1
    await check_output(dut, {'oai21_a1': 'x', 'oai21_a2': 'x', 'oai21_b': 0}, 1, dut.oai21_zn, "OAI21: B=0")

    # B=1, A1=0, A2=0 - output is 1
    await check_output(dut, {'oai21_a1': 0, 'oai21_a2': 0, 'oai21_b': 1}, 1, dut.oai21_zn, "OAI21: B=1, A1=0, A2=0")

    # B=1, A1=1 or A2=1 - output is 0
    await check_output(dut, {'oai21_a1': 1, 'oai21_a2': 0, 'oai21_b': 1}, 0, dut.oai21_zn, "OAI21: B=1, A1=1")
    await check_output(dut, {'oai21_a1': 0, 'oai21_a2': 1, 'oai21_b': 1}, 0, dut.oai21_zn, "OAI21: B=1, A2=1")

    # B=1, A1=x, A2=0 - output is x
    await check_output(dut, {'oai21_a1': 'x', 'oai21_a2': 0, 'oai21_b': 1}, 'x', dut.oai21_zn, "OAI21: B=1, A=x")

    # B=x, A1=0, A2=0 - output is 1
    await check_output(dut, {'oai21_a1': 0, 'oai21_a2': 0, 'oai21_b': 'x'}, 1, dut.oai21_zn, "OAI21: B=x, OR=0")

    # B=x, A1=1 - output is x
    await check_output(dut, {'oai21_a1': 1, 'oai21_a2': 'x', 'oai21_b': 'x'}, 'x', dut.oai21_zn, "OAI21: B=x, OR=1")

@cocotb.test()
async def test_oai22_1(dut):
    """Test OAI22 gate: ZN = !((A1 | A2) & (B1 | B2))"""
    dut._log.info("Testing OAI22 gate...")

    # Both OR gates produce 0 - output is 1
    await check_output(dut, {'oai22_a1': 0, 'oai22_a2': 0, 'oai22_b1': 0, 'oai22_b2': 0}, 1, dut.oai22_zn, "OAI22: all 0s")

    # One OR gate produces 0, other unknown - output is 1
    await check_output(dut, {'oai22_a1': 0, 'oai22_a2': 0, 'oai22_b1': 'x', 'oai22_b2': 'x'}, 1, dut.oai22_zn, "OAI22: A=0")

    # Both OR gates produce 1 - output is 0
    await check_output(dut, {'oai22_a1': 1, 'oai22_a2': 'x', 'oai22_b1': 1, 'oai22_b2': 'x'}, 0, dut.oai22_zn, "OAI22: both ORs=1")

@cocotb.test()
async def test_oai211_1(dut):
    """Test OAI211 gate: ZN = !((A1 | A2) & B & C)"""
    dut._log.info("Testing OAI211 gate...")

    # B=0 or C=0 - output is 1
    await check_output(dut, {'oai211_a1': 'x', 'oai211_a2': 'x', 'oai211_b': 0, 'oai211_c': 'x'}, 1, dut.oai211_zn, "OAI211: B=0")

    # B=1, C=1, A1=0, A2=0 - output is 1
    await check_output(dut, {'oai211_a1': 0, 'oai211_a2': 0, 'oai211_b': 1, 'oai211_c': 1}, 1, dut.oai211_zn, "OAI211: B=1, C=1, OR=0")

    # B=1, C=1, A1=1 - output is 0
    await check_output(dut, {'oai211_a1': 1, 'oai211_a2': 'x', 'oai211_b': 1, 'oai211_c': 1}, 0, dut.oai211_zn, "OAI211: all ANDs=1")

@cocotb.test()
async def test_oai221_1(dut):
    """Test OAI221 gate: ZN = !((A1 | A2) & (B1 | B2) & C)"""
    dut._log.info("Testing OAI221 gate...")

    # C=0 - output is 1
    await check_output(dut, {'oai221_a1': 'x', 'oai221_a2': 'x', 'oai221_b1': 'x', 'oai221_b2': 'x', 'oai221_c': 0}, 1, dut.oai221_zn, "OAI221: C=0")

    # C=1, one OR=0 - output is 1
    await check_output(dut, {'oai221_a1': 0, 'oai221_a2': 0, 'oai221_b1': 'x', 'oai221_b2': 'x', 'oai221_c': 1}, 1, dut.oai221_zn, "OAI221: C=1, A=0")

    # C=1, both ORs=1 - output is 0
    await check_output(dut, {'oai221_a1': 1, 'oai221_a2': 'x', 'oai221_b1': 1, 'oai221_b2': 'x', 'oai221_c': 1}, 0, dut.oai221_zn, "OAI221: all ANDs=1")

@cocotb.test()
async def test_oai222_1(dut):
    """Test OAI222 gate: ZN = !((A1 | A2) & (B1 | B2) & (C1 | C2))"""
    dut._log.info("Testing OAI222 gate...")

    # One OR=0 - output is 1
    await check_output(dut, {'oai222_a1': 0, 'oai222_a2': 0, 'oai222_b1': 'x', 'oai222_b2': 'x', 'oai222_c1': 'x', 'oai222_c2': 'x'}, 1, dut.oai222_zn, "OAI222: A=0")

    # All ORs=1 - output is 0
    await check_output(dut, {'oai222_a1': 1, 'oai222_a2': 'x', 'oai222_b1': 1, 'oai222_b2': 'x', 'oai222_c1': 1, 'oai222_c2': 'x'}, 0, dut.oai222_zn, "OAI222: all ORs=1")

@cocotb.test()
async def test_oai31_1(dut):
    """Test OAI31 gate: ZN = !((A1 | A2 | A3) & B)"""
    dut._log.info("Testing OAI31 gate...")

    # B=0 - output is 1
    await check_output(dut, {'oai31_a1': 'x', 'oai31_a2': 'x', 'oai31_a3': 'x', 'oai31_b': 0}, 1, dut.oai31_zn, "OAI31: B=0")

    # B=1, all A=0 - output is 1
    await check_output(dut, {'oai31_a1': 0, 'oai31_a2': 0, 'oai31_a3': 0, 'oai31_b': 1}, 1, dut.oai31_zn, "OAI31: B=1, OR=0")

    # B=1, one A=1 - output is 0
    await check_output(dut, {'oai31_a1': 1, 'oai31_a2': 0, 'oai31_a3': 0, 'oai31_b': 1}, 0, dut.oai31_zn, "OAI31: B=1, OR=1")

@cocotb.test()
async def test_oai32_1(dut):
    """Test OAI32 gate: ZN = !((A1 | A2 | A3) & (B1 | B2))"""
    dut._log.info("Testing OAI32 gate...")

    # One OR=0 - output is 1
    await check_output(dut, {'oai32_a1': 0, 'oai32_a2': 0, 'oai32_a3': 0, 'oai32_b1': 'x', 'oai32_b2': 'x'}, 1, dut.oai32_zn, "OAI32: A=0")

    # Both ORs=1 - output is 0
    await check_output(dut, {'oai32_a1': 1, 'oai32_a2': 'x', 'oai32_a3': 'x', 'oai32_b1': 1, 'oai32_b2': 'x'}, 0, dut.oai32_zn, "OAI32: both ORs=1")
