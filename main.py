import os
from telegram_bot import TelegramBot
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv
from message_sender import TelegramMessageSender

async def cli_loop(bot: TelegramBot) -> None:
    print("CLI ready. Commands: allow <id>, deny <id>, message <id> <prompt>, exit")

    while True:
        cmd = await asyncio.to_thread(input, "> ")

        if not cmd:
            continue

        if cmd == "exit":
            print("Shutting down...")
            await bot.client.disconnect()
            break

        if cmd.startswith("allow "):
            chat_id = int(cmd.split()[1])
            bot.allow_chat(chat_id)
            print(f"Allowed chat {chat_id}")

        elif cmd.startswith("deny "):
            chat_id = int(cmd.split()[1])
            bot.disallow_chat(chat_id)
            print(f"Disallowed chat {chat_id}")

        elif cmd.startswith("message "):
            try:
                _, chat_id_str, prompt = cmd.split(" ", 2)
                chat_id = int(chat_id_str)
            except ValueError:
                print("Usage: message <chat_id> <text>")
                continue

            await bot.generate_and_send_message(chat_id, prompt)

        else:
            print("Unknown command")


async def main() -> None:

    load_dotenv()

    api_id = int(os.getenv("API_ID", "0"))
    api_hash = os.getenv("API_HASH")

    client = TelegramClient("session", api_id, api_hash)
    
    await client.start()

    user = await client.get_me()
    message_sender = TelegramMessageSender(client)
   
    bot = TelegramBot(
        name="LyohaGPT",
        client=client,
        message_sender=message_sender,
        user=user,
        trigger_words=["Леха", "Лёха", "LyohaGPT"],
        allowed_chat_ids=[-318631037,18866739,311022903,18001035,1190128587]
    )

    print(
        f"Telegram bot started as "
        f"{user.username or user.id}"
    )

    cli_task = asyncio.create_task(cli_loop(bot))

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())