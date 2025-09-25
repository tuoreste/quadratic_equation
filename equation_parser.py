"""
Equation parsing and validation module.
Main parsing logic for polynomial equations.
"""

import re
import sys
from parser import split_terms_with_parentheses, expand_distributive
from term_parser import parse_term

def parse_equation(equation):
    """Parse a polynomial equation into coefficient dictionary."""
    # Protect against multiple '=' and handle errors
    try:
        left, right = equation.split('=')
    except ValueError as e:
        print("Error: Invalid equation format")
        sys.exit(1)
    
    # Check for empty sides
    if not left.strip():
        print("Error: Empty left side of equation")
        sys.exit(1)
    
    if not right.strip():
        print("Error: Empty right side of equation")
        sys.exit(1)

    def organize_equation_side(side):
        """Organize one side of the equation into terms dictionary."""
        side = side.replace(" ", "")  # remove whitespace
        
        # Expand distributive multiplication
        side = expand_distributive(side)
        
        # Check for balanced parentheses
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
        
        # After distributive expansion, remaining parentheses should only be in power expressions
        # Check if remaining parentheses are only after ^ symbols
        if '(' in side or ')' in side:
            # Check if all parentheses are in valid power expressions (after ^)
            temp_side = side
            while True:
                power_match = re.search(r'\^[^()]*\([^)]*\)', temp_side)
                if not power_match:
                    break
                # Replace this valid power expression with a placeholder
                temp_side = temp_side[:power_match.start()] + "^VALID" + temp_side[power_match.end():]
            
            # If there are still parentheses left, they're invalid
            if '(' in temp_side or ')' in temp_side:
                print("Error: Unsupported parentheses expression")
                sys.exit(1)
        
        # Check for consecutive operator signs
        # Allow up to 2 consecutive + or - (like +- or --), but reject other combinations
        if re.search(r'[*^]{2,}', side):  # Multiple * or ^ in a row
            print("Error: Consecutive operators")
            sys.exit(1)
        if re.search(r'[+\-]{3,}', side):  # More than 2 + or - in a row
            print("Error: Consecutive operators")
            sys.exit(1)
        if re.search(r'[+\-][*^]|[*^][+\-]', side):  # Mix of +/- with */^
            print("Error: Consecutive operators")
            sys.exit(1)
        if re.search(r'[*^][*^]', side):  # Mix of * and ^
            print("Error: Consecutive operators")
            sys.exit(1)
        
        # Check for multiple ^ in the same term (like 2^1^2)
        if re.search(r'[0-9]\^[^+\-]*\^', side):
            print("Error: Multiple exponentiation operators")
            sys.exit(1)
        
        # Check for equation sides ending with operators
        if re.search(r'[+\-*^]$', side):
            print("Error: Trailing operator")
            sys.exit(1)
        
        terms = {}  # dictionary of terms where key=power, value=coefficient
        
        # Split into terms while preserving signs and respecting parentheses
        matches = split_terms_with_parentheses(side)
        
        for term in matches:
            if not term:
                continue

            # Parse each term to extract coefficient and power
            # check for any other invalid characters
            try:
                if re.search(r'[^0-9Xx\^\+\-\*/(). ]', term):
                    raise ValueError("Invalid characters")
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)
            
            # Check for variables in denominators (like 2/3x which could be 2/(3x))
            # This would create negative powers which we don't support
            if re.search(r'/[^()]*[Xx]', term, re.IGNORECASE):
                print("Error: Variables in denominators not supported")
                sys.exit(1)
            
            # if it is empty after ^ there should be atleast + and number otherwise it is an error
            if re.search(r'\^[\+\-\*/(). ]*$', term):
                print("Error: Empty power")
                sys.exit(1)
            
            # Check for trailing operators
            if re.search(r'[+\-*^]$', term):
                print("Error: Term ends with operator")
                sys.exit(1)
            
            coeff, power = parse_term(term.strip())
            
            # Add to existing coefficient for this power or create new entry
            if power in terms:
                terms[power] += coeff
            else:
                terms[power] = coeff
        
        return terms
    
    left_terms = organize_equation_side(left)
    right_terms = organize_equation_side(right)
    
    # Move right side terms to left (subtract right side from left side)
    coeffs = {}
    
    # Add left side terms
    for power, coeff in left_terms.items():
        coeffs[power] = coeffs.get(power, 0) + coeff
    
    # Subtract right side terms  
    for power, coeff in right_terms.items():
        coeffs[power] = coeffs.get(power, 0) - coeff
    
    return coeffs
