# AI Conversation Client Component

## Concept of a Component

In this repository, a **component** is a self-contained unit designed to provide a specific functionality. Each component is encapsulated in its own folder, with corresponding implementation, interfaces, and models. Tests are located in a separate `/tests` directory, maintaining isolation from business logic. 

The **AI Conversation Client** component is responsible for managing AI-driven conversation sessions, including sending messages, retrieving chat history, storing user preferences, and handling session lifecycle operations. It interacts with an injected API client, which abstracts the actual communication with the external API.

---

## Directory Structure

```
ai_conversation_client/
│   ├── __init__.py            # Initialize the package
│   ├── client.py              # Implementation of AIConversationClient class
│   ├── interface.py           # Interface for AIConversationClient
│   └── models.py              # Data models for Message and UserPreferences

tests/
│   ├── test_client.py         # Unit tests for AIConversationClient
│   └── dummy_client.py        # Dummy client for testing purposes
```

Each component follows a structure where:
- **Implementation file** (`client.py`): Contains the logic and methods for the component.
- **Interface file** (`interface.py`): Defines the interface for the component's operations.
- **Models file** (`models.py`): Contains the data models used by the component.

For tests:
- **Test file** (`test_client.py`): Includes unit tests for verifying the component's functionality.

---

## AIConversationClient Component

### Purpose

The `AIConversationClient` component handles AI conversation sessions. It provides methods for sending messages, retrieving chat history, setting user preferences, and managing session lifecycles. This component interacts with an external API client (passed via dependency injection), ensuring decoupling and flexibility.

### Methods and Inputs/Outputs

- **send_message(session_id: str, message: str) -> dict[str, Any]**  
  Sends a message to the API client and retrieves the response.  
  **Input:** `session_id` (str), `message` (str)  
  **Output:** `response` (dict)

- **get_chat_history(session_id: str) -> list[dict[str, Any]]**  
  Retrieves the chat history for a given session.  
  **Input:** `session_id` (str)  
  **Output:** `chat_history` (list of dict)

- **set_user_preferences(user_id: str, preferences: dict[str, Any]) -> bool**  
  Sets user preferences via the API client.  
  **Input:** `user_id` (str), `preferences` (dict)  
  **Output:** `success` (bool)

- **start_new_session(user_id: str) -> str**  
  Starts a new conversation session for a given user.  
  **Input:** `user_id` (str)  
  **Output:** `session_id` (str)

- **end_session(session_id: str) -> bool**  
  Ends the specified session.  
  **Input:** `session_id` (str)  
  **Output:** `success` (bool)

---

### Example Usage

```python
from ai_conversation_client.client import AIConversationClient
from ai_conversation_client.models import Message, UserPreferences
from some_api_client import APIClient  # Example API client implementation

# Instantiate the API client
api_client = APIClient()

# Instantiate the AIConversationClient with the API client
conversation_client = AIConversationClient(api_client)

# Start a new session
session_id = conversation_client.start_new_session("user_123")

# Send a message
response = conversation_client.send_message(session_id, "Hello, AI!")

# Get chat history
chat_history = conversation_client.get_chat_history(session_id)

# Set user preferences
preferences = {"theme": "dark", "notifications": "enabled"}
conversation_client.set_user_preferences("user_123", preferences)

# End the session
conversation_client.end_session(session_id)
```

### Interactions

The `AIConversationClient` interacts with the injected API client to perform operations such as sending messages, retrieving chat history, and managing sessions. The interface (`APIClientProtocol`) ensures that different API client implementations can be used without modifying the core logic of the `AIConversationClient`.

The component also relies on data models (`Message` and `UserPreferences`) for organizing input and output data. For example, messages are structured using the `Message` model, and user preferences are handled with the `UserPreferences` model.

---

## Component Interaction and Integration

The AIConversationClient component is designed to be modular and self-contained, focusing solely on managing AI-driven conversation sessions. It relies on dependency injection to interact with an abstracted API client, allowing for flexibility and easy replacement of the underlying API implementation.

This architecture promotes:

- Loose coupling between the client and backend service.

- Easy unit testing using dummy or mock API clients.

Future extensibility, should additional components (like logging or notifications) be integrated later.

- **With Logger:** After sending a message or ending a session, the `AIConversationClient` can log the operation using the `Logger` component.
- **With Notifier:** If a user sets preferences that trigger notifications, the `Notifier` component could alert the user when certain conditions are met.
