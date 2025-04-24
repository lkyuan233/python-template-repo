#!/usr/bin/env python3
"""
Command-line interface for the AI Conversation Client.
"""

import argparse
import asyncio
from ai_conversation_client.client import AIConversationClient
from ai_conversation_client.gemini_api_client import GeminiAPIClient

async def interactive_chat(client: AIConversationClient, user_id: str) -> None:
    """
    Run an interactive chat session.

    Args:
        client: The AIConversationClient instance.
        user_id: The user identifier.
    """
    session_id = client.start_new_session(user_id)
    print(f"New session started. Session ID: {session_id}")
    print("Type 'exit' to quit.\n")

    loop = asyncio.get_event_loop()

    while True:
        user_input = await loop.run_in_executor(None, input, "You: ")
        user_input = user_input.strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Ending session...")
            client.end_session(session_id)
            break

        try:
            response = client.send_message(session_id, user_input)
            print(f"AI: {response['content']}")
        except Exception as e:
            print(f"Error: {e}")

def list_sessions(client: AIConversationClient) -> None:
    """
    List active session IDs (not implemented for generic interface).
    """
    print("Session listing is not implemented for the generic interface.")

def show_history(client: AIConversationClient, session_id: str) -> None:
    """
    Show the chat history for a session.

    Args:
        client: The AIConversationClient instance.
        session_id: The session identifier.
    """
    try:
        history = client.get_chat_history(session_id)
        if not history:
            print("No messages yet.")
            return
        for msg in history:
            print(f"[{msg['timestamp']}] {msg['role'].capitalize()}: {msg['content']}")
    except Exception as e:
        print(f"Error: {e}")

async def run_cli(client: AIConversationClient) -> None:
    """
    Run the command-line interface.

    Args:
        client: The AIConversationClient instance.
    """
    parser = argparse.ArgumentParser(description="AI Conversation CLI")
    subparsers = parser.add_subparsers(dest="command")

    chat_parser = subparsers.add_parser("chat", help="Start a new chat")
    chat_parser.add_argument("--user-id", required=True, help="User ID for the session")

    history_parser = subparsers.add_parser("history", help="Show chat history")
    history_parser.add_argument("session_id", help="Session ID to view")

    subparsers.add_parser("list", help="List active session IDs")

    args = parser.parse_args()

    if args.command == "chat":
        await interactive_chat(client, args.user_id)
    elif args.command == "history":
        show_history(client, args.session_id)
    elif args.command == "list":
        list_sessions(client)
    else:
        parser.print_help()

if __name__ == "__main__":
    api_client = GeminiAPIClient()
    client = AIConversationClient(api_client)
    asyncio.run(run_cli(client))
