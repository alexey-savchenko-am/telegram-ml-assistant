from dataclasses import dataclass
from typing import Literal

Role = Literal["system", "user", "assistant"]

@dataclass
class ChatMessage:
    role: Role
    content: str