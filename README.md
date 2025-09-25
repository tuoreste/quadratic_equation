# Polynomial Equation Solver

## Overview
A comprehensive Python program that parses and solves polynomial equations up to degree 2 (quadratic equations). Features robust equation parsing with validation, distributive multiplication support, parentheses handling, and precise mathematical solutions.

## Quick Start

```bash
python3 computor.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
```

**Output:**
```
Reduced form:  - 9.3 * X^2 + 4 * X + 4 = 0
Polynomial degree: 2
Discriminant is strictly positive, the two solutions are:
-0.47849462365591394
0.9086021505376343
```

## Features

- ✅ **Advanced Parsing**: Distributive multiplication, parentheses, implicit coefficients
- ✅ **Comprehensive Validation**: Error checking for malformed expressions
- ✅ **Multiple Equation Types**: Linear (degree 1), quadratic (degree 2), constant (degree 0)
- ✅ **Complex Solutions**: Full support for imaginary number results
- ✅ **Flexible Input**: Decimal coefficients, various formatting styles
- ✅ **Identity Equations**: Handles cases like "2 = 2" (all real numbers solution)
- ✅ **Modular Architecture**: Clean, organized codebase with separate modules
- ⚠️ **Limitation**: Degree > 2 equations not supported

## Usage
```bash
python computor.py "equation"
```

## Input Format

The program accepts polynomial equations with flexible syntax:

```
coefficient * X^power + ... = coefficient * X^power + ...
```

**Examples of valid equations:**
```bash
python3 computor.py "5*X^2 + 4*X^1 + 3*X^0 = 0"
python3 computor.py "X^2 - 2*X + 1 = 0" 
python3 computor.py "2.5*X^2 = 3*X^1 + 1"
python3 computor.py "42*X^0 = 42*X^0"
python3 computor.py "2*(X+1) - 3 = 0"
python3 computor.py "(2/3)*X^2 + X = 5"
```

**Advanced Features:**
- **Distributive Multiplication**: `2*(X+1)` → `2*X + 2`
- **Parentheses Support**: Grouping and power expressions `X^(2+1)`
- **Implicit Coefficients**: `X^2` = `1*X^2`, `-X` = `-1*X^1`
- **Flexible Formatting**: Spaces optional, multiple term arrangements
- **Arithmetic in Coefficients**: `(1/2)*X^2`, `2^3*X^1`

**Rules:**
- Variables must be `X` (case insensitive: `x` or `X`)
- Powers: 0, 1, or 2 only (explicit: `X^0`, `X^1`, `X^2`)
- Both equation sides required (separated by `=`)
- No variables in denominators or exponents

## Algorithm

1. **Parse and Validate**: Advanced parsing with distributive expansion and error checking
2. **Term Organization**: Extract coefficients and powers, handle implicit multiplication
3. **Equation Reduction**: Move all terms to left side, combine like terms
4. **Degree Determination**: Find highest non-zero power (tolerance: 1e-12)
5. **Solution Application**: Apply appropriate method based on polynomial degree

### Solution Methods

| Degree | Type | Method |
|--------|------|--------|
| 0 | Constant | Check if contradiction or identity |
| 1 | Linear | x = -b/a |
| 2 | Quadratic | Quadratic formula with discriminant analysis |
| >2 | Higher-order | Not supported |

### Quadratic Solutions (ax² + bx + c = 0)

- **Discriminant Δ = b² - 4ac**
  - **Δ > 0**: Two distinct real solutions
  - **Δ = 0**: One repeated real solution  
  - **Δ < 0**: Two complex conjugate solutions

## Examples

### Identity Equation
```bash
$ python3 computor.py "2 = 2"
Reduced form: 0 = 0
Polynomial degree: 0
All real numbers are solution.
```

### Linear Equation
```bash
$ python3 computor.py "2*X^1 + 4 = 0"
Reduced form: 2 * X + 4 = 0
Polynomial degree: 1
The solution is:
-2.0
```

### Quadratic with Real Solutions
```bash
$ python3 computor.py "X^2 - 5*X + 6 = 0"
Reduced form: X^2 - 5 * X + 6 = 0
Polynomial degree: 2
Discriminant is strictly positive, the two solutions are:
3.0
2.0
```

### Quadratic with Complex Solutions
```bash
$ python3 computor.py "X^2 + 1 = 0"
Reduced form: X^2 + 1 = 0
Polynomial degree: 2
Discriminant is strictly negative, no real solution.
0.0 + 1.0i
0.0 - 1.0i
```

### Distributive Multiplication
```bash
$ python3 computor.py "2*(X+1) = 6"
Reduced form: 2 * X - 4 = 0
Polynomial degree: 1
The solution is:
2.0
```

## Implementation Details

### Modular Architecture

The codebase is organized into focused modules:

- **`computor.py`**: Main entry point and command-line interface
- **`equation_parser.py`**: Main equation parsing and validation logic
- **`parser.py`**: Basic parsing utilities and distributive expansion
- **`term_parser.py`**: Individual term parsing with comprehensive validation
- **`solver.py`**: Polynomial solving and output formatting
- **`math_utils.py`**: Custom mathematical functions (sqrt, abs)

### Core Functions

- **`parse_equation()`**: Comprehensive equation parsing with validation
- **`expand_distributive()`**: Handles expressions like `2*(X+1)` → `2*X+2`
- **`parse_term()`**: Extracts coefficients and powers from individual terms
- **`reduce_form()`**: Converts coefficient dictionary to readable polynomial string
- **`solve()`**: Applies appropriate solution method based on degree

### Advanced Error Handling

- **Syntax Validation**: Comprehensive checking for malformed expressions
- **Parentheses Balancing**: Ensures proper opening/closing parentheses
- **Operator Validation**: Detects consecutive operators and trailing operators
- **Power Constraints**: Enforces polynomial degree limits (0, 1, 2)
- **Division Safety**: Prevents variables in denominators
- **Expression Complexity**: Limits unsupported mathematical operations

### Dependencies
- **Standard Library**: `re`, `sys` (no external dependencies)
- **Custom Mathematics**: Newton's method square root implementation

## Testing

The project includes a comprehensive test suite to validate all functionality:

### Running Tests

```bash
python3 test_cases.py
```

### Test Categories

The test suite covers:

- **🟢 Quadratic Equations**: Perfect squares, real solutions, complex solutions
- **🟡 Linear Equations**: Simple and complex linear cases
- **🔵 Constant Equations**: Identity cases (`2 = 2`) and contradictions (`3 = 5`)
- **🟡 Parsing Features**: Multiplication, implicit coefficients, power expressions
- **🔍 Reported Issues**: User-reported edge cases and fixes
- **🔴 Error Cases**: Invalid syntax that should fail gracefully
- **🟠 Edge Cases**: Boundary conditions and special scenarios
- **🟢 Complex Valid Cases**: Advanced equations with multiple features

### Example Test Output

```bash
$ python3 test_cases.py

================================================================================
Test: Simple linear equation
Equation: x + 2 = 0
Expected: Should pass
Expected degree: 1
--------------------------------------------------------------------------------
✅ PASS
Output:
Reduced form: X + 2 = 0
Polynomial degree: 1
The solution is:
-2.0
✅ Degree check: Expected 1, got 1
```

### Manual Testing

You can also test individual equations manually:

```bash
python3 computor.py "your_equation_here"
```