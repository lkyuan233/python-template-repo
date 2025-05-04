# AI-Powered Email Spam Detector

## 🧠 Overview

This repository provides an integrated solution for analyzing email spam probability using AI. It combines a modular Gmail client, an AI conversation interface (backed by Google's Gemini API), and a spam detection pipeline. The project is structured for extensibility, testability, and ease of deployment.

All logic is orchestrated through a single script: `main.py`, which ties together Gmail access, Gemini API, and spam scoring logic.

---

## 💡 Features

- 📥 **Gmail Client**: Fetch and manage emails using the Gmail API
- 🤖 **AI Conversation Client**: Unified interface for interacting with LLMs (currently Gemini 2.0)
- 🧪 **Spam Detection**: Uses LLMs to rate the spam probability of emails
- 💻 **Command-Line Interface**: CLI tools for AI interaction and session management
- ⚙️ **Configurable & Extensible**: Easily swap AI backends or email providers

---

## 🗂 Project Structure

```
.
├── main.py                       # Entry point for full pipeline
├── spam_detector.py              # Core logic for email processing and Gemini scoring
├── ai_conversation_client/       # Gemini API integration
│   ├── __init__.py
│   ├── cli.py
│   ├── client.py
│   ├── conversation.py
│   ├── gemini_api_client.py
│   └── interface.py
├── mail_client/                  # Gmail API integration
│   ├── __init__.py
│   ├── interface.py
│   ├── gmail_client.py
│   ├── factories.py
│   ├── gmail_message.py
│   └── gmail_attachment.py
├── tests/                        # Unit and integration tests
│   ├── __init__.py
│   ├── dummy_api_client.py
│   ├── test_client.py
│   ├── test_integration.py
│   ├── test_spam_detector.py
│   └── test_end_to_end.py
├── .env                          # Environment variables (GEMINI_API_KEY)
├── credentials.json              # OAuth2 client secrets for Gmail API
├── output.csv                    # Final result (mail_id, Pct_spam)
├── pyproject.toml                # Project metadata and dependencies
├── uv.lock                       # Locked dependency versions
├── .circleci/                    # CI/CD configuration
│   ├── config.yml
├── README.md
├── component.md
└── .gitignore
```

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

2. **Set Up Environment Variables**

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your-gemini-api-key
```

> Get your API key from: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
> Model - Gemini 2.0 Flash

3. **Configure Gmail API**

- Place your `credentials.json` in the root directory.
  1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. Please enter or use the same email id in all the steps mentioned below.
  3. Create or select a project
  4. **Enable Gmail API** (Search for APIs and Services )
  5. Search for **Google Auth Platform**
     1. **OAuth Client ID**:
        1. Go to **Clients** -> Click on "Get Started" -> Enter App Information -> Choose **External**
        2. Go to **Clients** -> **Create Client** -> App type: **Desktop App**
        3. Download the json file and rename it to `credentials.json` and place it in the project root.
     2. **OAuth consent screen**:
        1. Go to **Audience** -> **Test Users** -> **Add Users**
        2. Enter the same email id used before
        3. Save the IDs
- The first run will prompt authentication and generate `token.json`. Continue with the on-screen instructions and choose the email id used before.

### Installation

1. **Clone the Repository**

```bash
git clone https://github.com/lkyuan233/python-template-repo.git
cd python-template-repo
git checkout hw4-step3
```

2. **Install Dependencies**

```bash
uv pip install -r pyproject.toml
uv sync --group dev
```

---

## 🧠 Usage

### Run the Integration Pipeline

Process all unread emails, score them for spam, and save results to `output.csv`:

```bash
uv run main.py
```

> While using model - Gemini 2.0 Flash - we have a limit of 15 RPM
> Hence, we parse through only 15 emails while crawling the respective inbox.

### Command-Line AI Chat (Optional)

```bash
uv run ai_conversation_client/cli.py chat --user-id your_user_id
```

---

## 📝 Output Format

The CSV file `output.csv` contains:

| mail_id       | Pct_spam |
| ------------- | -------- |
| 17c912ab3d... | 83       |
| 14aef2345a... | 12       |
| ...           | ...      |

---

## ⚙️ How It Works

1. **Email Fetching**: The Gmail client retrieves unread emails.
2. **Spam Scoring**: Each email body is sent as a prompt to Gemini for a spam score.
3. **Results Output**: Scores are saved to `output.csv` and emails are marked as read.

---

## ⚙️ Configuration

- **Dependencies**: Managed in `pyproject.toml`, locked in `uv.lock`
- **Testing**: `pytest`, `pytest-cov`, `ruff`, `mypy` for quality checks
- **CI/CD**: CircleCI configuration included in `.circleci/config.yml`

---

## 🧪 Running Tests

```bash
uv run pytest
```

Key test file:

- `tests/tests_spam_detector.py`: Validates the spam scoring logic

---

## 📚 API Reference

### AIConversationClient Class

#### Initialization

```python
client = AIConversationClient()
```

#### 1. `send_message(session_id: str, message: str) -> dict`

Sends a message to the Gemini-powered AI and returns a structured response.

**Args:**

- `session_id`: Unique identifier for the session.
- `message`: User input.

**Returns:**

- A `dict` containing the assistant’s message, role, timestamp, and ID.

#### 2. `get_chat_history(session_id: str) -> list`

Retrieves all messages from a session.

**Returns:**

- A list of message dictionaries (user + assistant).

#### 3. `set_user_preferences(user_id: str, preferences: dict) -> bool`

Stores preferences such as system prompts for a user.

#### 4. `start_new_session(user_id: str) -> str`

Starts a new conversation session.

**Returns:**

- A new session ID.

#### 5. `end_session(session_id: str) -> bool`

Ends an active session and removes its history.

### MailClient Class

```
📁 This project uses the [mail_client] from (https://github.com/Awek-015/OSPSD/pull/29) for Gmail API abstraction.

The full client interface is defined in:
[`mail_client/interface.py`](./mail_client/interface.py)
```

---

## 🛠 Tech Stack

- Python 3.10+
- Gmail API (OAuth 2.0)
- Google Gemini API (`gemini-2.0-flash`)
- `uv`, `dotenv`, `pytest`, `mypy`, `google-api-python-client`

---

## ✅ Project Scope

✅ What it does:

- Email spam analysis using AI
- Gmail + Gemini unified integration
- Command-line interface
- Output CSV results

❌ What it doesn’t:

- Real-time inbox monitoring
- Work with non-Gmail providers
- Custom LLM training or fine-tuning

---

## 🧑‍💻 Contributing

1. Fork the repo
2. `git checkout -b feature-name`
3. Commit and push your changes
4. Open a Pull Request

---

## 📄 License

MIT License © 2025