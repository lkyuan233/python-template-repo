# **AI Conversation Client**

# **Overview**
The AI Conversation Client is a lightweight Python module designed to facilitate interactions between users and an AI-powered chatbot. It provides methods for managing conversation sessions, exchanging messages, retrieving chat history, and setting user preferences.

# **Features**
1. **Send and receive messages:** Users can interact with the AI using a structured API.
2. **Session management:** Start, retrieve, and end conversation sessions.
3. **Chat history retrieval:** Access previous messages in an ongoing session.
4. **User preferences:** Customize user settings for AI interactions.

# **API Reference**

**AIConversationClient Class**

**Initialization**
```sh
client = AIConversationClient()
```

1. **send_message(session_id: str, message: str) -> dict**
- Sends a message to the AI and returns a response.

Args:

    - session_id (str): Unique session identifier.
    
    - message (str): User's message.

Returns:

    - dict: AI-generated reply.

2. **get_chat_history(session_id: str) -> list**
- Retrieves chat history for a session.

Args:

    - session_id (str): Unique session identifier.

Returns:

    - list: A list of message dictionaries.

3. **set_user_preferences(user_id: str, preferences: dict) -> bool**
- Updates user preferences for AI interactions.

Args:

    - user_id (str): Unique user identifier.
    
    - preferences (dict): Dictionary of preferences.

Returns:

    - bool: Success status.

4. **start_new_session(user_id: str) -> str**
- Starts a new conversation session.

Args:

    - user_id (str): Unique user identifier.

Returns:

    - str: New session ID.
    
5. **end_session(session_id: str) -> bool**
- Ends an active conversation session.

Args:

    - session_id (str): Unique session identifier.

Returns:

    - bool: Success status.

**Setup & Installation**

1️⃣ **Clone the Repository**

```sh
git clone https://github.com/lkyuan233/python-template-repo.git
cd python-template-repo
git checkout interface-definition
```

**Running Tests**

Run tests with:
```sh
uv run pytest
```

# **Project Scope**

**Minimum Viable Product (MVP)**

Users can send messages and receive AI responses.
Users can start and end conversation sessions.
Chat history retrieval for a session.
User preferences management.

**Out of Scope**

AI model implementation (assumed external integration).
Real-time message streaming.
Advanced personalization beyond basic preferences.

**Contributing**

- Fork the repo.
- Create a new branch: `git checkout -b feature-name`
- Commit changes: `git commit -m "Add feature"`
- Push and create a PR.

# **License**

This project is licensed under the MIT License.
