import re
import time
import asyncio
from typing import Iterable
from telethon import TelegramClient, events
from telethon.tl.types import User, InputPeerUser
from telethon.tl.custom.message import Message
from telethon.tl.types import User, Chat, Channel, MessageEntityMentionName, Dialog
from message_sender import MessageSender
from message import ChatMessage
from message_handler import ChatMessageHandler

class TelegramBot:
    def __init__(
        self,
        name: str,
        client: TelegramClient,
        message_sender: MessageSender,
        user: User | InputPeerUser,
        *,
        trigger_words: Iterable[str],
        allowed_chat_ids: Iterable[int],
    ) -> None:

        if not client:
            raise ValueError("Client is required")
        
        self._name = name
        self._client = client
        self._message_sender = message_sender
        self._user = user

        words = [w.strip() for w in trigger_words if w.strip()]
        if not words:
            raise ValueError("trigger_words must contain at least one non-empty word")
        pattern = "|".join(re.escape(w) for w in words)
        self._trigger_regex = re.compile(pattern, re.IGNORECASE)

        self._allowed_chat_ids: set[int] = set(allowed_chat_ids or [])

        self._chat_queues: dict[int, asyncio.Queue] = {}
        self._chat_workers: dict[int, asyncio.Task] = {}

        self._client.add_event_handler(
            self._on_message, 
            events.NewMessage
        )

    # ---------- public API ----------

    def allow_chat(self, chat_id: int) -> None:
        self._allowed_chat_ids.add(chat_id)

    def disallow_chat(self, chat_id: int) -> None:
        self._allowed_chat_ids.discard(chat_id)

    async def generate_and_send_message(self, chat_id: int, prompt: str) -> None:
        try:
            generated_message = await self._handler(chat_id, prompt)  # type: ignore[arg-type]
            if generated_message:
                await self._message_sender.send(chat_id, generated_message)
        except Exception as exc:
                print("Handler error:", exc)

    async def _on_message(self, event: events.NewMessage.Event) -> None:

        if not await self._process_event(event):
            return

        addressed_to_me: bool = await self._addressed_to_me(event)
        chat: User | Chat | Channel = await event.get_chat()
        sender: User | None = await event.get_sender()


        text = event.message.text.replace(f"@{self._user.username}", "").strip()

        name_type = self._get_chat_name_and_type(chat)

        sender_name = (
            sender.first_name
            if sender and sender.first_name
                else sender.username if sender else "Unknown"
            )

        print(f"[{name_type[1]}] {name_type[0]} ({chat.id}): {sender_name} → {text}")

        msg = ChatMessage(
            role="user", 
            content=f"[SENDER: {sender_name}, RECIPIENT: {name_type[0]}]: {text}",
        )

        queue = self._ensure_chat_worker(chat.id)
        await queue.put((event, msg, addressed_to_me))

    # ---------- internal logic ----------

    def _ensure_chat_worker(self, chat_id: int) -> asyncio.Queue:
        if chat_id not in self._chat_queues:
            queue = asyncio.Queue()
            self._chat_queues[chat_id] = queue
            self._chat_workers[chat_id] = asyncio.create_task(
                self._chat_worker(chat_id, queue)
            )
        return self._chat_queues[chat_id]
    
    async def _chat_worker(self, chat_id: int, queue: asyncio.Queue) -> None:

        message_handler = ChatMessageHandler(chat_id)

        while True:
            event, msg, addressed_to_me = await queue.get()
            try:
                start = time.perf_counter()
                reply = await message_handler(
                    msg,
                    need_reply=addressed_to_me)
                
                if reply:
                    elapsed = time.perf_counter() - start
                    await self._message_sender.reply(
                        chat_id,
                        self._format_message(reply, elapsed),
                        event.id,
                    )
            except Exception as exc:
                print(f"Handler error in chat {chat_id}:", exc)
            finally:
                queue.task_done()
                
    async def _process_event(self, event: events.NewMessage.Event) -> bool:

        mid = event.chat_id or event.user_id
   
        if not event.text:
            return False

        if event.sender_id is None:
            return False

        if self._allowed_chat_ids and mid not in self._allowed_chat_ids:
            return False
        
        return True
    
    async def _addressed_to_me(self, event: events.NewMessage.Event) -> bool:
        if self._trigger_regex.search(event.text):
            return True

        if event.message.reply_to_msg_id:
            reply_msg = await event.message.get_reply_message()
            if reply_msg and reply_msg.text:
                if self._trigger_regex.search(reply_msg.text):
                    return True
                
        return False
    
    def _format_message(self, msg: ChatMessage, elapsed: float) -> str:
        return f"[{self._name} 💬🤖🔥]\n{elapsed:.2f} sec elapsed\n{msg.content}" if msg else None
    
    @staticmethod
    def _get_chat_name_and_type(
        chat: User | Chat | Channel,
    ) -> tuple[str, str]:
        if isinstance(chat, User):
            return chat.first_name or "User", "private"

        if isinstance(chat, Chat):
            return chat.title, "group"

        if isinstance(chat, Channel):
            return chat.title, "channel"

        raise TypeError(f"Unsupported chat type: {type(chat)!r}")
