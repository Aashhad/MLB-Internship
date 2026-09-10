from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from auth.models import User
from auth.schemas import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse
)

from auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ============================================================
# SECURITY
# ============================================================

security = HTTPBearer()


# ============================================================
# REGISTER
# POST /auth/register
# ============================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):

    # Check username
    existing_username = (
        db.query(User)
        .filter(User.username == user_data.username)
        .first()
    )

    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    # Check email
    existing_email = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )


    # Hash password
    hashed_password = hash_password(
        user_data.password
    )


    # Create user
    new_user = User(

        username=user_data.username,

        email=user_data.email,

        password=hashed_password
    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return new_user


# ============================================================
# LOGIN
# POST /auth/login
# ============================================================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):

    # Find user
    user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )


    # Check user
    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


    # Verify password
    password_correct = verify_password(
        user_data.password,
        user.password
    )


    if not password_correct:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


    # Create JWT
    access_token = create_access_token(
        user.id
    )


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ============================================================
# GET CURRENT USER
# GET /auth/me
# ============================================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    # Get token
    token = credentials.credentials


    # Verify token
    user_id = verify_access_token(token)


    if user_id is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


    # Find user
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )


    return user