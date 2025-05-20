# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    # print("+++++++++++++" + str(dut.uo_out.value) + "+++++++++++++")
    # dut.ui_in.value = 0b01110000
    # await ClockCycles(dut.clk, 1)
    # print("+++++++++++++" + str(dut.uo_out.value) + "+++++++++++++")
    # await ClockCycles(dut.clk, 1)
    # print("+++++++++++++" + str(dut.uo_out.value) + "+++++++++++++")
    # await ClockCycles(dut.clk, 1)
    # print("+++++++++++++" + str(dut.uo_out.value) + "+++++++++++++")
    # await ClockCycles(dut.clk, 1)
    # print("+++++++++++++" + str(dut.uo_out.value) + "+++++++++++++")
    # await ClockCycles(dut.clk, 1)
    # print("+++++++++++++" + str(dut.uo_out.value) + "+++++++++++++")

    dut._log.info("Test project behavior")

    # Set the input values you want to test

    # Wait for one clock cycle to see the outpuomgomgt values
    await ClockCycles(dut.clk, 1)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    assert dut.uo_out.value == 0, "Counter should be 0 after reset"

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.

    # # # Load 5 into the counter
    dut._log.info("Load 5 into the counter")
    dut.ui_in.value = 0b10010101
    await ClockCycles(dut.clk, 2) # have to wait for an extra clock cycle to get correct value from non-blocking assignment
    assert dut.uo_out.value == 5, "Counter value should be 5 after loading"

    # Counter up for 3 cycles
    dut._log.info("Count up for 3 cycles")
    dut.ui_in.value = 0b01110000
    await ClockCycles(dut.clk, 3)
    dut.ui_in.value = 0b00110000
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 8, "Counter value should be 8 after 3 counts up"

    # Counter down for 2 cycles
    dut._log.info("Count down for 2 cycles")
    dut.ui_in.value = 0b01010000
    await ClockCycles(dut.clk, 2)
    dut.ui_in.value = 0b00010000
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 6, "Counter value should be 6 after 2 counts down"
