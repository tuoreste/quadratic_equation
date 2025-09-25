"""
Equation parsing and validation module.
Main parsing logic for polynomial equations.
"""

import re
import sys
from parser import split_terms_with_parentheses, expand_distributive
from term_parser import parse_term

"""Parse a polynomial equation into coefficient dictionary."""
def parse_equation(equation):
    try:
        left, right = equation.split('=')
    except ValueError as e:
        print("Error: Invalid equation format")
        sys.exit(1)
    
    if not left.strip():
        print("Error: Empty left side of equation")
        sys.exit(1)
    
    if not right.strip():
        print("Error: Empty right side of equation")
        sys.exit(1)

    """Parse and validate one side of equation, returning terms dictionary."""
    def organize_equation_side(side):
        side = side.replace(" ", "")
        side = expand_distributive(side)
        
        paren_count = 0
        for char in side:
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
                if paren_count < 0:
                    print("Error: Unmatched closing parenthesis")
                    sys.exit(1)
        
        if paren_count > 0:
            print("Error: Unmatched opening parenthesis")
            sys.exit(1)
        
        if '(' in side or ')' in side:
            temp_side = side
            while True:
                power_match = re.search(r'\^[^()]*\([^)]*\)', temp_side)
                if not power_match:
                    break
                temp_side = temp_side[:power_match.start()] + "^VALID" + temp_side[power_match.end():]
            
            if '(' in temp_side or ')' in temp_side:
                print("Error: Unsupported parentheses expression")
                sys.exit(1)
        
        if re.search(r'[*^]{2,}', side):
            print("Error: Consecutive operators")
            sys.exit(1)
        if re.search(r'[+\-]{3,}', side):
            print("Error: Consecutive operators")
            sys.exit(1)
        if re.search(r'[+\-][*^]|[*^][+\-]', side):
            print("Error: Consecutive operators")
            sys.exit(1)
        if re.search(r'[*^][*^]', side):
            print("Error: Consecutive operators")
            sys.exit(1)
        
        if re.search(r'[0-9]\^[^+\-]*\^', side):
            print("Error: Multiple exponentiation operators")
            sys.exit(1)
        
        if re.search(r'[+\-*^]$', side):
            print("Error: Trailing operator")
            sys.exit(1)
        
        terms = {}
        matches = split_terms_with_parentheses(side)
        
        for term in matches:
            if not term:
                continue

            try:
                if re.search(r'[^0-9Xx\^\+\-\*/(). ]', term):
                    raise ValueError("Invalid characters")
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)
            
            if re.search(r'/[^()]*[Xx]', term, re.IGNORECASE):
                print("Error: Variables in denominators not supported")
                sys.exit(1)
            
            if re.search(r'\^[\+\-\*/(). ]*$', term):
                print("Error: Empty power")
                sys.exit(1)
            
            if re.search(r'[+\-*^]$', term):
                print("Error: Term ends with operator")
                sys.exit(1)
            
            coeff, power = parse_term(term.strip())
            
            if power in terms:
                terms[power] += coeff
            else:
                terms[power] = coeff
        
        return terms
    
    left_terms = organize_equation_side(left)
    right_terms = organize_equation_side(right)
    
    coeffs = {}
    
    for power, coeff in left_terms.items():
        coeffs[power] = coeffs.get(power, 0) + coeff
    
    for power, coeff in right_terms.items():
        coeffs[power] = coeffs.get(power, 0) - coeff
    
    return coeffs
