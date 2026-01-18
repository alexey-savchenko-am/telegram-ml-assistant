from __future__ import annotations

from typing import Protocol, Literal, Sequence, runtime_checkable
from message import ChatMessage
from collections import deque
from typing import Sequence
from openai import OpenAI

@runtime_checkable
class ChatAssistant(Protocol):
    def process(self, messages: Sequence[ChatMessage], need_reply: bool = True) -> ChatMessage | None:
        """Send a sequence of messages to the assistant"""

class ChatGPTAssistant:
    def __init__(
        self,
        chat_id: int,
        model: str = "gpt-5-mini",
        system_prompt: str | None = None,
    ) -> None:
        self._chat_id = chat_id
        self._client = OpenAI()
        self._model = model
        self._system_prompt = system_prompt or (
            "Ты полезный ассистент по имени Леха."
            "К тебе приходят сообщения, в них содержится имя отправителя и получателя."
            "Обращайся к отправителю по имени в ответе."
            "Отвечай кратко, без дополнительных вопросов, по делу."
            "ТЫ ЛЕХА И НЕ ПОЗВОЛЯЙ ОБЗЫВАТЬ ТЕБЯ ПО ДРУГОМУ."
        )

    @property
    def chat_id(self) -> int:
        return self._chat_id
    
    def process(self, messages: Sequence[ChatMessage], need_reply: bool = True) -> ChatMessage | None:

        if not need_reply:
            return None
        
        openai_messages: list[dict[str, str]] = [
            {"role": "system", "content": self._system_prompt},
        ]

        for msg in messages:
            openai_messages.append(
                {"role": msg.role, "content": msg.content}
            )

        try:
            response = self._client.responses.create(
                model=self._model,
                input=openai_messages
            )

            content = response.output_text or ""

            return ChatMessage(
                role="assistant",
                content=content,
            )

        except Exception as exc:
            raise RuntimeError("ChatGPT request failed") from exc
        
class InMemoryAssistant:
    def __init__(
        self,
        assistant: ChatAssistant,
        context_size: int = 10,
    ) -> None:
        self._assistant = assistant
        self._context_size = context_size
        self._history: deque[ChatMessage] = deque(maxlen=context_size)

    def process(self, messages: Sequence[ChatMessage], need_reply: bool = True) -> ChatMessage | None:

        self.update_cache(messages)

        if not need_reply:
            return None

        reply = self._assistant.process(list(self._history))

        self._history.append(reply)

        return reply
    
    def update_cache(self, messages: Sequence[ChatMessage]) -> None:
         self._history.extend(messages)

    def clear_cache(self) -> None:
        self._history.clear()
