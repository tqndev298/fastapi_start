from fastapi import Depends, HTTPException
from typing import Optional

VALID_API_KEYS = [
    "verysecureapikey",
    "anothersecureapi",
    "onemoresecureapi",
]


async def get_api_key(api_key: Optional[str]):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key


from fastapi import APIRouter

router = APIRouter()


@router.get("/secure-data")
async def get_secure_data(api_key: str = Depends(get_api_key)):
    return {"message": "Access to secure data granted"}
