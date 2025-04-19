from ai_conversation_client.interface import IAIConversationClient

class DummyAIClient(IAIConversationClient):
    def send_message(self, session_id: str, message: str) -> dict:
        return {"reply": f"Echo: {message}"}

    def get_chat_history(self, session_id: str) -> list:
        return [{"sender": "user", "text": "Hello"}]

    def set_user_preferences(self, user_id: str, preferences: dict) -> bool:
        return True

    def start_new_session(self, user_id: str) -> str:
        return "dummy_session"

    def end_session(self, session_id: str) -> bool:
        return True
