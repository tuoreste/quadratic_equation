#!/usr/bin/env python3
"""
Comprehensive test cases for the quadratic equation solver.
This script tests parsing, solving, and various edge cases.
"""

import subprocess
import sys
import os

def run_test(equation, expected_result=None, should_fail=False, description="", expected_degree=None):
    """Run a single test case"""
    print(f"\n{'='*80}")
    print(f"Test: {description}")
    print(f"Equation: {equation}")
    print(f"Expected: {'Should fail' if should_fail else 'Should pass'}")
    if expected_degree is not None:
        print(f"Expected degree: {expected_degree}")
    print("-" * 80)
    
    try:
        result = subprocess.run([sys.executable, "computor.py", equation], 
                               capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            if should_fail:
                print("❌ UNEXPECTED PASS - This should have failed!")
                print("Output:")
                print(result.stdout)
            else:
                print("✅ PASS")
                print("Output:")
                print(result.stdout.strip())
                
                # Check if expected degree matches
                if expected_degree is not None:
                    output_lines = result.stdout.strip().split('\n')
                    for line in output_lines:
                        if line.startswith("Polynomial degree:"):
                            actual_degree = int(line.split(":")[1].strip())
                            if actual_degree == expected_degree:
                                print(f"✅ Degree check: Expected {expected_degree}, got {actual_degree}")
                            else:
                                print(f"❌ Degree mismatch: Expected {expected_degree}, got {actual_degree}")
                            break
        else:
            if should_fail:
                print("✅ EXPECTED FAILURE")
                print("Error:")
                print(result.stdout.strip() or result.stderr.strip())
            else:
                print("❌ UNEXPECTED FAILURE")
                print("Error:")
                print(result.stdout.strip() or result.stderr.strip())
    
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT - Test took too long")
    except Exception as e:
        print(f"🔥 EXCEPTION: {e}")

def run_comprehensive_tests():
    """Run all test categories"""
    
    # Test each category separately for better organization
    test_basic_quadratic_cases()
    test_linear_cases()
    test_constant_cases()
    test_parsing_features()
    test_reported_issues()
    test_error_cases()
    test_edge_cases()
    test_complex_equations()

def test_basic_quadratic_cases():
    """Test standard quadratic equations with different discriminant scenarios"""
    print(f"\n{'🟢 QUADRATIC EQUATIONS (DEGREE 2)':=^80}")
    
    # Perfect square (discriminant = 0)
    run_test("x^2 + 2*x + 1 = 0", 
            description="Perfect square (x+1)^2", 
            expected_degree=2)
    
    # Two real solutions (discriminant > 0)
    run_test("x^2 - 3*x + 2 = 0", 
            description="Two real solutions (x=1, x=2)", 
            expected_degree=2)
    
    run_test("x^2 - 5*x + 6 = 0", 
            description="Two real solutions (x=2, x=3)", 
            expected_degree=2)
    
    # No real solutions (discriminant < 0)
    run_test("x^2 + x + 1 = 0", 
            description="No real solutions (complex roots)", 
            expected_degree=2)
    
    run_test("x^2 + 2*x + 5 = 0", 
            description="No real solutions (complex roots)", 
            expected_degree=2)
    
    # Quadratic with different coefficients
    run_test("2*x^2 + 4*x + 2 = 0", 
            description="Quadratic with coefficient 2", 
            expected_degree=2)
    
    run_test("-x^2 + 4*x - 4 = 0", 
            description="Negative leading coefficient", 
            expected_degree=2)
    
    run_test("0.5*x^2 + x + 0.5 = 0", 
            description="Decimal coefficients", 
            expected_degree=2)

def test_linear_cases():
    """Test linear equations"""
    print(f"\n{'🟡 LINEAR EQUATIONS (DEGREE 1)':=^80}")
    
    run_test("x + 2 = 0", 
            description="Simple linear equation", 
            expected_degree=1)
    
    run_test("2*x - 4 = 0", 
            description="Linear with coefficient", 
            expected_degree=1)
    
    run_test("-3*x + 6 = 0", 
            description="Negative coefficient", 
            expected_degree=1)
    
    run_test("x = 5", 
            description="Direct assignment", 
            expected_degree=1)
    
    run_test("5 = x", 
            description="Reversed assignment", 
            expected_degree=1)
    
    run_test("0.5*x + 1.5 = 0", 
            description="Decimal linear equation", 
            expected_degree=1)

def test_constant_cases():
    """Test constant equations"""
    print(f"\n{'🔵 CONSTANT EQUATIONS (DEGREE 0)':=^80}")
    
    run_test("5 = 5", 
            description="True statement (infinite solutions)", 
            expected_degree=0)
    
    run_test("0 = 0", 
            description="Zero equals zero (infinite solutions)", 
            expected_degree=0)
    
    run_test("3 = 5", 
            description="False statement (no solution)", 
            expected_degree=0)
    
    run_test("2 + 3 = 5", 
            description="Arithmetic equality (infinite solutions)", 
            expected_degree=0)

def test_parsing_features():
    """Test advanced parsing features"""
    print(f"\n{'🟡 PARSING FEATURES':=^80}")
    
    # Multiplication cases
    run_test("x^1*x^0 = 2", 
            description="Basic multiplication x^1*x^0", 
            expected_degree=1)
    
    run_test("x^2*x^0 = 5", 
            description="x^2*x^0 should equal x^2", 
            expected_degree=2)
    
    run_test("2*x*3 = 6", 
            description="Coefficient multiplication", 
            expected_degree=1)
    
    # Implicit multiplication
    run_test("3x^2 = 12", 
            description="3x^2 implicit multiplication", 
            expected_degree=2)
    
    run_test("2x + 3 = 0", 
            description="Implicit multiplication in linear term", 
            expected_degree=1)
    
    # Power expressions
    run_test("x^(1+1) = 4", 
            description="Power in parentheses x^(1+1)", 
            expected_degree=2)
    
    run_test("x^(2-0) = 9", 
            description="Subtraction in power", 
            expected_degree=2)
    
    # Zero handling
    run_test("0*x^2 + x = 5", 
            description="Zero coefficient eliminates x^2 term", 
            expected_degree=1)
    
    run_test("x^0 = 1", 
            description="x^0 should equal 1 (constant)", 
            expected_degree=0)
    
    # Sign handling
    run_test("--x = 5", 
            description="Double negative equals positive", 
            expected_degree=1)
    
    run_test("-x^2 - x - 1 = 0", 
            description="All negative coefficients", 
            expected_degree=2)
    
    # Complex expressions
    run_test("x^2 + 2*x - x^2 = 3", 
            description="Terms cancel to linear", 
            expected_degree=1)
    
    run_test("2*x^2 - x^2 + x = 5", 
            description="Combining like terms", 
            expected_degree=2)

def test_reported_issues():
    """Test specific issues reported by users"""
    print(f"\n{'🔍 REPORTED ISSUES':=^80}")
    
    # Issues with reduced form display and solving
    run_test("(1/2)*x^2 + x = 0", 
            description="Fractional coefficient parsing", 
            expected_degree=2)
    
    run_test("x^(2*1) + x^(3-2) + x^(1*0) = 6", 
            description="Complex power expressions in parentheses", 
            expected_degree=2)
    
    # Sign handling edge cases
    run_test("x^2 + 2*x + 1 = 0", 
            description="Perfect square for reduced form check", 
            expected_degree=2)
    
    # Coefficient of 1 handling
    run_test("1*x^2 + 1*x + 1 = 0", 
            description="Explicit coefficient of 1", 
            expected_degree=2)
    
    run_test("-1*x^2 - 1*x - 1 = 0", 
            description="Explicit coefficient of -1", 
            expected_degree=2)

def test_error_cases():
    """Test cases that should fail"""
    print(f"\n{'🔴 ERROR CASES (Should Fail)':=^80}")
    
    # Invalid powers
    run_test("x^3 = 8", 
            should_fail=True, 
            description="Power 3 not allowed")
    
    run_test("x^(-1) = 2", 
            should_fail=True, 
            description="Negative power")
    
    run_test("x^4 + x^2 = 0", 
            should_fail=True, 
            description="Power 4 not allowed")
    
    run_test("x^2.5 = 4", 
            should_fail=True, 
            description="Decimal power")
    
    run_test("0.5 * X^2 - 0.5 * X^1.5 = 0", 
            should_fail=True, 
            description="Decimal power X^1.5 should fail")
    
    # Exponential expressions
    run_test("2^x = 4", 
            should_fail=True, 
            description="Exponential 2^x")
    
    run_test("x^x = 4", 
            should_fail=True, 
            description="Variable in exponent")
    
    # Operator errors
    run_test("x^2 ++ x = 0", 
            should_fail=False, 
            description="Double plus")
    
    run_test("x^2 + = 0", 
            should_fail=True, 
            description="Trailing operator")
    
    run_test("x^2 ** x = 0", 
            should_fail=True, 
            description="Double multiplication")
    
    run_test("0.5 * X^2 -*- 0.5 * X^1 = 0", 
            should_fail=True, 
            description="Invalid operator sequence -*-")
    
    run_test("X^0 + X^^0 = 2", 
            should_fail=True, 
            description="Double exponent operator ^^")
    
    run_test("X^0 + X^0 = 2+", 
            should_fail=True, 
            description="Trailing operator after equals")
    
    # Parentheses errors
    run_test("x^(2+1 = 0", 
            should_fail=True, 
            description="Unmatched opening parenthesis")
    
    run_test("x^2+1) = 0", 
            should_fail=True, 
            description="Unmatched closing parenthesis")
    
    # Invalid characters and variables
    run_test("x^2 + y = 0", 
            should_fail=True, 
            description="Wrong variable name (y)")
    
    run_test("0.5 * X^2 - 0.5 * Y^1 = 0", 
            should_fail=True, 
            description="Wrong variable Y should fail")
    
    run_test("x^2 + 3@ = 0", 
            should_fail=True, 
            description="Invalid character @")
    
    run_test("x^2 + 1/x = 0", 
            should_fail=True, 
            description="Variable in denominator")
    
    # Equation format errors
    run_test("x^2 + x", 
            should_fail=True, 
            description="Missing equals sign")
    
    run_test("x^2 = x = 0", 
            should_fail=True, 
            description="Multiple equals signs")
    
    run_test("", 
            should_fail=True, 
            description="Empty equation")
    
    # High power multiplication
    run_test("x^1*x^2 = 0", 
            should_fail=True, 
            description="x^1*x^2 = x^3 (invalid)")
    
    run_test("x*x*x = 0", 
            should_fail=True, 
            description="x*x*x = x^3 (invalid)")

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print(f"\n{'🟠 EDGE CASES':=^80}")
    
    # Very small coefficients
    run_test("0.000001*x^2 + x = 0", 
            description="Very small coefficient", 
            expected_degree=2)
    
    # Large coefficients
    run_test("1000000*x^2 + x = 0", 
            description="Large coefficient", 
            expected_degree=2)
    
    # Mixed signs and double negatives
    run_test("x^2 + -x + -1 = 0", 
            description="Plus negative terms", 
            expected_degree=2)
    
    run_test("0.5 * X^2 -- 0.5 * X^1 = 0", 
            description="Double negative should become positive", 
            expected_degree=2)
    
    # Many terms that cancel
    run_test("x^2 + x^2 - x^2 - x^2 + x = 5", 
            description="Terms that cancel out", 
            expected_degree=1)
    
    # Zero coefficient cases
    run_test("X^2 * 0 - 1*X^1 = 2", 
            description="X^2 with zero coefficient", 
            expected_degree=1)
    
    run_test("0 * X^2 - 1*X^1 = 2", 
            description="Zero coefficient at start", 
            expected_degree=1)
    
    # Multiplication with constants
    run_test("X^1 * X^0 = 2", 
            description="X^1 * X^0 multiplication", 
            expected_degree=1)
    
    run_test("X^1 * 1 - X^0 = 2", 
            description="X^1 * 1 coefficient", 
            expected_degree=1)
    
    # Fractional coefficients using parentheses
    run_test("(1/2)*x^2 + x = 0", 
            description="Fractional coefficient (1/2)", 
            expected_degree=2)
    
    # Complex reduced forms
    run_test("X^0 + X^0 = 2", 
            description="Multiple X^0 terms", 
            expected_degree=0)
    
    # Spacing variations
    run_test(" 0.5 * X^2 - 0.5 * X^1 = 0 ", 
            description="Extra spaces around equation", 
            expected_degree=2)

def test_complex_equations():
    """Test complex but valid equations"""
    print(f"\n{'🟢 COMPLEX VALID CASES':=^80}")
    
    run_test("-2*x^2 + 3*x - 1 = 0", 
            description="Complex quadratic with all terms", 
            expected_degree=2)
    
    run_test("x^2 - 2*x + 1 - x^2 + 2*x = 1", 
            description="Complex equation that simplifies to constant", 
            expected_degree=0)
    
    run_test("3*x^2 + 2*x^1*x^0 - 5*x^2 + x = 7", 
            description="Mixed notation with simplification", 
            expected_degree=2)
    
    run_test("x^(2*1) + x^(3-2) + x^(1*0) = 6", 
            description="Complex power expressions", 
            expected_degree=2)

def main():
    print("🧪 COMPREHENSIVE TEST SUITE FOR QUADRATIC EQUATION SOLVER")
    print("=" * 80)
    print("Testing parsing, reduced form display, and quadratic solving functionality")
    print("=" * 80)
    
    # Run all test categories
    run_comprehensive_tests()
    
    print(f"\n{'🏁 TEST SUITE COMPLETE':=^80}")
    print("All test categories have been executed.")
    print("Review the results above to identify any issues.")
    print("=" * 80)

if __name__ == "__main__":
    main()
