import asyncio
from telegram_bot import TelegramBot

class Cli:
    def __init__(self, bot: TelegramBot):
        self._bot = bot

    async def start(self) -> None:
       return asyncio.create_task(self._cli_loop())

    async def _cli_loop(self) -> None:
        print("CLI ready. Commands: allow <id>, deny <id>, chats, message <id> <prompt>, exit")

        while True:
            cmd = await asyncio.to_thread(input, "> ")

            if not cmd:
                continue

            if cmd == "exit":
                print("Shutting down...")
                await self._bot.client.disconnect()
                break

            if cmd.startswith("allow "):
                chat_id = int(cmd.split()[1])
                self._bot.allow_chat(chat_id)
                print(f"Allowed chat {chat_id}")

            elif cmd.startswith("deny "):
                chat_id = int(cmd.split()[1])
                self._bot.disallow_chat(chat_id)
                print(f"Disallowed chat {chat_id}")
            elif cmd.startswith("chats "):
                chat_id_str, filter = cmd.split(" ")
                chats = await self._bot.list_chats(filter)
                for chat in chats:
                    print(f"{chat.id} | {chat.name}")
            elif cmd.startswith("message "):
                try:
                    _, chat_id_str, prompt = cmd.split(" ", 2)
                    chat_id = int(chat_id_str)
                except ValueError:
                    print("Usage: message <chat_id> <text>")
                    continue

                await self._bot.generate_and_send_message(chat_id, prompt)

            else:
                print("Unknown command")