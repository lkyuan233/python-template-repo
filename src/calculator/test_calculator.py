"""Unit tests for Calculator module."""

import pytest
from src.calculator import calculator_api 

# Constants for testing
TWO = 2
THREE = 3
FIVE = 5
SIX = 6
ONE = 1
ZERO = 0

@pytest.fixture
def calculator() -> None:
    """Fixture to use the shared Calculator API instance."""
    return calculator_api  # ✅ Use the API instead of creating a new instance

def test_add(calculator) -> None:
    """Test addition of two numbers."""
    assert calculator.add(TWO, THREE) == FIVE

def test_subtract(calculator) -> None:
    """Test subtraction of two numbers."""
    assert calculator.subtract(FIVE, THREE) == TWO

def test_multiply(calculator) -> None:
    """Test multiplication of two numbers."""
    assert calculator.multiply(TWO, THREE) == SIX

def test_divide(calculator) -> None:
    """Test division of two numbers."""
    assert calculator.divide(SIX, TWO) == THREE

def test_divide_by_zero(calculator) -> None:
    """Test division by zero raises ValueError."""
    with pytest.raises(ValueError) as excinfo:
        calculator.divide(FIVE, ZERO)
    assert str(excinfo.value) == "Cannot divide by zero"
