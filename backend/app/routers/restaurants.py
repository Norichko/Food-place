from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.schemas.restaurant import RestaurantBase, RestaurantOut
from app.db.database import restaurants_collection, reviews_collection
from bson import ObjectId

router = APIRouter()

def calculate_average_rating(target_id: str):
    reviews = list(reviews_collection.find({"target_id": target_id}))
    if not reviews:
        return 0.0
    return round(sum(r["rating"] for r in reviews) / len(reviews), 1)

@router.post("/")
def create_restaurant(data: RestaurantBase):
    doc = data.model_dump()

    # Преобразуем ссылки в строки
    if doc.get("website"):
        doc["website"] = str(doc["website"])
    if doc.get("socialLink"):
        doc["socialLink"] = str(doc["socialLink"])

    # Обработка координат
    if "location" in doc and doc["location"]:
        lat = doc["location"].get("lat")
        lng = doc["location"].get("lng")
        if lat is not None and lng is not None:
            doc["location"] = {
                "type": "Point",
                "coordinates": [lng, lat]  # GeoJSON формат: [lng, lat]
            }
        else:
            doc.pop("location", None)  # удаляем если неполные
    else:
        # Значения по умолчанию — центр Москвы
        doc["location"] = {
            "type": "Point",
            "coordinates": [37.618423, 55.751244]
        }

    res = restaurants_collection.insert_one(doc)
    return {"id": str(res.inserted_id)}

@router.get("/", response_model=List[RestaurantOut])
def list_restaurants(kitchenType: Optional[str] = None, min_rating: Optional[float] = None):
    filters = {}
    if kitchenType:
        filters["kitchenType"] = kitchenType
    result = []

    for r in restaurants_collection.find(filters):
        r["id"] = str(r["_id"])
        r["average_rating"] = calculate_average_rating(r["id"])

        if "location" in r and r["location"].get("coordinates"):
            coords = r["location"]["coordinates"]
            r["location"] = {"lat": coords[1], "lng": coords[0]}  # lng — это X
        
        if min_rating is None or r["average_rating"] >= min_rating:
            result.append(r)
    return result

@router.get("/{restaurant_id}", response_model=RestaurantOut)
def get_restaurant(restaurant_id: str):
    restaurant = restaurants_collection.find_one({"_id": ObjectId(restaurant_id)})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Not found")
    restaurant["id"] = str(restaurant["_id"])
    restaurant["average_rating"] = calculate_average_rating(restaurant["id"])

    if "location" in restaurant and restaurant["location"].get("coordinates"):
        coords = restaurant["location"]["coordinates"]
        restaurant["location"] = {"lat": coords[1], "lng": coords[0]}

    return restaurant
