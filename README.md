🚀 **Python-Template-Repo**

# Description
This repository serves as a template for Python projects, including:
- **Pre-configured CI/CD pipeline** using CircleCI
- **Strict static analysis & formatting** with ruff and mypy
- **Comprehensive testing** (Unit, Integration, End-to-End) using pytest
- **Test coverage tracking**

📌 **Setup & Installation**

1️⃣ **Clone the Repository**
```sh
git clone https://github.com/lkyuan233/python-template-repo.git
cd python-template-repo
```

2️⃣ **Install Dependencies**
```sh
pip install --upgrade pip
uv pip install -r requirements.txt
```

3️⃣ **Run Static Analysis & Formatting**
```sh
ruff check .
mypy src/
ruff format .
```

🛠️ **Usage**
This repository includes three key components: (please refer to `component.md`)
- **Calculator** – Performs basic arithmetic operations.
- **Logger** – Records calculator operations.
- **Notifier** – Sends an alert when results exceed a threshold.

**Setting PYTHONPATH**

For Windows use the following command:
```sh
set PYTHONPATH=%CD%
```

For MacOS use the following command:
```sh
export PYTHONPATH=$(pwd)
```

✅ **Running Tests**

This project uses **pytest** for unit, integration and end-to-end testing.

### **Unit Tests**

- **Run all unit tests:**
```sh
python -m pytest src
```

- **Run individual unit tests:**
  1. **Calculator:**
  ```sh
  python -m pytest src/calculator/test_calculator.py
  ```
  2. **Logger:**
  ```sh
  python -m pytest src/logger/test_logger.py
  ```
  3. **Notifier:**
  ```sh
  python -m pytest src/notifier/test_notifier.py
  ```

### **Integration Tests**

- **Run integration tests correctly:**

  **For `calculator_logger`:**
  ```sh
  python -m pytest tests/calculator_logger.py
  ```
  **For detailed output:**
  ```sh
  python -m pytest -v -s tests/calculator_logger.py
  ```

  **For `logger_notifier`:**
  ```sh
  python -m pytest tests/logger_notifier.py
  ```
  **For detailed output:**
  ```sh
  python -m pytest -v -s tests/logger_notifier.py
  ```

### **End-to-End Tests**

- **Run E2E test correctly:**
```sh
python -m pytest tests/e2e.py
```

For the output, please refer to the **operations.log** file.

📊 **Viewing Coverage Report**
```sh
https://output.circle-artifacts.com/output/job/0011c25d-67b5-44be-9d81-cdeb94aa7f68/artifacts/0/coverage_html/index.html
```

### **CI/CD Pipeline (CircleCI)**
1. Tests are executed on every push to GitHub.
2. Results are visible in CircleCI’s “Tests” section.
3. Test coverage report is available via CircleCI artifacts.

To manually trigger a CI/CD run:
- Push a commit or open a PR.
- Check the CircleCI dashboard.

📏 **Code Quality Tools**
The repository enforces strict linting and static analysis:
- **Code Formatting:**
```sh
ruff format .
```
- **Linting:**
```sh
ruff check .
```
- **Static Analysis:**
```sh
mypy src/
```

If any check fails, fix issues before committing.

**Note:** ruff checks have **D203 disabled**.

📜 **Logging**
- **All operations are also logged into** `operations.log`

🤝 **Contributing**
- Fork the repo.
- Create a new branch: `git checkout -b feature-name`
- Commit changes: `git commit -m "Add feature"`
- Push and create a PR.

# License
This project is licensed under the MIT License. For more details, see the `LICENSE` file.


