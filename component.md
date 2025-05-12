# Project Components

## What is a Component?

A *component* in this project is a self-contained, reusable module that encapsulates a specific piece of functionality. Each component:

- Has a clear, well-defined responsibility.
- Exposes a simple interface for interaction with other parts of the system.
- Is independently developed, tested, and maintained.
- Minimizes dependencies on other components to ensure modularity and scalability.

*In this project*, a component is typically organized as its own directory within the src/ folder, containing its code, tests, and configuration files. This approach enables separation of concerns, easier testing, and straightforward extensibility.

## Why Modular Components?

Using modular components provides several key benefits:

- *Maintainability:* Each component can be updated or fixed independently, reducing risk of side effects.
- *Reusability:* Components can be reused across different parts of the project or in future projects.
- *Testability:* Isolated components are easier to unit test.
- *Scalability:* New features can be added as new components without disrupting existing code.
- *Collaboration:* Teams can work on different components simultaneously with minimal conflicts.

## Component Structure and Interaction

Each component resides in its own directory under src/, containing:

- Implementation code (e.g., calculator.py)
- Initialization file (__init__.py)
- Local configuration (pyproject.toml)
- Unit tests (e.g., test_calculator.py)

Components interact through well-defined interfaces (typically class methods). For example, the Calculator component performs arithmetic, the Logger component logs operations, and the Notifier component sends alerts based on values.

## Directory Structure

```
project_root/

│── .circleci/
    │── config.yml
│── .github/
    │── ISSUE_TEMPLATE/
        │──bug_report.md
        │── feature_request.md
        │── pull_request_template.md
│── src/
│   ├── calculator/   # Provides basic arithmetic operations
        ├── __init__.py
        ├── calculator.py
        ├── pyproject.toml
        ├── test_calculator.py
│   ├── logger/       # Manages logging of operations
        ├── __init__.py
        ├── logger.py
        ├── pyproject.toml
        ├── test_logger.py
│   ├── notifier/     # Sends alerts when specified conditions are met
        ├── __init__.py
        ├── notifier.py
        ├── pyproject.toml
        ├── test_notifier.py
│── tests/
    ├── test_calculator_logger.py
    ├── test_e2e.py
    ├── test_logger_notifier.py
│── .gitignore 
│── .pre-commit-config.yaml
│── .python-version
│── component.md       # Documentation of project components
│── LICENSE
│── mypy.ini
│── pyproject.toml
│── README.md           # Project overview and setup instructions
│── requirements.txt
│── uv.lock
```

---

## Components

### 1. Calculator

*Location:* src/calculator/

*Description:*  
Provides basic arithmetic operations essential for mathematical calculations.

*Classes:*

- Calculator: Contains methods for basic arithmetic operations.

*Methods:*

- add(a: float, b: float) -> float: Returns the sum of a and b.
- subtract(a: float, b: float) -> float: Returns the difference between a and b.
- multiply(a: float, b: float) -> float: Returns the product of a and b.
- divide(a: float, b: float) -> float: Returns the quotient of a and b.

---

### 2. Logger

*Location:* src/logger/

*Description:*  
Handles logging functionalities to track operations and system events.

*Classes:*

- Logger: Provides a method to log messages.

*Methods:*

- log(message: str) -> None: Logs the provided message for debugging and tracking purposes.

---

### 3. Notifier

*Location:* src/notifier/

*Description:*  
Monitors values and triggers alerts when predefined conditions are met.

*Classes:*

- Notifier: Checks values against a threshold and sends alerts.

*Methods:*

- send_alert(value: float) -> str: Returns an alert message if value exceeds the threshold; otherwise, indicates the value is within the limit.

---

## Summary

This modular, component-based architecture ensures that each feature is isolated, testable, and easily maintainable. By defining and adhering to clear component boundaries, the project remains robust, scalable, and easy to extend.
