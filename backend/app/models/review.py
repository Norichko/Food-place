from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Review(BaseModel):
    user_id: str
    target_id: str
    target_type: str  # 'restaurant' or 'dish'
    rating: int
    comment: Optional[str]
    date: datetime
