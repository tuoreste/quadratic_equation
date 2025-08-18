import re
import sys
from math import sqrt
from fractions import Fraction

def parse_equation(equation):
    equation = equation.replace(" ", "")
    left, right = equation.split("=")

    def parse_side(side):
        terms = re.findall(r'([+-]?\d*\.?\d*)\*?X\^(\d+)', side)
        coeffs = {}
        for coeff, power in terms:
            if coeff in (git@vogsphere.42heilbronn.de:vogsphere/intra-uuid-21675683-b383-407a-b51c-8ac2c1cef12e-6828196-otuyishi", "+"): coeff = "1"
            elif coeff == "-": coeff = "-1"
            coeffs[int(power)] = coeffs.get(int(power), 0.0) + float(coeff)
        return coeffs

    left_terms = parse_side(left)
    right_terms = parse_side(right)

    for p, c in right_terms.items():
        left_terms[p] = left_terms.get(p, 0.0) - c

    return left_terms


def reduce_form(coeffs):
    parts = []
    for p in sorted(coeffs.keys()):
        c = coeffs[p]
        if abs(c) < 1e-12:
            continue
        parts.append(f"{c:.6g} * X^{p}")
    return " + ".join(parts) if parts else "0"


def degree(coeffs):
    deg = max((p for p, c in coeffs.items() if abs(c) > 1e-12), default=0)
    return deg


def solve(coeffs):
    deg = degree(coeffs)
    if deg == 0:
        if abs(coeffs.get(0, 0)) < 1e-12:
            print("All real numbers are solution.")
        else:
            print("No solution.")
    elif deg == 1:
        a = coeffs.get(1, 0)
        b = coeffs.get(0, 0)
        sol = -b / a
        print("The solution is:")
        print(sol)
    elif deg == 2:
        a = coeffs.get(2, 0)
        b = coeffs.get(1, 0)
        c = coeffs.get(0, 0)
        D = b**2 - 4*a*c
        if D > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            sol1 = (-b + sqrt(D)) / (2*a)
            sol2 = (-b - sqrt(D)) / (2*a)
            print(sol1)
            print(sol2)
        elif abs(D) < 1e-12:
            print("Discriminant is zero, the solution is:")
            sol = -b / (2*a)
            print(sol)
        else:
            print("Discriminant is strictly negative, no real solution.")
            re_part = -b / (2*a)
            im_part = sqrt(-D) / (2*a)
            print(f"{re_part} + {im_part}i")
            print(f"{re_part} - {im_part}i")
    else:
        print("The polynomial degree is strictly greater than 2, I can't solve.")


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
