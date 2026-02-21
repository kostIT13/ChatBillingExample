from dataclasses import dataclass
from typing import Literal
from datetime import datetime


@dataclass
class MessageDTO:
    id: str 
    role: Literal["assistant", "human"]
    text: str 
    chat_id: str 
    created_at: datetime