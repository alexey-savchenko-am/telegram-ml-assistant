import os
from telegram_bot import TelegramBot
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv
from message_sender import TelegramMessageSender
from cli import Cli

async def main() -> None:

    load_dotenv()

    api_id = int(os.getenv("API_ID", "0"))
    api_hash = os.getenv("API_HASH")
    bot_name = "AssistantGPT"

    client = TelegramClient("sessions/session", api_id, api_hash)
    
    await client.start()

    user = await client.get_me()

    bot = TelegramBot(
        name=bot_name,
        client=client,
        message_sender=TelegramMessageSender(client),
        user=user,
        trigger_words=["chat"],
        allowed_chat_ids=[]
    )

    await Cli(bot).start()
 
    print(
        f"Telegram bot started as "
        f"{user.username or user.id}"
    )

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())