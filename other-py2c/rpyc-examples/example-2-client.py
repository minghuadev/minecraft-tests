#!/usr/bin/env python

# https://rpyc.readthedocs.io/en/latest/tutorial/tut3.html

import rpyc
c = rpyc.connect("localhost", 18861)
u = c.root

r1 = c.root.get_answer()
r2 = c.root.the_real_answer_though

print(" example-1-client: ", "r1", " = ", repr(r1))
print(" example-1-client: ", "r2", " = ", repr(r2))

