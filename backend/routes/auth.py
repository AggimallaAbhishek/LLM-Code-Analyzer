"""
Authentication routes for Google OAuth.
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
import httpx

from backend.config import settings

router = APIRouter()

# OAuth setup
oauth = OAuth()

# Register Google OAuth provider
oauth.register(
    name='google',
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# JWT settings
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=JWT_EXPIRATION_HOURS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(request: Request) -> Optional[dict]:
    """Get the current user from the session or token."""
    # Try session first
    user = request.session.get("user")
    if user:
        return user
    
    # Try Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = verify_token(token)
        if payload:
            return {
                "email": payload.get("email"),
                "name": payload.get("name"),
                "picture": payload.get("picture")
            }
    
    return None


def require_auth(request: Request):
    """Dependency to require authentication."""
    user = request.session.get("user")
    if not user:
        # Check Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = verify_token(token)
            if payload:
                return payload
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


@router.get("/login")
async def login(request: Request):
    """Initiate Google OAuth login flow."""
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(
            status_code=500, 
            detail="Google OAuth not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET."
        )
    
    # Determine redirect URI
    redirect_uri = f"{settings.frontend_url}/api/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def auth_callback(request: Request):
    """Handle Google OAuth callback."""
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if not user_info:
            # Fetch user info manually if not in token
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    'https://www.googleapis.com/oauth2/v3/userinfo',
                    headers={'Authorization': f'Bearer {token["access_token"]}'}
                )
                user_info = resp.json()
        
        # Store user in session
        user_data = {
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
            "sub": user_info.get("sub")  # Google's unique user ID
        }
        request.session["user"] = user_data
        
        # Create JWT for API access
        access_token = create_access_token({
            "email": user_data["email"],
            "name": user_data["name"],
            "picture": user_data["picture"]
        })
        
        # Redirect to frontend with success
        return RedirectResponse(url=f"/?auth=success&token={access_token}")
        
    except Exception as e:
        print(f"OAuth error: {e}")
        return RedirectResponse(url="/?auth=error")


@router.get("/me")
async def get_me(request: Request):
    """Get current authenticated user info."""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {
        "authenticated": True,
        "user": user
    }


@router.post("/logout")
async def logout(request: Request):
    """Log out the current user."""
    request.session.clear()
    return {"success": True, "message": "Logged out successfully"}


@router.get("/status")
async def auth_status(request: Request):
    """Check authentication status."""
    user = await get_current_user(request)
    return {
        "authenticated": user is not None,
        "user": user
    }
