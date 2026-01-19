from typing import Protocol
from message import ChatMessage
from chat_assistant import ChatAssistant, InMemoryAssistant, RoutingAssistant

class MessageHandler(Protocol):
    async def __call__(self, msg: ChatMessage, need_reply: bool = True) -> ChatMessage | None: ...

class ChatMessageHandler:
    def __init__(self, name: str, chat_id: int) -> None:
        self._assistant: ChatAssistant = self._create_assistant(name, chat_id)

    async def __call__(self, msg: ChatMessage, need_reply: bool = True) -> ChatMessage | None:
        return self._assistant.process([msg], need_reply)

    @staticmethod
    def _create_assistant(name: str, chat_id: int) -> ChatAssistant:
        return InMemoryAssistant(
            assistant=RoutingAssistant(name=name, chat_id=chat_id)
        )
