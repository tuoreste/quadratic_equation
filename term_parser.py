"""
Term parsing and validation module.
Handles parsing of individual terms in polynomial expressions.
"""

import re
import sys
from parser import parse_power_expression

def parse_term(term):
    """Parse a single term to extract coefficient and power."""
    if not term:
        return 0, 0
        
    # Handle sign
    sign = 1
    if term.startswith('-'):
        sign = -1
        term = term[1:]
    elif term.startswith('+'):
        term = term[1:]
    
    # Handle multiplication in the term (e.g., "x^2*0", "0*x^2", "2*x", "x^1*x^0")
    if '*' in term:
        # Check if parentheses are only in power expressions (after ^)
        # If there are parentheses, they should only be in power expressions like x^(2+1)
        if '(' in term or ')' in term:
            # Check if all parentheses are in power expressions
            temp_term = term
            while True:
                power_match = re.search(r'\^[^()]*\([^)]*\)', temp_term)
                if not power_match:
                    break
                # Replace this valid power expression with a placeholder
                temp_term = temp_term[:power_match.start()] + "^VALID" + temp_term[power_match.end():]
            
            # If there are still parentheses left, they're invalid in multiplication context
            if '(' in temp_term or ')' in temp_term:
                print("Error: Unexpected parentheses in term")
                sys.exit(1)
        
        # Split by * while respecting parentheses in power expressions
        parts = []
        current_part = ""
        paren_depth = 0
        
        for char in term:
            if char == '(':
                paren_depth += 1
                current_part += char
            elif char == ')':
                paren_depth -= 1
                current_part += char
            elif char == '*' and paren_depth == 0:
                # Only split on * when not inside parentheses
                if current_part:
                    parts.append(current_part)
                    current_part = ""
            else:
                current_part += char
        
        # Add the last part
        if current_part:
            parts.append(current_part)
        coeff = 1
        total_power = 0
        has_variable = False
        
        for part in parts:
            part = part.strip()
            if 'X' in part.upper():
                # This part contains the variable
                has_variable = True
                var_pattern = r'([^Xx]*)[Xx](\^.*)?'
                match = re.match(var_pattern, part, re.IGNORECASE)
                
                if match:
                    var_coeff_part = match.group(1) or '1'
                    power_part = match.group(2)
                    
                    # Check for parentheses in coefficient part
                    if '(' in var_coeff_part or ')' in var_coeff_part:
                        print("Error: Parentheses in coefficients not supported")
                        sys.exit(1)
                    
                    # Parse variable coefficient
                    if var_coeff_part == '' or var_coeff_part == '+':
                        var_coeff = 1
                    elif var_coeff_part == '-':
                        var_coeff = -1
                    else:
                        try:
                            var_coeff = float(var_coeff_part)
                        except ValueError:
                            print("Error: Invalid coefficient format")
                            sys.exit(1)
                    
                    coeff *= var_coeff
                    
                    # Parse power and add to total power (since x^a * x^b = x^(a+b))
                    if power_part is None:
                        part_power = 1
                    else:
                        power_expr = power_part[1:]  # Remove ^
                        try:
                            part_power = parse_power_expression(power_expr)
                        except ValueError as e:
                            print(f"Error: {e}")
                            sys.exit(1)
                    
                    total_power += part_power
            else:
                # This part is a number coefficient
                # Check for parentheses in number coefficients
                if '(' in part or ')' in part:
                    print("Error: Parentheses in coefficients not supported")
                    sys.exit(1)
                
                try:
                    num_coeff = float(part) if part else 1
                    coeff *= num_coeff
                except ValueError:
                    print("Error: Invalid coefficient format")
                    sys.exit(1)
        
        if has_variable:
            # Validate total power is 0, 1, or 2
            try:
                if total_power not in [0, 1, 2]:
                    raise ValueError(f"Invalid power: {total_power}")
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)
                
            return sign * coeff, total_power
        else:
            # No variable, this is a constant term
            return sign * coeff, 0
    
    # Check if term contains variable (X or x) - no multiplication
    elif 'X' in term.upper():
        # First check if this is an exponential expression like "2^x" 
        if re.search(r'\d+\^[Xx]', term, re.IGNORECASE):
            print("Error: Exponential expressions not allowed")
            sys.exit(1)
        
        # Parse terms with implicit multiplication (like "21x2" = 21*x*2)
        # Pattern: [coefficient]X[additional_coefficient][^power] - must match entire term
        var_pattern = r'^([^Xx]*)[Xx]([0-9]*\.?[0-9]*)(\^.*)?$'
        match = re.match(var_pattern, term, re.IGNORECASE)
        
        if match:
            coeff_part = match.group(1) or '1'
            additional_coeff_part = match.group(2) or '1'
            power_part = match.group(3)
            
            # Check if coefficient part contains ^ (which would be invalid)
            if '^' in coeff_part:
                print("Error: Invalid coefficient format")
                sys.exit(1)
            
            # Parse coefficient
            if coeff_part == '' or coeff_part == '+':
                coeff = 1
            elif coeff_part == '-':
                coeff = -1
            else:
                try:
                    # Handle parentheses with fractions like (2/3)
                    if coeff_part.startswith('(') and coeff_part.endswith(')'):
                        expr = coeff_part[1:-1]  # Remove parentheses
                        # Only allow simple arithmetic for safety
                        if re.match(r'^[0-9+\-*/.\s]+$', expr):
                            coeff = eval(expr)
                        else:
                            raise ValueError("Invalid expression in parentheses")
                    else:
                        coeff = float(coeff_part)
                except (ValueError, SyntaxError, ZeroDivisionError):
                    print("Error: Invalid coefficient format")
                    sys.exit(1)
            
            # Parse additional coefficient (implicit multiplication)
            if additional_coeff_part and additional_coeff_part != '1':
                try:
                    additional_coeff = float(additional_coeff_part)
                    coeff *= additional_coeff
                except ValueError:
                    print("Error: Invalid coefficient format")
                    sys.exit(1)
            
            # Parse power
            if power_part is None:
                # No power specified means power of 1
                power = 1
            else:
                # Remove ^ symbol and parse power expression
                power_expr = power_part[1:]  # Remove ^
                try:
                    power = parse_power_expression(power_expr)
                except ValueError as e:
                    print(f"Error: {e}")
                    sys.exit(1)
                
                # Validate power is 0, 1, or 2
                try:
                    if power not in [0, 1, 2]:
                        raise ValueError(f"Invalid power: {power}")
                except ValueError as e:
                    print(f"Error: {e}")
                    sys.exit(1)

            return sign * coeff, power
        else:
            print("Error: Invalid term format")
            sys.exit(1)
    else:
        # Handle constant terms and number powers (e.g., "2^3", "5")
        if '^' in term:
            # Check for multiple ^ operators which should be an error
            if term.count('^') > 1:
                print("Error: Multiple ^ operators")
                sys.exit(1)
            
            # Check if this is a number raised to a power
            base_and_power = term.split('^', 1)
            base_part = base_and_power[0]
            power_part = base_and_power[1]
            
            # Check if power contains variable - this is invalid (exponential, not polynomial)
            if 'X' in power_part.upper():
                print("Error: Variables in exponents not allowed")
                sys.exit(1)
            
            try:
                base = float(base_part)
                # Parse and evaluate the power expression
                power_value = parse_power_expression(power_part)
                result = base ** power_value
                return sign * result, 0
            except (ValueError, TypeError) as e:
                print(f"Error: Invalid number power expression - {e}")
                sys.exit(1)
        else:
            # Simple constant term (power 0)
            try:
                coeff = float(term) if term else 0
                return sign * coeff, 0
            except ValueError:
                print("Error: Invalid constant term")
                sys.exit(1)
