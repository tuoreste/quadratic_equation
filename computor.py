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

def split_terms_with_parentheses(expression):
    """Split expression into terms while respecting parentheses"""
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
            # Only split on + or - when not inside parentheses
            # Don't split if this is the start of the expression or if the current term is empty/just operators
            if current_term and not re.match(r'^[+\-]*$', current_term):
                terms.append(current_term)
                current_term = char if char == '-' else ""
            else:
                # This + or - is part of the coefficient, not a separator
                current_term += char
        else:
            current_term += char
    
    # Add the last term
    if current_term:
        terms.append(current_term)
    
    return terms

def parse_equation(equation):
    #protect against multiple '=' and handle errors
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

    def expand_distributive(expression):
        """Expand simple distributive multiplication like 2*(x+1) to 2*x+2*1"""
        # Handle patterns like coeff*(term1+term2) or (term1+term2)*coeff
        while True:
            # Look for distributive patterns
            match = re.search(r'([^()]*)\*\(([^)]+)\)|\(([^)]+)\)\*([^()]*)', expression)
            if not match:
                break
                
            if match.group(1) is not None:
                # Pattern: coeff*(expression)
                coeff_str = match.group(1)
                expr_str = match.group(2)
            else:
                # Pattern: (expression)*coeff
                expr_str = match.group(3)
                coeff_str = match.group(4)
            
            # Check if this is actually a simple coefficient in parentheses (like (1/2))
            # If expr_str contains only arithmetic operations and no variables, treat as coefficient
            if not re.search(r'[Xx]', expr_str, re.IGNORECASE) and re.match(r'^[0-9+\-*/.\s]+$', expr_str):
                # This is a coefficient in parentheses, not distributive multiplication
                # Just remove the parentheses and let normal parsing handle it
                if match.group(1) is not None:
                    # Pattern: something*(arithmetic_expression)
                    replacement = f"{coeff_str}*({expr_str})"
                else:
                    # Pattern: (arithmetic_expression)*something
                    replacement = f"({expr_str})*{coeff_str}"
                
                # Replace parentheses with the expression itself since it's just a coefficient
                try:
                    # Evaluate the arithmetic expression safely
                    if re.match(r'^[0-9+\-*/.\s]+$', expr_str):
                        coeff_value = eval(expr_str)
                        if match.group(1) is not None:
                            replacement = f"{coeff_str}*{coeff_value}"
                        else:
                            replacement = f"{coeff_value}*{coeff_str}"
                    else:
                        # Keep as is and let other parsing handle it
                        break
                except:
                    # If evaluation fails, keep as is
                    break
                    
                expression = expression[:match.start()] + replacement + expression[match.end():]
                continue
            
            # Parse coefficient
            try:
                coeff = float(coeff_str) if coeff_str else 1
            except ValueError:
                print("Error: Invalid coefficient in distributive multiplication")
                sys.exit(1)
            
            # Check for complex expressions (variables with operators)
            if re.search(r'[*/^]', expr_str):
                print("Error: Complex expressions in parentheses not supported")
                sys.exit(1)
            
            # Split expression by + and - while preserving signs
            terms = re.findall(r'[+-]?[^+-]+', expr_str)
            
            # Expand each term
            expanded_terms = []
            for term in terms:
                term = term.strip()
                if not term:
                    continue
                
                # Handle signs
                if term.startswith('+'):
                    term = term[1:]
                    expanded_coeff = coeff
                elif term.startswith('-'):
                    term = term[1:]
                    expanded_coeff = -coeff
                else:
                    expanded_coeff = coeff
                
                # Create expanded term
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
                    # Numeric term
                    try:
                        numeric_val = float(term)
                        result = expanded_coeff * numeric_val
                        expanded_terms.append(f"{result}")
                    except ValueError:
                        expanded_terms.append(f"{expanded_coeff}*{term}")
            
            # Join expanded terms
            expanded = ""
            for i, term in enumerate(expanded_terms):
                if i == 0:
                    expanded = term
                else:
                    if term.startswith('-'):
                        expanded += term
                    else:
                        expanded += "+" + term
            
            # Replace the original expression with expanded version
            expression = expression[:match.start()] + expanded + expression[match.end():]
        
        return expression

    def organizeEqn(side):
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
    
    def parse_term(term):
        """Parse a single term to extract coefficient and power"""
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
                            part_power = parse_power_expression(power_expr)
                        
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
                    power = parse_power_expression(power_expr)
                    
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
                    if power_value is None:
                        raise ValueError("Power expression evaluated to None")
                    result = base ** power_value
                    return sign * result, 0
                except (ValueError, TypeError) as e:
                    print("Error: Invalid number power expression")
                    sys.exit(1)
            else:
                # Simple constant term (power 0)
                try:
                    coeff = float(term) if term else 0
                    return sign * coeff, 0
                except ValueError:
                    print("Error: Invalid constant term")
                    sys.exit(1)
    
    def parse_power_expression(expr):
        """Parse power expression, handling brackets and simple expressions"""
        if not expr:
            return 1
            
        # Remove brackets if present
        expr = expr.strip()
        if expr.startswith('(') and expr.endswith(')'):
            expr = expr[1:-1]
        
        # Evaluate simple power expressions
        try:
            # For safety, only allow simple arithmetic operations
            if re.match(r'^[0-9+\-*/\s()]+$', expr):
                result = eval(expr)
                if isinstance(result, (int, float)) and result == int(result):
                    return int(result)
                else:
                    raise ValueError(f"Power must be an integer: {result}")
            else:
                # Try to parse as simple integer
                # case: -x^(2+1)=-x with this power it should be valid
                if re.match(r'^-?[0-9]+$', expr):
                    return int(expr)
        except (ValueError, SyntaxError):
            raise ValueError(f"Invalid power expression: {expr}")

    left_terms = organizeEqn(left)
    right_terms = organizeEqn(right)
    
    # Move right side terms to left (subtract right side from left side)
    coeffs = {}
    
    # Add left side terms
    for power, coeff in left_terms.items():
        coeffs[power] = coeffs.get(power, 0) + coeff
    
    # Subtract right side terms  
    for power, coeff in right_terms.items():
        coeffs[power] = coeffs.get(power, 0) - coeff
    
    return coeffs


def reduce_form(coeffs):
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
