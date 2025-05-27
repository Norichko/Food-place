from fastapi import APIRouter
from datetime import datetime, timezone
from app.schemas.review import ReviewCreate, ReviewOut
from app.db.database import reviews_collection
from bson import ObjectId

router = APIRouter()

@router.post("/")
def add_review(review: ReviewCreate):
    review_dict = review.dict()
    review_dict["date"] = datetime.now(timezone.utc)
    result = reviews_collection.insert_one(review_dict)
    return {"msg": "Review added", "id": str(result.inserted_id)}

@router.get("/{target_id}", response_model=list[ReviewOut])
def get_reviews(target_id: str):
    reviews = list(reviews_collection.find({"target_id": target_id}))
    for r in reviews:
        r["id"] = str(r["_id"])
    return reviews
