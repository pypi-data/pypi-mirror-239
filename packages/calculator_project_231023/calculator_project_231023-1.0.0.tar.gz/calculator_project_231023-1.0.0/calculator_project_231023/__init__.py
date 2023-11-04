"""
Calculator Project

This is a simple calculator program written in Python that performs basic arithmetic 
operations such as addition, subtraction, multiplication, division, and taking the root 
of a number. The calculator uses the Decimal module to ensure precision in calculations.

Usage:
- Import the package using `import calculator_project_231023`
- Use run_interface() function to get the text input interface where you can provide
inputs to the calculator.

Example:
```python
import calculator_project_231023

run_interface()     # Output:   Welcome to the calculator
                                Use it to add, subtract, multiply, divide, or take a root
                                Enter the first element (integer or float):

For more information refer to the project's official documentation.
"""

__version__ = "1.0.0"

from .calculator import Calculator, get_valid_number, get_valid_operation, run_interface

__all__ = ['Calculator', 'get_valid_number', 'get_valid_operation', 'run_interface']