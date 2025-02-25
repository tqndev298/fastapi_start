import pyotp


def generate_totp_secret():
    return pyotp.random_base32()


def generate_totp_uri(secret, user_email):
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=user_email, issuer_name="YourAppName"
    )


from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from db_connection import get_session
from operations import get_user
from rbac import get_current_user
from responses import UserCreateResponse

router = APIRouter()


@router.post("/user/enable-mfa")
def enable_mfa(
    user: UserCreateResponse = Depends(get_current_user),
    db_session: Session = Depends(get_session),
):
    secret = generate_totp_secret()
    db_user = get_user(db_session, user.username)
    db_user.totp_secret = secret
    db_session.add(db_user)
    db_session.commit()
    totp_uri = generate_totp_uri(secret, user.email)
    return {"totp_uri": totp_uri, "secret_numbers": pyotp.TOTP(secret).now()}


@router.post("/verify-totp")
def verify_totp(code: str, username: str, session: Session = Depends(get_session)):
    user = get_user(session, username)
    print(user)
    if not user.totp_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="MFA not activated"
        )
    totp = pyotp.TOTP(user.totp_secret)
    print(totp)
    if not totp.verify(code):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid TOTP token"
        )
    return {"message": "TOTP token verified successfully"}
