from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    email: str
    password: str
    establishment_name: str


class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    establishment_name: Optional[str] = None


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse