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
        name: str,
        chat_id: int,
        model: str,
        system_prompt: str | None = None,
    ) -> None:
        self._chat_id = chat_id
        self._client = OpenAI()
        self._model = model
        self._system_prompt = system_prompt or (
            f"You are a helpful assistant named {name}. "
            "You receive messages that contain the sender's names. "
            "Address the sender by name in your reply. "
            "Reply in the same language as the message text."
        )

    @property
    def chat_id(self) -> int:
        return self._chat_id
    
    def process(self, messages: Sequence[ChatMessage], need_reply: bool = True) -> ChatMessage | None:

        if not need_reply:
            return None
        
        openai_messages: list[dict[str, str]] = [
            {"role": "system", "content": self._system_prompt},
            {"role": "system", "content": f"Chat ID: {self.chat_id}"},
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
            raise RuntimeError(f"ChatGPT request failed for Chat {self.chat_id}") from exc
        
class InMemoryAssistant:
    def __init__(
        self,
        assistant: ChatAssistant,
        context_size: int = 50,
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

class RoutingAssistant:
    def __init__(
        self,
        name: str,
        chat_id: int,
        fast_model: str = "gpt-4o-mini",
        smart_model: str = "gpt-5-mini",
        system_prompt: str | None = None,
    ) -> None:
        self._fast = ChatGPTAssistant(
            name=name,
            chat_id=chat_id,
            model=fast_model,
            system_prompt=system_prompt,
        )
        self._smart = ChatGPTAssistant(
            name=name,
            chat_id=chat_id,
            model=smart_model,
            system_prompt=system_prompt,
        )

    def process(
        self,
        messages: Sequence[ChatMessage],
        need_reply: bool = True,
    ) -> ChatMessage | None:

        if not need_reply:
            return None

        if self._is_complex(messages):
            return self._smart.process(messages, need_reply)

        return self._fast.process(messages, need_reply)
    
    def _is_complex(self, messages: Sequence[ChatMessage]):
        last = messages[-1].content

        score = 0

        if len(last) > 100:
            score += 2

        if len(last.split()) > 20:
            score += 2

        newlines = last.count('\n')
        if newlines >= 1:
            score += 1
        if newlines >= 3:
            score += 2

        if last.count('?') >= 2:
            score += 1

        if any(x in last for x in ('\n-', '\n*', '\n1.', '```')):
            score += 3

        return score >= 4