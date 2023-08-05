import math
import numpy as np


def sum1d(s, e):
    c = 0
    for i in range(s, e):
        c += i
    return c


def sum2d(s, e):
    c = 0
    for i in range(s, e):
        for j in range(s, e):
            c += i * j
    return c


def while_count(s, e):
    i = s
    c = 0
    while i < e:
        c += i
        i += 1
    return c


def copy_arrays(a, b):
    for i in range(a.shape[0]):
        b[i] = a[i]


def copy_arrays2d(a, b):
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            b[i, j] = a[i, j]


def redefine1():
    x = 0
    for i in range(5):
        x += 1
    x = 0. + x
    for i in range(5):
        x += 1
    return x


def andor(x, y):
    return (x > 0 and x < 10) or (y > 0 and y < 10)


def ifelse1(x, y):
    if x > y:
        return 1
    elif x == 0 or y == 0:
        return 2
    else:
        return 3


def ifelse2(x, y):
    if x > 0:
        if y > 0:
            return 1
        elif y < 0:
            return 1
        else:
            return 0
    elif x < 0:
        return 1
    else:
        return 0


def ifelse3(x, y):
    if x == y:
        return 1


def string_concat(x, y):
    a = "whatzup"
    return a + str(x + y)


def string_len(s):
    return len(s)


def string_slicing(s, start, stop):
    return s[start:stop]


def string_conversion(x):
    return str(x)


def string_comparison(s1, s2, op):
    return op(s1, s2)


def blackscholes_cnd(d):
    A1 = 0.31938153
    A2 = -0.356563782
    A3 = 1.781477937
    A4 = -1.821255978
    A5 = 1.330274429
    RSQRT2PI = 0.39894228040143267793994605993438
    K = 1.0 / (1.0 + 0.2316419 * math.fabs(d))
    ret_val = (RSQRT2PI * math.exp(-0.5 * d * d) *
               (K * (A1 + K * (A2 + K * (A3 + K * (A4 + K * A5))))))
    if d > 0:
        ret_val = 1.0 - ret_val
    return ret_val


def slicing(a, start, stop, step):
    """
    NoPython mode cannot create new array object that out live the scope of
    the function because the array data buffer is borrowed from an object in
    the function scope or from an argument.  Returning array would require
    stealing the data buffer reference or copying the array content.
    """
    return a[start:stop:step]

