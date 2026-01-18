from typing import Protocol
from message import ChatMessage
from chat_assistant import ChatAssistant, ChatGPTAssistant, InMemoryAssistant

class MessageHandler(Protocol):
    async def __call__(self, msg: ChatMessage, need_reply: bool = True) -> ChatMessage | None: ...

class ChatMessageHandler:
    def __init__(self, chat_id: int) -> None:
        self._assistant: ChatAssistant = self._create_assistant(chat_id)

    async def __call__(self, msg: ChatMessage, need_reply: bool = True) -> ChatMessage | None:
        return self._assistant.process([msg], need_reply)

    def _create_assistant(self, chat_id: int) -> ChatAssistant:
        return InMemoryAssistant(
            assistant=ChatGPTAssistant(chat_id=chat_id)
        )
