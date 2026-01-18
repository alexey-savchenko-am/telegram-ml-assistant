from typing import Protocol
from telethon import TelegramClient

class MessageSender(Protocol):
    async def send(self, chat_id: int, text: str) -> None: ...
    async def reply(self, chat_id: int, text: str, message_id: int) -> None: ...

class TelegramMessageSender:
    def __init__(self, client: TelegramClient):
        self._client = client

    async def send(self, chat_id: int, text: str) -> None:
        await self._client.send_message(chat_id, text)

    async def reply(self, chat_id: int, text: str, message_id: int) -> None:
        await self._client.send_message(chat_id, text, reply_to = message_id)