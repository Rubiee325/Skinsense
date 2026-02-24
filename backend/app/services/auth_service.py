from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status
from bson import ObjectId

from ..db import get_database
from ..core.auth import verify_password, get_password_hash, create_access_token


async def create_user(
    email: str,
    password: str,
    name: str,
    age: int,
    gender: str,
    role: str = "patient"
) -> dict:
    """Create a new user in MongoDB."""
    db = get_database()
    users_collection = db["users"]
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = get_password_hash(password)
    
    # Create user document
    user_doc = {
        "email": email,
        "password": hashed_password,
        "name": name,
        "age": age,
        "gender": gender,
        "role": role,
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Insert user
    result = await users_collection.insert_one(user_doc)
    # Convert MongoDB _id to id for JSON serialization
    user_doc["_id"] = str(result.inserted_id)
    user_doc["id"] = user_doc["_id"]  # Add id field for compatibility
    
    # Remove password from response
    user_doc.pop("password", None)
    
    return user_doc


async def authenticate_user(email: str, password: str) -> Optional[dict]:
    """Authenticate a user and return user data if valid."""
    db = get_database()
    users_collection = db["users"]
    
    # Find user by email
    user = await users_collection.find_one({"email": email})
    if not user:
        return None
    
    # Verify password
    if not verify_password(password, user["password"]):
        return None
    
    # Convert ObjectId to string for JSON serialization
    user["_id"] = str(user["_id"])
    user["id"] = user["_id"]  # Add id field for compatibility
    user.pop("password", None)
    
    return user


async def get_user_by_id(user_id: str) -> Optional[dict]:
    """Get user by user ID."""
    db = get_database()
    users_collection = db["users"]
    
    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            user["id"] = user["_id"]  # Add id field for compatibility
            user.pop("password", None)
        return user
    except Exception:
        return None


async def login_user(email: str, password: str) -> dict:
    """Login user and return access token."""
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user["_id"], "email": user["email"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

