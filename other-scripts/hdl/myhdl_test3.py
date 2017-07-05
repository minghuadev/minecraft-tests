#!/usr/bin/env python

from myhdl import Signal, intbv, delay, always, now, Simulation, toVerilog


def ClkDriver(clk):

    halfPeriod = delay(10)

    @always(halfPeriod)
    def driveClk():
        clk.next = not clk

    return driveClk


def HelloWorld(clk, outs):

    counts = [Signal(intbv(3)[32:])]

    @always(clk.posedge)
    def sayHello():
        outs.next = not outs
        if counts[0] >= 3 - 1:
            counts[0].next = 0
        else:
            counts[0].next = counts[0] + 1
        if __debug__:
            print "%s Hello World! outs %s %s %d" % (
                  now(), str(outs), str(outs.next), counts[0])

    return sayHello


clk = Signal(bool(0))
outs = Signal(intbv(0)[1:])
clkdriver_inst = ClkDriver(clk)
toVerilog.initial_values=True
hello_inst = toVerilog(HelloWorld, clk, outs)
sim = Simulation(clkdriver_inst, hello_inst)
sim.run(150)


