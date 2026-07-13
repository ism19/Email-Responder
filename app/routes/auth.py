import os
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.database.database import get_professor_by_google_id, insert_and_update_professors

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET")
REDIRECT_URI = "http://localhost:8000/auth/google/callback"

SCOPES = [
    "openid",
    "email",
    "profile",
    "https://www.googleapis.com/auth/gmail.modify"
]

@router.get("/auth/google")
async def auth_google():
    scope = " ".join(SCOPES)
    url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={scope}"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    return RedirectResponse(url)

@router.get("/auth/google/callback")
async def auth_google_callback(code: str):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code"
            }
        )
        token_data = token_response.json()

        if "error" in token_data:
            raise HTTPException(status_code=400, detail=token_data["error"])
        
        access_token = token_data["access_token"]
        refresh_token = token_data.get("refresh_token", "")
        token_expiry = str(datetime.now(timezone.utc) + timedelta(seconds=token_data["expires_in"]))

        profile_response = await client.get (
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        profile = profile_response.json

        google_id = profile["id"]
        email = profile["email"]
        name = profile.get("name", "")

        await insert_and_update_professors (
            google_id=google_id,
            email=email,
            name=name,
            access_token=access_token,
            refresh_token=refresh_token,
            token_expiry=token_expiry
        )

        jwt_token = jwt.encode (
            {
                "google_id": google_id,
                "email": email,
                "exp": datetime.now(timezone.utc) + timedelta(days=7),
            },
            JWT_SECRET,
            algorithm="HS256"
        )

        return {"token": jwt_token}

