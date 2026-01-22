# telegram-ml-assistant

A lightweight, asynchronous Telegram **userbot** built with **Telethon** that integrates a **ChatGPT-based assistant**.  

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

## Setup

### Create a .env file

```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
OPENAI_API_KEY=your_openai_api_key
```

