"""
Mathematical utility functions for quadratic equation solver.
"""

"""Custom absolute value function."""
def abs(x):
    if x < 0:
        return x * -1
    return x

"""Custom square root implementation using Newton's method."""
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
