#!/usr/bin/env python3
"""
Command-line interface for the AI Conversation Client.
"""

import asyncio
import argparse
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath('..'))
from ai_conversation_client import AIConversationClient

async def interactive_chat(client: AIConversationClient, user_id: str):
    """Starts an interactive chat session with the AI."""
    session_id = client.start_new_session(user_id)
    print(f"New session started. Session ID: {session_id}")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Ending session...")
            client.end_session(session_id)
            break

        try:
            response = await client.send_message(session_id, user_input)
            print(f"AI: {response['content']}")
        except Exception as e:
            print(f"Error: {e}")

def list_sessions(client: AIConversationClient):
    print("Available session IDs:")
    for session_id in client._sessions.keys():
        print(f" - {session_id}")

def show_history(client: AIConversationClient, session_id: str):
    try:
        history = client.get_chat_history(session_id)
        if not history:
            print("No messages yet.")
            return
        for msg in history:
            print(f"[{msg['timestamp']}] {msg['role'].capitalize()}: {msg['content']}")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    load_dotenv()

    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY is not set.")
        return

    parser = argparse.ArgumentParser(description="AI Conversation CLI")
    subparsers = parser.add_subparsers(dest="command")

    chat_parser = subparsers.add_parser("chat", help="Start a new chat")
    chat_parser.add_argument("--user-id", required=True, help="User ID for the session")

    history_parser = subparsers.add_parser("history", help="Show chat history")
    history_parser.add_argument("session_id", help="Session ID to view")

    subparsers.add_parser("list", help="List active session IDs")

    args = parser.parse_args()
    client = AIConversationClient()

    if args.command == "chat":
        await interactive_chat(client, args.user_id)
    elif args.command == "history":
        show_history(client, args.session_id)
    elif args.command == "list":
        list_sessions(client)
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())
