# Project Components

## What is a Component?

A **component** in this project is a self-contained module that encapsulates a specific piece of functionality.  
Each component exposes a clear public interface (methods, classes), manages its own internal logic, and can be independently tested and reused.

Components follow these principles:

- **Separation of Concerns**: Each component is responsible for one thing only.
- **Modularity**: Components can be developed, tested, and maintained in isolation.
- **Scalability**: New components can be added without modifying existing ones.
- **Testability**: Every component comes with its own set of unit tests.

Components live in top-level folders (e.g., `ai_conversation_client/`) and are treated as standalone packages.

---

## Overview

This project is structured into modular components, each handling a specific functionality. Components are placed at the project root level, ensuring separation of concerns, maintainability, and scalability.

## Directory Structure

```
project_root/
│── .circleci/
│   └── config.yml
│── .github/
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       ├── feature_request.md
│       └── pull_request_template.md
│── ai_conversation_client/    # Manages AI-based conversational logic
│   ├── __init__.py
│   ├── client.py              # Defines the AIConversationClient interface
│   └── test_client.py         # Unit tests for the component
│── tests/                     # Higher-level integration tests
│   └── integration/
│       └── test_ai_conversation_flow.py
│── README.md                  # Project overview and setup instructions
│── component.md               # Documentation of project components
│── pyproject.toml
│── requirements.txt
│── uv.lock
```

Each component is designed as an independent module that can be extended or modified with minimal impact on the rest of the system.

---

## Components

### 1. AIConversationClient

**Location**: `ai_conversation_client/client.py`

**Description**:  
The `AIConversationClient` component manages the logic for session-based communication between users and an AI system. It supports message exchange, session management, chat history retrieval, and user preference storage.

**Classes**:

- **AIConversationClient**  
  The primary interface for initiating and handling conversational sessions with an AI.

**Methods**:

- `start_new_session(user_id: str) -> str`  
  Starts a new conversation session for a given user.  
  - **Args**:  
    - `user_id`: Identifier for the user.  
  - **Returns**:  
    - A unique session ID.

- `send_message(session_id: str, message: str) -> dict`  
  Sends a message within the given session and receives the AI’s response.  
  - **Args**:  
    - `session_id`: Identifier for the session.  
    - `message`: The user's message content.  
  - **Returns**:  
    - A dictionary containing the AI’s reply.

- `get_chat_history(session_id: str) -> list`  
  Retrieves the message history of a session.  
  - **Args**:  
    - `session_id`: Identifier for the session.  
  - **Returns**:  
    - A list of message entries.

- `set_user_preferences(user_id: str, preferences: dict) -> bool`  
  Stores or updates user-specific settings or preferences.  
  - **Args**:  
    - `user_id`: Identifier for the user.  
    - `preferences`: A dictionary of user-defined settings.  
  - **Returns**:  
    - `True` if preferences are successfully updated.

- `end_session(session_id: str) -> bool`  
  Ends the specified conversation session.  
  - **Args**:  
    - `session_id`: Identifier for the session to end.  
  - **Returns**:  
    - `True` if the session was successfully ended.