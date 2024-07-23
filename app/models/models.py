from pydantic import BaseModel, EmailStr
from typing import List, Optional


class TFBSRequest(BaseModel):
    email: EmailStr
    t: float
    m: str
    s: float
    promoter_length: int
    window_size: int
    pseudocount: float
    mrna: List[str]


class TFBSDetail(BaseModel):
    sequence_id: str
    position: int
    score: float


class TFBSWindow(BaseModel):
    window_id: int
    tf: str
    window_pos: List[int]
    window_score: float
    details: List[TFBSDetail]
