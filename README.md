# telegram-ml-assistant

A lightweight, asynchronous Telegram **userbot** built with **Telethon** that integrates a **ChatGPT-based assistant**

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
### 1. Clone the repository
```bash
git clone https://github.com/alexey-savchenko-am/telegram-ml-assistant.git
cd telegram-ml-assistant
```
### 2. Create an .env file in the root 

```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
OPENAI_API_KEY=your_openai_api_key
```

### 3. Create sessions folder & start Docker

```bash
mkdir sessions
docker compose up --build --force-recreate
```

