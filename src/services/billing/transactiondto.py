from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass 
class TransactionDTO:
    id: str 
    user_id: str
    transaction_type: Literal["chat", "top_up", "refund"]
    value: int 
    created_at: datetime