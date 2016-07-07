#!/usr/bin/env python

###################################################################
'''
this is almost a verbatim copy of itertools.product with only added 
one more level of indirection when len(args)==1. this adds the ability 
to pass args in a single tuble argument variable.
'''

def product(*args, **kwds):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    if len(args) == 1:
        args = args[0]
    pools = map(tuple, args) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
        print result
    for prod in result:
        yield tuple(prod)

a=[1,2]
b=[3,4]
d=[5,6]

c=[a,b,d]

for k in product(c):
    print k

for k in product(*c):
    print k


###################################################################
'''
another example by searching  python turn nested for loop to generator
http://code.activestate.com/recipes/578046-easily-write-nested-loops/
'''

"""Provide an iterator for automatically nesting multiple sequences.

The "nest" generator function in this module is provided to make writing
nested loops easier to accomplish. Instead of writing a for loop at each
level, one may call "nest" with each sequence as an argument and receive
items from the sequences correctly yielded back to the caller. A test is
included at the bottom of this module to demonstrate how to use the code."""

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '17 February 2012'
__version__ = 1, 0, 0

################################################################################

def nest(*iterables):
    "Iterate over the iterables as if they were nested in loops."
    return _nest(list(map(tuple, reversed(iterables))))

def _nest(stack):
    "Build recursive loops and iterate over tuples on the stack."
    top = stack.pop()
    if stack:
        for v1 in top:
            for v2 in _nest(stack):
                yield (v1,) + v2
    else:
        for value in top:
            yield (value,)
    stack.append(top)

################################################################################

def test():
    "Check the nest generator function for correct yield values."
    subject = 'I He She It They Adam Eve Cain Abel Zacharias'.split()
    verb = 'ate bought caught dangled elected fought got hit'.split()
    complement = 'an elephant,a cow,the boot,my gun,its head'.split(',')
    for sentence in nest(subject, verb, complement):
        print('{} {} {}.'.format(*sentence))

if __name__ == '__main__':
    test()



###################################################################
'''
my version based on an answer here
http://stackoverflow.com/questions/1280667/in-python-is-there-an-easier-way-to-write-6-nested-for-loops
by searching  python turn nested for loop to generator
'''

def product2(*args):
    if len(args)<1:
        return
    if len(args) == 1:
        for x in args[0]:
            yield (x,)
    else:
        head = args[0]
        tail = args[1:]
        for h in head:
            for t in product2(*tail):
                yield tuple( [h] + list(t) )

for k in product2(*c):
    print k


