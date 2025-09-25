"""
Polynomial solver module.
Contains functions for solving quadratic equations and formatting output.
"""

from math_utils import abs, sqrt

def reduce_form(coeffs):
    """Convert coefficient dictionary to readable polynomial string."""
    parts = []
    for p in sorted(coeffs.keys(), reverse=True):
        c = coeffs[p]
        if abs(c) < 1e-12:
            continue
        
        # Format the coefficient
        if c == int(c):
            coeff_str = str(int(c))
        else:
            coeff_str = f"{c:.6g}"
        
        # Handle the sign and spacing
        if c > 0 and parts:
            sign = " + "
        elif c < 0:
            sign = " - "
            coeff_str = coeff_str[1:]  # Remove the negative sign from coefficient
        else:
            sign = ""
        
        # Format the term based on power
        if p == 0:
            # Constant term - just show the coefficient
            term = f"{coeff_str}"
        elif p == 1:
            # Linear term - show as coefficient * X (without ^1)
            if abs(c) == 1:
                term = "X" if coeff_str == "1" else "-X"
            else:
                term = f"{coeff_str} * X"
        else:
            # Higher powers - show as coefficient * X^power
            if abs(c) == 1:
                term = f"X^{p}" if coeff_str == "1" else f"-X^{p}"
            else:
                term = f"{coeff_str} * X^{p}"
        
        parts.append(f"{sign}{term}")
    
    result = "".join(parts) if parts else "0"
    return result

def degree(coeffs):
    """Find the degree (highest power) of the polynomial."""
    deg = max((p for p, c in coeffs.items() if abs(c) > 1e-12), default=0)
    return deg

def solve(coeffs):
    """Solve the polynomial equation based on its degree."""
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
