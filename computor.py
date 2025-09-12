import re
import sys

def abs(x):
    if x < 0:
        return x * -1
    return x

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

def parse_equation(equation):
    equation = equation.replace(" ", "")
    left, right = equation.split("=")

    def parse_side(side):
        coeffs = {}

        tokens = re.findall(r'([+-]?\s*\d*\.?\d*)\s*\*?\s*X(?:\^([+-]?\d*\.?\d+))?|([+-]?\s*\d+\.?\d*)', side)

        for coeff, power, const in tokens:
            coeff = coeff.replace(" ", "")
            const = const.replace(" ", "")

            if const:
                c = float(const)
                coeffs[0] = coeffs.get(0, 0) + c
            else:
                if coeff in ("", "+"):
                    c = 1.0
                elif coeff == "-":
                    c = -1.0
                else:
                    c = float(coeff)

                if power == "":
                    p = 1
                elif power is None:
                    p = 1
                else:
                    if (float(power)) % 1 != 0:
                        print("Error: Decimal Power not supported.")
                        sys.exit(1)
                        return
                    else:
                        p = int(power)

                coeffs[p] = coeffs.get(p, 0) + c

        return coeffs

    left_terms = parse_side(left)
    right_terms = parse_side(right)

    for p, c in right_terms.items():
        left_terms[p] = left_terms.get(p, 0.0) - c

    return left_terms


def reduce_form(coeffs):
    parts = []
    for p in sorted(coeffs.keys(), reverse=True):
        c = coeffs[p]
        if abs(c) < 1e-12:
            continue
        sign = "+" if c > 0 and parts else ""
        parts.append(f"{sign}{c:.6g} * X^{p}")
    return " ".join(parts) if parts else "0"


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
        D = b*b - 4*a*c
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
