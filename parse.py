import re
import sys

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
            if current_term:
                terms.append(current_term)
            current_term = char if char == '-' else ""
        else:
            current_term += char
    
    # Add the last term
    if current_term:
        terms.append(current_term)
    
    return terms

def parse(equation):
    #protect against multiple '=' and handle errors
    try:
        left, right = equation.split('=')
    except ValueError as e:
        print(f"Error parsing equation, (does your eqn contain one '=' sign?)")
        sys.exit(1)


    def organizeEqn(side):
        side = side.replace(" ", "")  # remove whitespace
        
        # Check for consecutive operator signs (2 or more operators following each other)
        if re.search(r'[+\-*^]{2,}', side):
            print(f"Error: Consecutive operator signs detected. Two or more operators cannot follow each other.")
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
                    raise ValueError(f"Invalid characters spotted, only 0-9, X, ^, +, -, *, /, (, ), . are allowed")
            except ValueError as e:
                print(f"Error parsing term '{term}': {e}")
                sys.exit(1)
            
            # if it is empty after ^ there should be atleast + and number otherwise it is an error
            if re.search(r'\^[\+\-\*/(). ]*$', term):
                print(f"Error parsing term '{term}': Power cannot be empty after '^'")
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
        
        # Handle multiplication in the term (e.g., "x^2*0", "0*x^2", "2*x")
        if '*' in term:
            parts = term.split('*')
            coeff = 1
            power = 0
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
                        
                        # Parse variable coefficient
                        if var_coeff_part == '' or var_coeff_part == '+':
                            var_coeff = 1
                        elif var_coeff_part == '-':
                            var_coeff = -1
                        else:
                            try:
                                var_coeff = float(var_coeff_part)
                            except ValueError:
                                raise ValueError(f"Invalid variable coefficient: {var_coeff_part}")
                        
                        coeff *= var_coeff
                        
                        # Parse power
                        if power_part is None:
                            power = 1
                        else:
                            power_expr = power_part[1:]  # Remove ^
                            power = parse_power_expression(power_expr)
                else:
                    # This part is a number coefficient
                    try:
                        num_coeff = float(part) if part else 1
                        coeff *= num_coeff
                    except ValueError:
                        raise ValueError(f"Invalid coefficient: {part}")
            
            if has_variable:
                # Validate power is 0, 1, or 2
                try:
                    if power not in [0, 1, 2]:
                        raise ValueError(f"Invalid power: {power}. Only powers 0, 1, 2 are allowed.")
                except ValueError as e:
                    print(f"Error parsing term '{term}': {e}")
                    sys.exit(1)
                    
                return sign * coeff, power
            else:
                # No variable, this is a constant term
                return sign * coeff, 0
        
        # Check if term contains variable (X or x) - no multiplication
        elif 'X' in term.upper():
            # First check if this is an exponential expression like "2^x" 
            if re.search(r'\d+\^[Xx]', term, re.IGNORECASE):
                print(f"Error: Exponential expressions like '{term}' are not allowed. Only polynomial expressions are supported.")
                sys.exit(1)
            
            # Split by variable to get coefficient and power parts
            var_pattern = r'([^Xx]*)[Xx](\^.*)?'
            match = re.match(var_pattern, term, re.IGNORECASE)
            
            if match:
                coeff_part = match.group(1) or '1'
                power_part = match.group(2)
                
                # Check if coefficient part contains ^ (which would be invalid)
                if '^' in coeff_part:
                    print(f"Error: Invalid term format '{term}'. Exponential expressions in coefficients are not supported.")
                    sys.exit(1)
                
                # Parse coefficient
                if coeff_part == '' or coeff_part == '+':
                    coeff = 1
                elif coeff_part == '-':
                    coeff = -1
                else:
                    try:
                        coeff = float(coeff_part)
                    except ValueError:
                        raise ValueError(f"Invalid coefficient: {coeff_part}")
                
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
                            raise ValueError(f"Invalid power: {power}. Only powers 0, 1, 2 are allowed.")
                    except ValueError as e:
                        print(f"Error parsing term '{term}': {e}")
                        sys.exit(1)

                return sign * coeff, power
            else:
                raise ValueError(f"Invalid term format: {term}")
        else:
            # Handle constant terms and number powers (e.g., "2^3", "5")
            if '^' in term:
                # Check if this is a number raised to a power
                base_and_power = term.split('^', 1)
                base_part = base_and_power[0]
                power_part = base_and_power[1]
                
                # Check if power contains variable - this is invalid (exponential, not polynomial)
                if 'X' in power_part.upper():
                    print(f"Error: Exponential expressions like '{term}' are not allowed. Only polynomial expressions are supported.")
                    sys.exit(1)
                
                try:
                    base = float(base_part)
                    # Parse and evaluate the power expression
                    power_value = parse_power_expression(power_part)
                    result = base ** power_value
                    return sign * result, 0
                except ValueError as e:
                    raise ValueError(f"Invalid number power expression: {term}")
            else:
                # Simple constant term (power 0)
                try:
                    coeff = float(term) if term else 0
                    return sign * coeff, 0
                except ValueError:
                    raise ValueError(f"Invalid constant term")
    
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

    print("Left side terms:", organizeEqn(left))
    print("Right side terms:", organizeEqn(right))


def main():
    if len(sys.argv) != 2:
        print("Usage format: ./parse.py \"equation\"")
        sys.exit(1)

    parse(sys.argv[1])
    # equation = sys.argv[1]
    # coeffs = parse_equation(equation)

    # print("Reduced form:", reduce_form(coeffs), "= 0")
    # deg = degree(coeffs)
    # print("Polynomial degree:", deg)

    # solve(coeffs)


if __name__ == "__main__":
    main()