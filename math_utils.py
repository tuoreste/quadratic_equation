"""
Mathematical utility functions for quadratic equation solver.
"""

"""Custom absolute value function."""
def abs(x):
    if x < 0:
        return x * -1
    return x

"""Custom square root implementation using Newton's method."""
"""
def sqrt(num):
    a = 1.0
    step = 0.1
    tolerance = 0.01

    while True:
        b = a * a
        if abs(b - num) < tolerance:
            break
        elif b > num:
            prev = a - step
            if abs(prev*prev - num) < abs(b - num):
                return (round(a, 2))
            else:
                return (round(a, 2))
        a += step
    return (round(a, 2))
"""

def sqrt(num):
    if num < 0:
        raise ValueError("Cannot compute square root of negative number")
    x = num
    tolerance = 0.01
    if num == 0:
        return 0.0
    guess = num / 2.0
    while abs(guess * guess - num) > tolerance:
        guess = (guess + num / guess) / 2.0
    return round(guess, 2)


