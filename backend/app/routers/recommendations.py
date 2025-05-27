from fastapi import APIRouter, Depends
from bson import ObjectId
from app.db.database import users_collection, dishes_collection, reviews_collection
from app.core.security import get_current_user

router = APIRouter()

def get_avg_rating(dish_id: str) -> float:
    reviews = list(reviews_collection.find({"target_id": dish_id, "target_type": "dish"}))
    if not reviews:
        return 0.0
    return round(sum(r["rating"] for r in reviews) / len(reviews), 1)

@router.get("/")
def personalized_recommendations(user=Depends(get_current_user)):
    user_id = ObjectId(user["id"])
    user_doc = users_collection.find_one({"_id": user_id})
    favorites = user_doc.get("favorites", [])
    if not favorites:
        return []
    kitchen_counter = {}
    category_counter = {}

    for dish_id in favorites:
        dish = dishes_collection.find_one({"_id": ObjectId(dish_id)})
        if not dish:
            continue
        kt = dish["kitchenType"]
        kitchen_counter[kt] = kitchen_counter.get(kt, 0) + 1
        for cat in dish["categories"]:
            category_counter[cat] = category_counter.get(cat, 0) + 1

    top_kitchen = max(kitchen_counter, key=kitchen_counter.get, default=None)
    top_category = max(category_counter, key=category_counter.get, default=None)

    query = {
        "kitchenType": top_kitchen,
        "categories": top_category,
        "_id": {"$nin": [ObjectId(f) for f in favorites]}
    }

    dishes = dishes_collection.find(query)
    result = []
    for d in dishes:
        d["id"] = str(d["_id"])
        d["average_rating"] = get_avg_rating(str(d["_id"]))
        result.append(d)

    result.sort(key=lambda x: x["average_rating"], reverse=True)
    return result
