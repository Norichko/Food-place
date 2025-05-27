from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserOut
from app.core.security import hash_password, verify_password, create_access_token
from app.db.database import users_collection
from bson import ObjectId

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["favorites"] = []
    inserted = users_collection.insert_one(user_dict)
    return {"msg": "User registered successfully", "id": str(inserted.inserted_id)}

@router.post("/login", response_model=UserResponse)
def login(credentials: UserLogin):
    user = users_collection.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(data={"user_id": str(user["_id"])})
    user_out = UserOut(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        locationNow=user.get("locationNow"),
        favorites=user.get("favorites", [])
    )
    return {"user": user_out, "token": token}
