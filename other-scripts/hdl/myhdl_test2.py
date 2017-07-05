#!/usr/bin/env python

from myhdl import Signal, intbv, delay, always, now, Simulation, toVerilog

__debug = True

def ClkDriver(clk):

    halfPeriod = delay(10)

    @always(halfPeriod)
    def driveClk():
        clk.next = not clk

    return driveClk


def HelloWorld(clk, outs):

    counts = intbv(3)[32:]

    @always(clk.posedge)
    def sayHello():
        outs.next = not outs
        if counts >= 3 - 1:
            counts.next = 0
        else:
            counts.next = counts + 1
        if __debug__:
            print "%s Hello World! outs %s %s" % (
                  now(), str(outs), str(outs.next))

    return sayHello


clk = Signal(bool(0))
outs = Signal(intbv(0)[1:])
clkdriver_inst = ClkDriver(clk)
hello_inst = toVerilog(HelloWorld, clk, outs)
sim = Simulation(clkdriver_inst, hello_inst)
sim.run(150)


