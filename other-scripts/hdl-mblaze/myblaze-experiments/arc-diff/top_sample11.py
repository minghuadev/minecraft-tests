#!/usr/bin/env  python
#

# insert pythonpath to ../rtl
import os
import sys
sys.path.insert(0, os.path.abspath("../rtl"))

import myhdl

import top

if __name__ == '__main__':
    tb = myhdl.traceSignals(top.TopBench)
    myhdl.Simulation(tb).run()
