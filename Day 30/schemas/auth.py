from pydantic import BaseModel, EmailStr


# ============================================================
# REGISTER
# ============================================================

class UserRegister(BaseModel):

    username: str
    email: EmailStr
    password: str


# ============================================================
# LOGIN
# ============================================================

class UserLogin(BaseModel):

    email: EmailStr
    password: str


# ============================================================
# USER RESPONSE
# ============================================================

class UserResponse(BaseModel):

    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# ============================================================
# TOKEN
# ============================================================

class TokenResponse(BaseModel):

    access_token: str
    token_type: str