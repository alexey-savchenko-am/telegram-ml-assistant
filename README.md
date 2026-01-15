# Telegram GPT Assistant Bot

A lightweight, asynchronous Telegram bot built with **Telethon** that integrates a **ChatGPT-based assistant**.  
The bot responds only to allowed users and only when trigger words are detected (either in the message itself or in a replied message).

---

## Features

- Asynchronous Telegram client (Telethon)
- ChatGPT integration
- Per-chat / per-user assistant instances
- Message history support (context window)
- Trigger-word based activation
- Reply-aware message processing
- Runtime management of allowed senders
- Clean separation of responsibilities

---

## Architecture Overview

telegram_bot.py → Telegram client & message filtering
chatgpt_assistant.py → ChatGPT integration
message_handler.py → Message handler interface

**Flow:**

1. Telegram receives a new message
2. Message is filtered:
   - sender is allowed
   - trigger word is present (directly or in reply)
3. Message is passed to a handler
4. ChatGPT generates a response
5. Bot replies in the same chat

---

## Requirements

- Python **3.12.7**
- Telegram API credentials
- OpenAI API key

---

## Environment Variables

Create a .env file:

```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
OPENAI_API_KEY=your_openai_api_key
```
