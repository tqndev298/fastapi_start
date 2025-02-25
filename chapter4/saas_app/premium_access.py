from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import Role
from operations import add_user
from db_connection import get_session
from responses import ResponseCreateUser, UserCreateBody, UserCreateResponse


router = APIRouter()


@router.post(
    "/register/premium-user",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCreateUser,
)
def register_premium_user(
    user: UserCreateBody, session: Session = Depends(get_session)
):
    user = add_user(session=session, **user.model_dump(), role=Role.premium)
    if not user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "username or email already exists",
        )
    user_response = UserCreateResponse(
        username=user.username,
        email=user.email,
    )
    return {
        "message": "user created",
        "user": user_response,
    }
