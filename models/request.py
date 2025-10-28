from pydantic import BaseModel
from typing import Dict, Optional

class SendGroupMsgParams(BaseModel):
    group_id: int
    message: str

class RequestModel(BaseModel):
    action: str
    params: SendGroupMsgParams
    echo: Optional[str] = None