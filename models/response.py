from pydantic import BaseModel
from typing import List, Optional, Dict

class MessageItem(BaseModel):
    type: str
    data: Dict[str, str]

class Sender(BaseModel):
    user_id: int
    nickname: str
    card: str
    role: str

class ResponseModel(BaseModel):
    self_id: int
    user_id: int
    time: int
    message_id: int
    message_seq: int
    real_id: int
    real_seq: str
    message_type: str
    sender: Sender
    raw_message: str
    font: Optional[int]
    sub_type: Optional[str]
    message: List[MessageItem]
    message_format: Optional[str]
    post_type: str
    group_id: int
    group_name: str