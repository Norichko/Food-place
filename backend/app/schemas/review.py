from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    target_id: str
    target_type: str  # 'restaurant' or 'dish'
    rating: int
    comment: Optional[str]

class ReviewCreate(ReviewBase):
    user_id: str

class ReviewOut(ReviewBase):
    id: str
    user_id: str
    date: datetime
