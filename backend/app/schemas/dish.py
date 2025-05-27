from pydantic import BaseModel
from typing import List

class DishBase(BaseModel):
    name: str
    price: float
    calories: float
    ingredients: List[str]
    kitchenType: str
    categories: List[str]
    restaurant_id: str

class DishOut(DishBase):
    id: str
    average_rating: float
