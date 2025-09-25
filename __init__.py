"""
Quadratic Equation Solver Package

A comprehensive polynomial equation parser and solver that handles
quadratic equations with robust error checking and validation.
"""

from .equation_parser import parse_equation
from .solver import solve, reduce_form, degree
from .math_utils import sqrt, abs

__all__ = ['parse_equation', 'solve', 'reduce_form', 'degree', 'sqrt', 'abs']
