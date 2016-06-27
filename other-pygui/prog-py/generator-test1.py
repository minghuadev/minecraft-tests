#!/usr/bin/python
#   generator-test1.py


# https://jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/

import math

def is_prime(number):
    if number > 1:
        if number == 2:
            return True
        if number % 2 == 0:
            return False
        for current in range(3, int(math.sqrt(number) + 1), 2):
            if number % current == 0: 
                return False
        return True
    return False

def get_primes(number):
    print "                start with number %d" % number
    while True:
        if is_prime(number):
            print "                to yield prime number %d" % number
            number = yield number
            print "                to continue w number  %d" % number
        number += 1

def print_successive_primes(iterations, base=10):
    prime_generator = get_primes(base)
    prime_generator.send(None)
    for power in range(iterations):
        print(prime_generator.send(base ** power))

if __name__ == "__main__":
    print_successive_primes(2)


