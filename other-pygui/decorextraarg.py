
# How to pass extra arguments to python decorator?
# The outer function will be given any arguments you pass explicitly, 
# and should return the inner function. The inner function will 
# be passed the function to decorate, and return the wrapped function.
def myDecorator(logIt):
    def actualDecorator(test_func):
        @functools.wraps(test_func)
        def wrapper(*args, **kwargs):
            if logIt:
                print "Calling Function: " + test_func.__name__
            return test_func(*args, **kwargs)
        return wrapper
    return actualDecorator

@myDecorator(False)
def someFunc():
    print 'Hello'


