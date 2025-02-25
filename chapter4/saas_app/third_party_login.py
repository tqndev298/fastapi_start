GITHUB_CLIENT_ID = "Iv23liKsm4ewmn7PP0Ho"
GITHUB_CLIENT_SECRET = "523715e3bcaad44b1a9035a95a1de916aef6102d"
GITHUB_REDIRECT_URI = "http://localhost:8000/github/auth/token"
GITHUB_AUTHORIZATION_URL = "https://github.com/login/oauth/authorize"


import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2
from sqlalchemy.orm import Session
from models import User
from db_connection import get_session
from operations import get_user


def resolve_github_token(
    access_token: str = Depends(OAuth2()), session: Session = Depends(get_session)
) -> User:
    print(access_token)
    user_response = httpx.get(
        "https://api.github.com/user",
        headers={"Authorization": access_token},
    ).json()
    print(f"{user_response}")
    username = user_response.get("login", " ")
    print(username)
    user = get_user(session, username)
    if not user:
        email = user_response.get("email", " ")
        user = get_user(session, email)
    if not user:
        raise HTTPException(status_code=403, detail="Token not valid")
    return user
