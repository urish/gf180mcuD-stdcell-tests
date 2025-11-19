import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_aoi21_1(dut):
    """A simple test that toggles a signal."""
    dut.a1.value = 'x'
    dut.a2.value = 'x'
    dut.b.value = 1
    await Timer(10, unit="ns")
    assert dut.aoi21_1_zn.value == 0, "Initial output should be low"

    dut.a1.value = 1
    await Timer(10, unit="ns")
    assert dut.aoi21_1_zn.value == 0, "Output should still be low"

    dut.a1.value = 0
    dut.b.value = 0
    await Timer(10, unit="ns")
    assert dut.aoi21_1_zn.value == 1, "Output should be high when b is 0"

    dut.a1.value = 1
    dut.a2.value = 1
    dut.b.value = 'x'
    await Timer(10, unit="ns")
    assert dut.aoi21_1_zn.value == 0, "Output should be low when b is x and a1, a2 are 1"
