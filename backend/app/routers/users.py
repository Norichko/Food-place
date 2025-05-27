from fastapi import APIRouter, Depends
from app.db.database import users_collection, dishes_collection
from app.core.security import get_current_user
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter()

@router.get("/me")
def get_profile(user=Depends(get_current_user)):
    return user

def serialize_mongo_document(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

@router.get("/favorites")
def get_favorites(user=Depends(get_current_user)):
    try:
        user_id = ObjectId(user["id"])
    except InvalidId:
        return {"error": "Invalid user ID"}

    user_doc = users_collection.find_one({"_id": user_id})
    if not user_doc:
        return {"error": "User not found"}

    favorites = user_doc.get("favorites", [])

    dish_ids = []
    for fid in favorites:
        try:
            dish_ids.append(ObjectId(fid))
        except InvalidId:
            print(f"Invalid dish ID: {fid}")

    dishes_cursor = dishes_collection.find({"_id": {"$in": dish_ids}})

    result = [serialize_mongo_document(dish) for dish in dishes_cursor]

    return result

@router.post("/favorites/{dish_id}")
def add_to_favorites(dish_id: str, user=Depends(get_current_user)):
    user_id = ObjectId(user["id"])
    users_collection.update_one(
        {"_id": user_id},
        {"$addToSet": {"favorites": dish_id}}
    )
    return {"msg": "Добавлено в избранное"}

@router.delete("/favorites/{dish_id}")
def remove_from_favorites(dish_id: str, user=Depends(get_current_user)):
    user_id = ObjectId(user["id"])
    users_collection.update_one(
        {"_id": user_id},
        {"$pull": {"favorites": dish_id}}
    )
    return {"msg": "Удалено из избранного"}
