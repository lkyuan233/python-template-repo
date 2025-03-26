"""Calculator module for performing basic arithmetic operations."""

from .calculator import Calculator

# Define module-level API
calculator_api = Calculator()

# Expose only necessary components
__all__ = ["Calculator", "calculator_api"]

# Now calculator_api is accessible without creating an instance manually
# Follows the guideline of defining an API
# Improves usability across different components