#!/usr/bin/env python
# mtcnn_pnet_l1.py
# https://github.com/kpzhang93/MTCNN_face_detection_alignment

'''
    Input:       n=12, 12x12 pixel
    Processing:  conv 3x3,           10 filters
    Middle L1c:  n-2, 10x10 array    x10
    Processing:  MP 2x2
    Middle L1m:  5x5 array           x10
'''

from myhdl import block, Signal, intbv, delay, always, always_comb, now, instance, StopSimulation
from myhdl import toVerilog

def computeRanges(n=12, p=3):
    n_pixels = n
    n_l1c = (n_pixels - (p-1))
    n_l1m = (n_l1c/2)
    r_pixels = n_pixels * n_pixels
    r_l1c = n_l1c * n_l1c
    r_l1m = n_l1m * n_l1m
    return n_l1c, n_l1m, r_pixels, r_l1c, r_l1m

@block
def PL1Net(clk, go, done, pixels, mid1c, mid1p, filter, n=12, p=3):
    n_l1c, n_l1m, r_pixels, r_l1c, r_l1m = computeRanges(n, p)

    sig_l1m = [Signal(intbv(0)[16:]) for i in range(r_l1m)]
    state_go = Signal(bool(False))
    state_done = Signal(bool(False))
    stage_m = Signal(bool(False))

    sig_l1c = Signal(intbv(0)[18:])
    conv_cord_x = Signal(intbv(0, min=0, max=n))
    conv_cord_y = Signal(intbv(0, min=0, max=n))

    patch_x = Signal(intbv(0, min=0, max=n))
    patch_y = Signal(intbv(0, min=0, max=n))
    patch_cumu = Signal(bool(False))

    @always(clk.posedge)
    def computePL1():
        done.next = state_done
        if not state_go: # state_go
            state_done.next = False # state_done
            stage_m.next = False # stage_mp
            sig_l1c.next = 0
            for i in range(r_l1m): sig_l1m[i] = 0
            conv_cord_x.next = 0
            conv_cord_y.next = 0
            patch_x.next = 0
            patch_y.next = 0
            patch_cumu.next = False
            if go:
                state_go.next = True
                if __debug__:
                    print " now %s good state start" % now()
        else:
            if not state_done: # state_done
                if not stage_m: # stage_mp
                    if __debug__:
                        print " now %s stage p x %u y %u p %u %u" % (
                            now(), conv_cord_x, conv_cord_y,
                            patch_x, patch_y)
                    if not patch_cumu:
                        fltidx = patch_x + patch_y * p
                        pixidx = (conv_cord_x + patch_x) + (conv_cord_y + patch_y) * p
                        sig_l1c.next = sig_l1c + filter[fltidx] * pixels[pixidx]
                        if patch_x >= p-1 and patch_y >= p-1:
                            patch_cumu.next = True
                        elif patch_x >= p-1:
                            patch_x.next = 0
                            patch_y.next = patch_y + 1
                        else:
                            patch_x.next = patch_x + 1
                    else:
                        pixidx = conv_cord_x + conv_cord_y * p
                        mid1c[pixidx] = sig_l1c[16:8]
                        patch_cumu.next = False
                        patch_x.next = 0
                        patch_y.next = 0
                        if conv_cord_x >= n_l1c - 1 and conv_cord_y >= n_l1c - 1:
                            stage_m.next = True
                        elif conv_cord_x == n_l1c - 1:
                            conv_cord_x.next = 0
                            conv_cord_y.next = conv_cord_y + 1
                        else:
                            conv_cord_x.next = conv_cord_x + 1
                else:
                    if __debug__:
                        print " now %s stage m x %u y %u p %u %u" % (
                            now(), conv_cord_x, conv_cord_y,
                            patch_x, patch_y)
                    state_done.next = True

    return computePL1

@block
def mtcnn_pnet_l1_toplogic(clock, go, finished, n=12, p=3):

    n_pixels = n
    n_filter = p # filter dimension 3 x 3
    n_l1c, n_l1m, r_pixels, r_l1c, r_l1m = computeRanges(n_pixels, n_filter)

    content = [x for x in range(p * p)]

    pixels = [Signal(intbv(3)[8:]) for i in range(r_pixels)]
    midl1c = [Signal(intbv(3)[8:]) for i in range(r_l1c)]
    midl1m = [Signal(intbv(3)[8:]) for i in range(r_l1m)]

    filters = [Signal(intbv(content[i])[8:]) for i in range(n_filter * n_filter)]

    hello_inst = PL1Net(clock, go, finished, pixels, midl1c, midl1m,
                        filters, n_pixels, n_filter)

    return hello_inst

if __name__ == '__main__':
    import sys
    do_sim = True
    if len(sys.argv) > 1 and sys.argv[1] == "goconv":
        do_sim = False

    if do_sim:
        @block
        def topsim():
            clk = Signal(bool(0))
            halfperiod = delay(5)
            @always(halfperiod)
            def clockGen():
                clk.next = not clk
            trigger = Signal(bool(0))
            finished = Signal(bool(0))

            n=6
            p=2

            h2inst = mtcnn_pnet_l1_toplogic(clk, trigger, finished,
                                      n=n, p=p)

            @instance
            def stimulus():
                yield clk.negedge
                yield clk.posedge
                trigger.next = True
                for i in range(16000):
                    if i > 5:
                        trigger.next = False
                    yield clk.negedge
                    if finished:
                        break
                print " done at now %s  n=%d p=%d" % (now(), n, p)
                '''
                        1300   6 2
                        10050 12 3
                        19650 16 3
                        37490 16 5
                '''
                raise StopSimulation()
            return clockGen, h2inst, stimulus

        mysys = topsim()
        mysys.run_sim()
    else:
        def topconv():
            clk = Signal(bool(0))
            trigger = Signal(bool(0))
            finished = Signal(bool(0))
            toVerilog.initial_values = True
            h2inst = mtcnn_pnet_l1_toplogic(clk, trigger, finished, 12, 3)
            h2inst.convert(hdl="Verilog")

        topconv()

