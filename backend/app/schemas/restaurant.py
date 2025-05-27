from pydantic import BaseModel, HttpUrl
from typing import Optional


class GeoPoint(BaseModel):
    lat: float
    lng: float


class RestaurantBase(BaseModel):
    name: str
    address: str
    openingHours: str
    website: Optional[HttpUrl]
    socialLink: Optional[HttpUrl]
    kitchenType: str
    location: Optional[GeoPoint]


class RestaurantOut(RestaurantBase):
    id: str
    average_rating: Optional[float] = 0.0
