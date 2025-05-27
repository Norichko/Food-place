from pydantic import BaseModel
from typing import List

class Dish(BaseModel):
    name: str
    price: float
    calories: float
    ingredients: List[str]
    kitchenType: str
    categories: List[str]
    restaurant_id: str
