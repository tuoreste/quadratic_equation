"""
Term parsing and validation module.
Handles parsing of individual terms in polynomial expressions.
"""

import re
import sys
from parser import parse_power_expression

"""Parse a single term to extract coefficient and power."""
def parse_term(term):
    if not term:
        return 0, 0

    sign = 1
    if term.startswith('-'):
        sign = -1
        term = term[1:]
    elif term.startswith('+'):
        term = term[1:]
    
    if '*' in term:
        if '(' in term or ')' in term:
            temp_term = term
            while True:
                power_match = re.search(r'\^[^()]*\([^)]*\)', temp_term)
                if not power_match:
                    break
                temp_term = temp_term[:power_match.start()] + "^VALID" + temp_term[power_match.end():]
            
            if '(' in temp_term or ')' in temp_term:
                print("Error: Unexpected parentheses in term")
                sys.exit(1)
        
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
                if current_part:
                    parts.append(current_part)
                    current_part = ""
            else:
                current_part += char
        
        if current_part:
            parts.append(current_part)
        coeff = 1
        total_power = 0
        has_variable = False
        
        for part in parts:
            part = part.strip()
            if 'X' in part.upper():
                has_variable = True
                var_pattern = r'([^Xx]*)[Xx](\^.*)?'
                match = re.match(var_pattern, part, re.IGNORECASE)
                
                if match:
                    var_coeff_part = match.group(1) or '1'
                    power_part = match.group(2)
                    
                    if '(' in var_coeff_part or ')' in var_coeff_part:
                        print("Error: Parentheses in coefficients not supported")
                        sys.exit(1)
                    
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
                    
                    if power_part is None:
                        part_power = 1
                    else:
                        power_expr = power_part[1:]
                        try:
                            part_power = parse_power_expression(power_expr)
                        except ValueError as e:
                            print(f"Error: {e}")
                            sys.exit(1)
                    
                    total_power += part_power
            else:
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
            try:
                if total_power not in [0, 1, 2]:
                    raise ValueError(f"Invalid power: {total_power}")
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)
                
            return sign * coeff, total_power
        else:
            return sign * coeff, 0
    
    elif 'X' in term.upper():
        if re.search(r'\d+\^[Xx]', term, re.IGNORECASE):
            print("Error: Exponential expressions not allowed")
            sys.exit(1)
        
        var_pattern = r'^([^Xx]*)[Xx]([0-9]*\.?[0-9]*)(\^.*)?$'
        match = re.match(var_pattern, term, re.IGNORECASE)
        
        if match:
            coeff_part = match.group(1) or '1'
            additional_coeff_part = match.group(2) or '1'
            power_part = match.group(3)
            
            if '^' in coeff_part:
                print("Error: Invalid coefficient format")
                sys.exit(1)
            
            if coeff_part == '' or coeff_part == '+':
                coeff = 1
            elif coeff_part == '-':
                coeff = -1
            else:
                try:
                    if coeff_part.startswith('(') and coeff_part.endswith(')'):
                        expr = coeff_part[1:-1]
                        if re.match(r'^[0-9+\-*/.\s]+$', expr):
                            coeff = eval(expr)
                        else:
                            raise ValueError("Invalid expression in parentheses")
                    else:
                        coeff = float(coeff_part)
                except (ValueError, SyntaxError, ZeroDivisionError):
                    print("Error: Invalid coefficient format")
                    sys.exit(1)
            
            if additional_coeff_part and additional_coeff_part != '1':
                try:
                    additional_coeff = float(additional_coeff_part)
                    coeff *= additional_coeff
                except ValueError:
                    print("Error: Invalid coefficient format")
                    sys.exit(1)
            
            if power_part is None:
                power = 1
            else:
                power_expr = power_part[1:]
                try:
                    power = parse_power_expression(power_expr)
                except ValueError as e:
                    print(f"Error: {e}")
                    sys.exit(1)
                
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
        if '^' in term:
            if term.count('^') > 1:
                print("Error: Multiple ^ operators")
                sys.exit(1)
            
            base_and_power = term.split('^', 1)
            base_part = base_and_power[0]
            power_part = base_and_power[1]
            
            if 'X' in power_part.upper():
                print("Error: Variables in exponents not allowed")
                sys.exit(1)
            
            try:
                base = float(base_part)
                power_value = parse_power_expression(power_part)
                result = base ** power_value
                return sign * result, 0
            except (ValueError, TypeError) as e:
                print(f"Error: Invalid number power expression - {e}")
                sys.exit(1)
        else:
            try:
                coeff = float(term) if term else 0
                return sign * coeff, 0
            except ValueError:
                print("Error: Invalid constant term")
                sys.exit(1)
