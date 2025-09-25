#!/usr/bin/env python3
"""
Comprehensive test cases for the quadratic equation parser.
This script tests various edge cases and potential failure scenarios.
"""

import subprocess
import sys
import os

def run_test(equation, expected_result=None, should_fail=False, description=""):
    """Run a single test case"""
    print(f"\n{'='*60}")
    print(f"Test: {description}")
    print(f"Equation: {equation}")
    print(f"Expected: {'Should fail' if should_fail else 'Should pass'}")
    print("-" * 60)
    
    try:
        result = subprocess.run([sys.executable, "parse.py", equation], 
                               capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            if should_fail:
                print("❌ UNEXPECTED PASS - This should have failed!")
                print("Output:", result.stdout)
            else:
                print("✅ PASS")
                print("Output:", result.stdout.strip())
        else:
            if should_fail:
                print("✅ EXPECTED FAILURE")
                print("Error:", result.stdout.strip() or result.stderr.strip())
            else:
                print("❌ UNEXPECTED FAILURE")
                print("Error:", result.stdout.strip() or result.stderr.strip())
    
    except subprocess.TimeoutExpired:
        print("⏰ TIMEOUT - Test took too long")
    except Exception as e:
        print(f"🔥 EXCEPTION: {e}")

def main():
    print("🧪 COMPREHENSIVE TEST SUITE FOR QUADRATIC EQUATION PARSER")
    print("=" * 60)
    
    # First, uncomment the print statements in parse.py
    print("Note: Make sure the print statements in parse.py are uncommented for these tests!")
    
    # 1. BASIC VALID CASES
    print("\n🟢 BASIC VALID CASES")
    run_test("x^2 + 2*x + 1 = 0", description="Standard quadratic")
    run_test("x = 5", description="Simple linear equation")
    run_test("5 = x", description="Reversed linear equation")
    run_test("x^2 = 4", description="Pure quadratic")
    run_test("2*x^2 - 3*x + 1 = 0", description="Standard form with coefficients")
    
    # 2. MULTIPLICATION EDGE CASES
    print("\n🟡 MULTIPLICATION CASES")
    run_test("x^1*x^0 = 2", description="Basic multiplication x^1*x^0")
    run_test("x^2*x^0 = 5", description="x^2*x^0 should equal x^2")
    run_test("x^0*x^1 = 3", description="Reverse order x^0*x^1")
    run_test("2*x*3 = 6", description="Coefficient multiplication")
    run_test("x*2*x = 4", description="Mixed multiplication")
    
    # 3. IMPLICIT MULTIPLICATION
    print("\n🟡 IMPLICIT MULTIPLICATION CASES")
    run_test("21x2 = 42", description="21x2 should be 21*x*2 = 42x")
    run_test("3x^2 = 12", description="3x^2 implicit multiplication")
    run_test("x5 = 10", description="x5 should be 5x")
    
    # 4. PARENTHESES CASES
    print("\n🟡 PARENTHESES CASES")
    run_test("x^(1+1) = 4", description="Power in parentheses")
    run_test("x^(2-1) = 3", description="Subtraction in power")
    run_test("2*(x+1) = 6", should_fail=True, description="Parentheses in coefficients (not supported)")
    
    # 5. EDGE CASES WITH ZEROS
    print("\n🟡 ZERO CASES")
    run_test("0*x^2 + x = 5", description="Zero coefficient")
    run_test("x^0 = 1", description="x^0 should equal 1")
    run_test("0 = 0", description="Zero equals zero")
    run_test("x*0 = 0", description="Variable times zero")
    
    # 6. SIGN HANDLING
    print("\n🟡 SIGN CASES")
    run_test("-x^2 + x = 0", description="Negative leading coefficient")
    run_test("x^2 + -x = 0", description="Plus negative")
    run_test("--x = 0", should_fail=True, description="Double negative (should fail)")
    run_test("+-x = 0", should_fail=True, description="Plus minus (should fail)")
    
    # 7. INVALID POWER CASES
    print("\n🔴 INVALID POWER CASES (Should Fail)")
    run_test("x^3 = 8", should_fail=True, description="Power 3 not allowed")
    run_test("x^(-1) = 2", should_fail=True, description="Negative power")
    run_test("x^4 + x^2 = 0", should_fail=True, description="Power 4 not allowed")
    run_test("x^2.5 = 4", should_fail=True, description="Decimal power")
    
    # 8. EXPONENTIAL EXPRESSIONS (Should Fail)
    print("\n🔴 EXPONENTIAL CASES (Should Fail)")
    run_test("2^x = 4", should_fail=True, description="Exponential 2^x")
    run_test("3^x^2 = 9", should_fail=True, description="Complex exponential")
    run_test("x^x = 4", should_fail=True, description="Variable in exponent")
    
    # 9. OPERATOR ERRORS
    print("\n🔴 OPERATOR ERROR CASES (Should Fail)")
    run_test("x^2 ++ x = 0", should_fail=True, description="Double plus")
    run_test("x^2 + = 0", should_fail=True, description="Trailing operator")
    run_test("= x^2", should_fail=True, description="Leading equals")
    run_test("x^2 ** x = 0", should_fail=True, description="Double multiplication")
    run_test("x^^ = 0", should_fail=True, description="Double exponent")
    
    # 10. PARENTHESES ERRORS
    print("\n🔴 PARENTHESES ERROR CASES (Should Fail)")
    run_test("x^(2+1 = 0", should_fail=True, description="Unmatched opening parenthesis")
    run_test("x^2+1) = 0", should_fail=True, description="Unmatched closing parenthesis")
    run_test("x^((2)) = 0", should_fail=True, description="Nested parentheses (might fail)")
    
    # 11. INVALID CHARACTERS
    print("\n🔴 INVALID CHARACTER CASES (Should Fail)")
    run_test("x^2 + y = 0", should_fail=True, description="Wrong variable name")
    run_test("x^2 + 3@ = 0", should_fail=True, description="Invalid character @")
    run_test("x^2 & x = 0", should_fail=True, description="Invalid character &")
    run_test("x^2 % 3 = 0", should_fail=True, description="Invalid character %")
    
    # 12. EQUATION FORMAT ERRORS
    print("\n🔴 EQUATION FORMAT ERRORS (Should Fail)")
    run_test("x^2 + x", should_fail=True, description="Missing equals sign")
    run_test("x^2 = x = 0", should_fail=True, description="Multiple equals signs")
    run_test("", should_fail=True, description="Empty equation")
    
    # 13. POWER EXPRESSION ERRORS
    print("\n🔴 POWER EXPRESSION ERRORS (Should Fail)")
    run_test("x^ = 0", should_fail=True, description="Empty power after ^")
    run_test("x^+ = 0", should_fail=True, description="Only operator after ^")
    run_test("x^(+) = 0", should_fail=True, description="Only operator in parentheses")
    
    # 14. MULTIPLICATION WITH HIGH POWERS
    print("\n🔴 MULTIPLICATION HIGH POWER CASES (Should Fail)")
    run_test("x^1*x^2 = 0", should_fail=True, description="x^1*x^2 = x^3 (invalid)")
    run_test("x^2*x^1 = 0", should_fail=True, description="x^2*x^1 = x^3 (invalid)")
    run_test("x*x*x = 0", should_fail=True, description="x*x*x = x^3 (invalid)")
    
    # 15. COMPLEX VALID CASES
    print("\n🟢 COMPLEX VALID CASES")
    run_test("-2*x^2 + 3*x - 1 = 0", description="Complex quadratic")
    run_test("x^2 - 2*x + 1 = (x-1)^2", should_fail=True, description="Right side with parentheses")
    run_test("0.5*x^2 + 1.5*x = 2.25", description="Decimal coefficients")
    
    print("\n" + "="*60)
    print("🏁 TEST SUITE COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
