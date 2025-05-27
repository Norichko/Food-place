from fastapi import APIRouter
from typing import List, Optional
from app.schemas.dish import DishBase, DishOut
from app.db.database import dishes_collection, reviews_collection
from bson import ObjectId
from fastapi import Query

router = APIRouter()

def calculate_average_rating(target_id: str):
    reviews = list(reviews_collection.find({"target_id": target_id}))
    if not reviews:
        return 0.0
    return round(sum(r["rating"] for r in reviews) / len(reviews), 1)

@router.post("/")
def add_dish(dish: DishBase):
    res = dishes_collection.insert_one(dish.dict())
    return {"id": str(res.inserted_id)}

@router.get("/restaurant/{restaurant_id}", response_model=List[DishOut])
def get_dishes_by_restaurant(
    restaurant_id: str,
    category: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_price: Optional[float] = None,
    ingredients: Optional[List[str]] = Query(None)
):
    query = {"restaurant_id": restaurant_id}
    if category:
        query["categories"] = category
    if ingredients:
        query["ingredients"] = {"$all": ingredients}  # ← добавлено

    result = []
    for d in dishes_collection.find(query):
        d["id"] = str(d["_id"])
        d["average_rating"] = calculate_average_rating(str(d["_id"]))
        if (min_rating is None or d["average_rating"] >= min_rating) and \
           (max_price is None or d["price"] <= max_price):
            result.append(d)
    return result

@router.get("/search", response_model=List[DishOut])
def search_all_dishes(
    ingredient: Optional[str] = None,
    category: Optional[str] = None,
    kitchenType: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_price: Optional[float] = None
):
    query = {}

    if ingredient:
        query["ingredients"] = {"$regex": ingredient, "$options": "i"}
    if category:
        query["categories"] = category
    if kitchenType:
        query["kitchenType"] = kitchenType

    result = []
    for d in dishes_collection.find(query):
        d["id"] = str(d["_id"])
        d["average_rating"] = calculate_average_rating(str(d["_id"]))
        if (min_rating is None or d["average_rating"] >= min_rating) and \
           (max_price is None or d["price"] <= max_price):
            result.append(d)
    return result
