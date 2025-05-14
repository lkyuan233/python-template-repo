"""Calculator module for performing basic arithmetic operations."""

from abc import ABC, abstractmethod
from .calculator import Calculator

# Step 1: Define the interface for Calculator
class ICalculator(ABC):
    """Interface for a calculator component."""

    @abstractmethod
    def add(self, a: float, b: float) -> float:
        pass

    @abstractmethod
    def subtract(self, a: float, b: float) -> float:
        pass

    @abstractmethod
    def multiply(self, a: float, b: float) -> float:
        pass

    @abstractmethod
    def divide(self, a: float, b: float) -> float:
        pass

# Step 2: Provide a default implementation of the interface
calculator_api: ICalculator = Calculator()

# Step 3: Explicit API surface
__all__ = ["ICalculator", "Calculator", "calculator_api"]