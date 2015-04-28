#!/usr/bin/env python

class NullDecl (object):
    def __init__ (self, func):
        print self.__class__.__name__, "__init__"
        self.func = func
        ##for n in set(dir(func)) - set(dir(self)):
        ##    setattr(self, n, getattr(func, n))

    def __call__ (self, * args):
        print self.__class__.__name__, "__call__"
        return self.func (*args)
    def __repr__(self):
        print self.__class__.__name__, "__repr__"
        return self.func

    # The descriptor protocol is the mechanism for binding a thing to an instance. 
    # It consists of __get__, __set__ and __delete__, which are called when 
    # the thing is got, set or deleted from the instances dictionary. 
    # In this case when the thing is got from the instance we are binding 
    # the first argument of it's __call__ method to the instance, using partial. 
    # This is done automatically for member functions when the class is constructed, 
    # but for a synthetic member function like this we need to do it explicitly. 
    # - tolomea 
    def __get__(self, obj, objtype):
        """Support instance methods."""
        import functools
        return functools.partial(self.__call__, obj)

class NullDecl1(NullDecl):
    pass

class NullDecl2(NullDecl):
    pass


# You need to make the decorator into a descriptor -- either by ensuring 
# its (meta)class has a __get__ method, or, way simpler, by using a decorator 
# function instead of a decorator class (since functions are already descriptors). 
# - Alex Martelli
def dec_check(f):
    def deco(self):
        print 'In deco'
        f(self)
    return deco


class MyCls:
    def __init__ (self, vv):
        self.v = vv

    @NullDecl1
    @NullDecl2
    def decoratedMethod(self, * args):
        print " v in decoratedMethod %d \n" % self.v
        pass

    @dec_check
    def decoratedMethod2(self):
        print " v in decoratedMethod %d \n" % self.v
        pass

    def pureMethod(self):
        print " v in pureMethod %d \n" % self.v
        pass


@NullDecl1
@NullDecl2
def decorated():
    pass

def pure():
    pass

# results in set(['func_closure', 'func_dict', '__get__', 'func_name',
# 'func_defaults', '__name__', 'func_code', 'func_doc', 'func_globals'])
print set(dir(pure)) - set(dir(decorated));


if __name__ == "__main__":
    pure()
    decorated()
    print dir(pure)
    print dir(decorated);

    print "\n Ok 1...\n"
    pure()
    decorated()

    print "\n Ok 2...\n"
    mycls = MyCls(333)
    mycls.pureMethod()
    mycls.decoratedMethod()
    mycls.decoratedMethod2()


