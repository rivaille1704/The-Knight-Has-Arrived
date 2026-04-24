# nim_next.py

import random
import math

def checkwin(a, b, c):
    while (a*a + b*b + c*c) != 0:
        if (a + b + c) % 2 == 1:
            return True
        a >>= 1
        b >>= 1
        c >>= 1
    return False

def nextlose(a, b, c):
    if c > 0:
        if c == 1:
            if b > 1:
                b = random.randrange(b)
            elif a > 1:
                a = random.randrange(a)
            else:
                c = 0
        else:
            c = random.randrange(c)
    else:
        if b == 1:
            if a > 1:
                a = random.randrange(a)
            else:
                b = 0
        else:
            b = random.randrange(b)
    return a, b, c

def calculate(m, n):
    value = 0
    i = 0
    while (m*m + n*n) != 0:
        value += ((m + n) % 2) * (2 ** i)
        m >>= 1
        n >>= 1
        i += 1
    return value

def nextwin(a, b, c):
    flag = None
    a1, b1, c1 = a, b, c
    while (a1*a1 + b1*b1 + c1*c1) != 0:
        m = a1 % 2
        n = b1 % 2
        p = c1 % 2
        if (m + n + p) % 2 == 1:
            if m == 1:
                flag = 1
            elif n == 1:
                flag = 2
            else:
                flag = 3
        a1 >>= 1
        b1 >>= 1
        c1 >>= 1
    if flag == 1:
        a = calculate(b, c)
    elif flag == 2:
        b = calculate(a, c)
    else:
        c = calculate(a, b)
    return a, b, c

def next_move(a, b, c):
    if a == 0 and b == 0 and c == 0:
        return "win"
    if not checkwin(a, b, c):
        return nextlose(a, b, c)
    else:
        return nextwin(a, b, c)
