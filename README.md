## 🧪 PR Coverage Tracker

A Python CLI tool to analyze how a GitHub Pull Request (PR) impacts code coverage. It compares test coverage before and after a PR, identifies which modified lines gained or lost coverage, and reports overall coverage change.

> ✅ Built using `coverage.py`, `pytest`, `git`, and GitHub CLI (`gh`)

---

## 📦 Features

- 📄 Line-level coverage transitions (e.g., `Line 42: ❌ → ✅`)
- 📊 Overall coverage delta with counts and percentages
- 🧠 Smart diff-based analysis using `git merge-base`
- 🧪 Uses a temporary clone — no effect on your local repo
- 💥 Graceful handling of empty or first-time PRs

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+

1. **Setting PYTHONPATH**

For Windows use the following command:

```sh
set PYTHONPATH=%CD%
```

For MacOS use the following command:

```sh
export PYTHONPATH=$(pwd)
```

2. **Install GitHub CLI (gh)**

If you're on macOS with Homebrew:

```bash
brew install gh
```

Or download it from https://cli.github.com/.

Then authenticate with your GitHub account:

```bash
gh auth login
```

Follow the prompts to connect your account via browser.

---

## 🛠️ Installation

1. **Clone the Repository**

```bash
git clone https://github.com/lkyuan233/python-template-repo.git
cd python-template-repo
git checkout extracredit
```

2. **Install Dependencies**

```bash
uv pip install coverage pytest
```

---

## 🚀 Usage

Run the script from your terminal:

```bash
uv run app.py --url <PR_URL>
```

---

## 🧾 Sample Output

```bash
📄 Modified Line Coverage Changes:
spam_detector.py: Line 45: ❌ → ✅

📊 Overall Coverage Summary:
   🔹 Covered lines: 83/88 (94.32%) → 272/312 (87.18%)
   🔺 Change: -7.14%
```

---

## 🧱 How It Works

1. Parses the PR URL and clones the repo into a temp directory

2. Fetches the PR and its base branch using GitHub CLI

3. Computes the merge base between base and PR HEAD

4. Runs tests with coverage at both commits

5. Uses git diff to extract modified lines

6. Compares line-level and total coverage changes

---

## ⚠️ Edge Case Handling

- Handles PRs where the base branch is empty (e.g., first commit)

- Reports 0/0 coverage if no tests or source code exist at merge base

- Skips JSON conversion if .coverage file is not generated

---

## 🧰 Future Improvements

- Markdown or HTML report export

- GitHub Action or CI integration

- Minimum required coverage thresholds

---

## 🧑‍💻 Contributing

1. Fork the repo
2. `git checkout -b feature-name`
3. Commit and push your changes
4. Open a Pull Request

---

## 📄 License

MIT License © 2025