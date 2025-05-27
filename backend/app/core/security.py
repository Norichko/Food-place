from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.db.database import users_collection
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed: str) -> bool:
    return pwd_context.verify(plain_password, hashed)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("✅ Payload decoded:", payload)
        user_id = payload.get("user_id")
        if not user_id:
            print("❌ user_id not found in token")
        return user_id
    except ExpiredSignatureError:
        print("❌ Token expired")
        return None
    except JWTError as e:
        print("❌ Token decode error:", str(e))
        return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    return user
