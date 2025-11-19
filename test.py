"""
AOI21_1 Unknown State Test Bench

Tests the aoi21_1 standard cell (AND-OR-INVERT 2-1) with unknown ('x') states.
The gate implements: ZN = !((A1 & A2) | B)

Unknown value propagation rules:
- x | 1 == 1  (OR with 1 is always 1)
- x & 0 == 0  (AND with 0 is always 0)
- x | 0 == x  (result is unknown)
- x & 1 == x  (result is unknown)

Examples for aoi21_1:
- B=1, A1=x, A2=x => (x & x) | 1 = 1, so ZN = 0 (deterministic)
- B=0, A1=0, A2=x => (0 & x) | 0 = 0, so ZN = 1 (deterministic)
- B=0, A1=1, A2=x => (1 & x) | 0 = x, so ZN = x (unknown)
- B=x, A1=1, A2=1 => (1 & 1) | x = 1, so ZN = 0 (deterministic)
"""

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_aoi21_1(dut):
    """Comprehensive test for aoi21_1 with unknown states."""

    # Helper function to check output
    async def check_output(a1, a2, b, expected, description):
        dut.a1.value = a1
        dut.a2.value = a2
        dut.b.value = b
        await Timer(10, unit="ns")
        actual = dut.aoi21_1_zn.value

        if expected == 'x':
            # For unknown, we just check that it's X, Z, or any unknown state
            assert actual.is_resolvable == False, \
                f"{description}: Expected unknown, got {actual} (a1={a1}, a2={a2}, b={b})"
        else:
            assert actual == expected, \
                f"{description}: Expected {expected}, got {actual} (a1={a1}, a2={a2}, b={b})"

    # ============================================================================
    # Case 1: B=1 => Output always 0 (regardless of A1, A2)
    # (A1 & A2) | 1 = 1, so ZN = !1 = 0
    # ============================================================================
    await check_output(0, 0, 1, 0, "B=1, A1=0, A2=0")
    await check_output(0, 1, 1, 0, "B=1, A1=0, A2=1")
    await check_output(1, 0, 1, 0, "B=1, A1=1, A2=0")
    await check_output(1, 1, 1, 0, "B=1, A1=1, A2=1")
    await check_output('x', 0, 1, 0, "B=1, A1=x, A2=0")
    await check_output(0, 'x', 1, 0, "B=1, A1=0, A2=x")
    await check_output('x', 1, 1, 0, "B=1, A1=x, A2=1")
    await check_output(1, 'x', 1, 0, "B=1, A1=1, A2=x")
    await check_output('x', 'x', 1, 0, "B=1, A1=x, A2=x")

    # ============================================================================
    # Case 2: B=0, A1=0 => Output always 1 (regardless of A2)
    # (0 & A2) | 0 = 0, so ZN = !0 = 1
    # ============================================================================
    await check_output(0, 0, 0, 1, "B=0, A1=0, A2=0")
    await check_output(0, 1, 0, 1, "B=0, A1=0, A2=1")
    await check_output(0, 'x', 0, 1, "B=0, A1=0, A2=x")

    # ============================================================================
    # Case 3: B=0, A2=0 => Output always 1 (regardless of A1)
    # (A1 & 0) | 0 = 0, so ZN = !0 = 1
    # ============================================================================
    await check_output(1, 0, 0, 1, "B=0, A1=1, A2=0")
    await check_output('x', 0, 0, 1, "B=0, A1=x, A2=0")

    # ============================================================================
    # Case 4: B=0, A1=1, A2=1 => Output is 0
    # (1 & 1) | 0 = 1, so ZN = !1 = 0
    # ============================================================================
    await check_output(1, 1, 0, 0, "B=0, A1=1, A2=1")

    # ============================================================================
    # Case 5: B=0, one of A1/A2 is 1, the other is x => Output is x
    # (1 & x) | 0 = x, so ZN = !x = x
    # ============================================================================
    await check_output(1, 'x', 0, 'x', "B=0, A1=1, A2=x")
    await check_output('x', 1, 0, 'x', "B=0, A1=x, A2=1")

    # ============================================================================
    # Case 6: B=0, both A1 and A2 are x => Output is x
    # (x & x) | 0 = x, so ZN = !x = x
    # ============================================================================
    await check_output('x', 'x', 0, 'x', "B=0, A1=x, A2=x")

    # ============================================================================
    # Case 7: B=x, A1=1, A2=1 => Output is 0
    # (1 & 1) | x = 1 | x = 1, so ZN = !1 = 0
    # ============================================================================
    await check_output(1, 1, 'x', 0, "B=x, A1=1, A2=1")

    # ============================================================================
    # Case 8: B=x, A1=0 or A2=0 => Output is x
    # (0 & x) | x = 0 | x = x, so ZN = !x = x
    # ============================================================================
    await check_output(0, 0, 'x', 'x', "B=x, A1=0, A2=0")
    await check_output(0, 1, 'x', 'x', "B=x, A1=0, A2=1")
    await check_output(1, 0, 'x', 'x', "B=x, A1=1, A2=0")
    await check_output(0, 'x', 'x', 'x', "B=x, A1=0, A2=x")
    await check_output('x', 0, 'x', 'x', "B=x, A1=x, A2=0")

    # ============================================================================
    # Case 9: B=x, A1=1, A2=x (or vice versa) => Output is x
    # (1 & x) | x = x | x = x, so ZN = !x = x
    # ============================================================================
    await check_output(1, 'x', 'x', 'x', "B=x, A1=1, A2=x")
    await check_output('x', 1, 'x', 'x', "B=x, A1=x, A2=1")
    await check_output('x', 'x', 'x', 'x', "B=x, A1=x, A2=x")

    dut._log.info("All aoi21_1 unknown state tests passed!")
