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

2️⃣ **Install UV**
- on MacOS/Linux:
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```
- on Windows:
```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3️⃣ **Install Dependencies**
```sh
pip install --upgrade pip
uv pip install -r requirements.txt
```

4️⃣ **Run Static Analysis & Formatting**
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

### For the output, please refer to the **operations.log** file.

- **Run all tests (integration & end-to-end):**
```sh
python -m pytest tests
```

📊 **CI/CD Links**
1. *Passed Tests:*
```sh
https://app.circleci.com/pipelines/circleci/PSPAqb61iTnmZKKMnwKv5y/GjLaCzQtg7o9JRt3fefk5f/137/workflows/ced0bc29-6728-49d6-9144-7832824a2690/jobs/139/steps
```
2. *Failed Tests:*
```sh
https://app.circleci.com/pipelines/circleci/PSPAqb61iTnmZKKMnwKv5y/GjLaCzQtg7o9JRt3fefk5f/133/workflows/12178a55-f62a-4a8f-a522-fcdf42f11a4c/jobs/134
```
3. *Viewing Coverage Report:*
```sh
https://output.circle-artifacts.com/output/job/5c84c65e-f546-42a0-a571-00298281fb0f/artifacts/0/coverage_html/index.html
```

### **CI/CD Pipeline (CircleCI)**
1. Tests are executed on every push to GitHub or every PR created on GitHub.
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
-- enabling D203 can lead to conflicts between the linter and the formatter.

📜 **Logging**
- **All operations are also logged into** `operations.log`

🤝 **Contributing**
- Fork the repo.
- Create a new branch: `git checkout -b feature-name`
- Commit changes: `git commit -m "Add feature"`
- Push and create a PR.

# License
This project is licensed under the MIT License. For more details, see the `LICENSE` file.
