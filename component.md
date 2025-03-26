# Project Components

## Overview

This project is structured into modular components, each handling a specific functionality. Components are organized within the `src/` directory to ensure separation of concerns, maintainability, and scalability.

### Directory Structure
```
project_root/
│── src/
│   ├── calculator.py   # Provides basic arithmetic operations
│   ├── logger.py       # Manages logging of operations
│   ├── notifier.py     # Sends alerts when specified conditions are met
│── components.md       # Documentation of project components
│── README.md           # Project overview and setup instructions
```

Each component is designed as an independent module that can be extended or modified with minimal impact on the rest of the system.

## Components

### 1. Calculator

**Location:** `src/calculator.py`

**Description:**
Provides basic arithmetic operations essential for mathematical calculations.

**Classes:**

- `Calculator`: Contains methods for basic arithmetic operations.

**Methods:**

- `add(a: float, b: float) -> float`: Returns the sum of `a` and `b`.
- `subtract(a: float, b: float) -> float`: Returns the difference between `a` and `b`.
- `multiply(a: float, b: float) -> float`: Returns the product of `a` and `b`.
- `divide(a: float, b: float) -> float`: Returns the quotient of `a` and `b`.

### 2. Logger

**Location:** `src/logger.py`

**Description:**
Handles logging functionalities to track operations and system events.

**Classes:**

- `Logger`: Provides a method to log messages.

**Methods:**

- `log(message: str) -> None`: Logs the provided message for debugging and tracking purposes.

### 3. Notifier

**Location:** `src/notifier.py`

**Description:**
Monitors values and triggers alerts when predefined conditions are met.

**Classes:**

- `Notifier`: Checks values against a threshold and sends alerts.

**Methods:**

- `send_alert(value: float) -> str`: Returns an alert message if `value` exceeds the threshold; otherwise, indicates the value is within the limit.




