from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict

class Restaurant(BaseModel):
    name: str
    address: str
    openingHours: str
    website: Optional[HttpUrl]
    socialLink: Optional[HttpUrl]
    kitchenType: str
    location: Optional[Dict[float, float]]  # Добавлено поле для координат
