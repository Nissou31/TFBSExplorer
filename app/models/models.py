from pydantic import BaseModel
from typing import List, Optional


class TFBSRequest(BaseModel):
    email: str
    t: float
    l: Optional[int] = 1000
    w: Optional[int] = 40
    m: str
    s: float
    p: Optional[float] = 0.0
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
