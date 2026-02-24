from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from ..services.auth_service import create_user, login_user

router = APIRouter(prefix="/auth", tags=["authentication"])


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=150)
    gender: str = Field(..., min_length=1)
    role: str = Field("patient", pattern="^(patient|dermatologist)$")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SignupResponse(BaseModel):
    message: str
    user_id: str
    email: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest):
    """Create a new user account."""
    try:
        user = await create_user(
            email=request.email,
            password=request.password,
            name=request.name,
            age=request.age,
            gender=request.gender,
            role=request.role
        )
        return SignupResponse(
            message="User created successfully",
            user_id=user.get("id") or user.get("_id"),
            email=user["email"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login and get access token."""
    return await login_user(request.email, request.password)

