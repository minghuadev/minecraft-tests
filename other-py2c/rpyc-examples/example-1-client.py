#!/usr/bin/env python

# https://rpyc.readthedocs.io/en/latest/tutorial/tut3.html

import rpyc
import copy

c = rpyc.connect("localhost", 18861,)
                 #config={'allow_pickle':True})
u = c.root

r1 = c.root.get_answer()
r1 = copy.deepcopy(r1)

r2 = c.root.the_real_answer_though

print(" example-2-client: ", "r1", " = ", repr(r1))
print(" example-2-client: ", "r2", " = ", repr(r2))

