#!/usr/bin/env python3
"""
Quadratic Equation Solver - Main Program

Usage: python3 computor.py "equation"
Example: python3 computor.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
"""

import sys
from equation_parser import parse_equation
from solver import solve, reduce_form, degree

def main():
    if len(sys.argv) != 2:
        print("Usage format: ./computor \"equation\"")
        sys.exit(1)

    equation = sys.argv[1]
    coeffs = parse_equation(equation)

    print("Reduced form:", reduce_form(coeffs), "= 0")
    deg = degree(coeffs)
    print("Polynomial degree:", deg)

    solve(coeffs)

if __name__ == "__main__":
    main()
