# Polynomial Equation Solver

## Overview
A Python program that solves polynomial equations up to degree 2 (quadratic equations). The program parses polynomial equations in standard form, reduces them to canonical form, determines the polynomial degree, and provides appropriate solutions.

## Quick Start

```bash
python computor.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
```

**Output:**
```
Reduced form: 4 * X^0 + 4 * X^1 + -9.3 * X^2 = 0
Polynomial degree: 2
Discriminant is strictly positive, the two solutions are:
-0.475131
0.905239
```

## Features

- ✅ Solves linear equations (degree 1)
- ✅ Solves quadratic equations (degree 2) 
- ✅ Handles complex solutions
- ✅ Automatic equation parsing and reduction
- ✅ Support for decimal coefficients
- ⚠️ Degree > 2 equations not supported

## Usage
```bash
python computor.py "equation"
```

## Input Format

The program accepts polynomial equations with the following syntax:

```
coefficient * X^power + ... = coefficient * X^power + ...
```

**Examples of valid equations:**
```bash
python computor.py "5*X^2 + 4*X^1 + 3*X^0 = 0"
python computor.py "X^2 - 2*X + 1 = 0" 
python computor.py "2.5*X^2 = 3*X^1 + 1"
python computor.py "42*X^0 = 42*X^0"
```

**Rules:**
- Variables must be `X` (case-sensitive)
- Powers must be explicit: `X^0`, `X^1`, `X^2`
- Coefficients can be integers or decimals
- Multiplication symbol `*` is optional between coefficient and variable
- Both sides of equation are required (separated by `=`)

## Algorithm

## Algorithm

1. **Parse equation** using regex to extract coefficients and powers
2. **Move all terms to left side** (subtract right side from left)
3. **Combine like terms** to get canonical form
4. **Determine polynomial degree** (highest non-zero power)
5. **Apply appropriate solution method** based on degree

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

### Linear Equation
```bash
$ python computor.py "2*X^1 + 4 = 0"
Reduced form: 4 * X^0 + 2 * X^1 = 0
Polynomial degree: 1
The solution is:
-2.0
```

### Quadratic with Real Solutions
```bash
$ python computor.py "X^2 - 5*X + 6 = 0"
Reduced form: 6 * X^0 + -5 * X^1 + 1 * X^2 = 0
Polynomial degree: 2
Discriminant is strictly positive, the two solutions are:
3.0
2.0
```

### Quadratic with Complex Solutions
```bash
$ python computor.py "X^2 + 1 = 0"
Reduced form: 1 * X^0 + 1 * X^2 = 0
Polynomial degree: 2
Discriminant is strictly negative, no real solution.
0.0 + 1.0i
0.0 - 1.0i
```

## Implementation Details

### Core Functions

- **`parse_equation()`**: Uses regex `([+-]?\d*\.?\d*)\*?X\^(\d+)` to extract coefficient-power pairs
- **`reduce_form()`**: Converts coefficient dictionary to human-readable polynomial string
- **`degree()`**: Finds highest power with non-zero coefficient (tolerance: 1e-12)
- **`solve()`**: Applies degree-appropriate solution method

### Error Handling

- **Missing arguments**: Shows usage format
- **Malformed equations**: May produce unexpected results (limited validation)
- **Division by zero**: Not explicitly handled (would raise Python exception)
- **Degree > 2**: Shows "can't solve" message

### Dependencies
```python
import re          # Regex parsing
import sys         # Command-line arguments  
import math        # sqrt() for quadratic formula
from fractions import Fraction  # Imported but unused
```