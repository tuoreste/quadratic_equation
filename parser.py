"""
Polynomial equation parsing module.
Handles parsing of mathematical expressions into coefficient dictionaries.
"""

import re
import sys

"""Split expression into terms while respecting parentheses depth."""
def split_terms_with_parentheses(expression):
    terms = []
    current_term = ""
    paren_depth = 0
    
    for i, char in enumerate(expression):
        if char == '(':
            paren_depth += 1
            current_term += char
        elif char == ')':
            paren_depth -= 1
            current_term += char
        elif char in '+-' and paren_depth == 0:
            if current_term and not re.match(r'^[+\-]*$', current_term):
                terms.append(current_term)
                current_term = char if char == '-' else ""
            else:
                current_term += char
        else:
            current_term += char

    if current_term:
        terms.append(current_term)
    
    return terms

"""Expand distributive multiplication like 2*(x+1) to 2*x+2*1 and remove simple grouping parentheses."""
def expand_distributive(expression):
    
    while True:
        simple_paren_match = re.search(r'\(([^()]+)\)', expression)
        if not simple_paren_match:
            break
            
        full_match = simple_paren_match.group(0)
        inner_expr = simple_paren_match.group(1)
        start_pos = simple_paren_match.start()
        end_pos = simple_paren_match.end()

        has_mult_before = start_pos > 0 and expression[start_pos - 1] == '*'
        has_mult_after = end_pos < len(expression) and expression[end_pos] == '*'
        has_power_before = start_pos > 0 and expression[start_pos - 1] == '^'
        
        if not has_mult_before and not has_mult_after and not has_power_before:
            if not re.search(r'[*/^]', inner_expr) or re.search(r'^[0-9+\-*/.\s*Xx^]+$', inner_expr):
                expression = expression[:start_pos] + inner_expr + expression[end_pos:]
            else:
                break
        else:
            break

    while True:
        match = re.search(r'([^()]*)\*\(([^)]+)\)|\(([^)]+)\)\*([^()]*)', expression)
        if not match:
            break
            
        if match.group(1) is not None:
            coeff_str = match.group(1)
            expr_str = match.group(2)
        else:
            expr_str = match.group(3)
            coeff_str = match.group(4)

        if not re.search(r'[Xx]', expr_str, re.IGNORECASE) and re.match(r'^[0-9+\-*/.\s]+$', expr_str):
            try:
                if re.match(r'^[0-9+\-*/.\s]+$', expr_str):
                    coeff_value = eval(expr_str)
                    if match.group(1) is not None:
                        replacement = f"{coeff_str}*{coeff_value}"
                    else:
                        replacement = f"{coeff_value}*{coeff_str}"
                else:
                    break
            except:
                break
                
            expression = expression[:match.start()] + replacement + expression[match.end():]
            continue
        
        try:
            coeff = float(coeff_str) if coeff_str else 1
        except ValueError:
            print("Error: Invalid coefficient in distributive multiplication")
            sys.exit(1)

        if re.search(r'[*/^]', expr_str):
            print("Error: Complex expressions in parentheses not supported")
            sys.exit(1)

        terms = re.findall(r'[+-]?[^+-]+', expr_str)
        expanded_terms = []
        
        for term in terms:
            term = term.strip()
            if not term:
                continue

            if term.startswith('+'):
                term = term[1:]
                expanded_coeff = coeff
            elif term.startswith('-'):
                term = term[1:]
                expanded_coeff = -coeff
            else:
                expanded_coeff = coeff

            if term == '1' or term == '':
                expanded_terms.append(f"{expanded_coeff}")
            elif 'x' in term.lower():
                if expanded_coeff == 1:
                    expanded_terms.append(f"{term}")
                elif expanded_coeff == -1:
                    expanded_terms.append(f"-{term}")
                else:
                    expanded_terms.append(f"{expanded_coeff}*{term}")
            else:
                try:
                    numeric_val = float(term)
                    result = expanded_coeff * numeric_val
                    expanded_terms.append(f"{result}")
                except ValueError:
                    expanded_terms.append(f"{expanded_coeff}*{term}")

        expanded = ""
        for i, term in enumerate(expanded_terms):
            if i == 0:
                expanded = term
            else:
                if term.startswith('-'):
                    expanded += term
                else:
                    expanded += "+" + term

        expression = expression[:match.start()] + expanded + expression[match.end():]
    
    return expression

"""Parse and evaluate power expressions, ensuring result is an integer."""
def parse_power_expression(expr):
    if not expr:
        return 1

    expr = expr.strip()
    if expr.startswith('(') and expr.endswith(')'):
        expr = expr[1:-1]

    try:
        if re.match(r'^[0-9+\-*/.\s()]+$', expr):
            result = eval(expr)
            if isinstance(result, (int, float)) and result == int(result):
                return int(result)
            else:
                raise ValueError(f"Power must be an integer: {result}")
        else:
            if re.match(r'^-?[0-9]+$', expr):
                return int(expr)
            else:
                raise ValueError(f"Invalid power expression: {expr}")
    except (ValueError, SyntaxError):
        raise ValueError(f"Invalid power expression: {expr}")
