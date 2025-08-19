from typing import Optional

from fastapi import Cookie, HTTPException, Header, Request, Response
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.main import Session, get_db, make_jwt, read_jwt, settings
from app.model.user import User
from . import router


JWT_COOKIE_NAME = "vaultml_token"

def user_from_auth(auth_header: Optional[str] = None, jwt_cookie: Optional[str] = None) -> int:
    token = None
    
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]
    elif jwt_cookie:
        token = jwt_cookie
    if not token:
        raise HTTPException(401, "Missing token")
    return read_jwt(token)


def read_token(authorization: Optional[str], jwt_cookie: Optional[str]) -> str:
    """Pick token from Authorization: Bearer ... or from cookie."""
    if authorization and authorization.startswith("Bearer "):
        return authorization.split(" ", 1)[1]
    if jwt_cookie:
        return jwt_cookie
    raise HTTPException(401, "Missing token")

def current_user_id(
    authorization: Optional[str] = Header(None),
    jwt_cookie: Optional[str] = Cookie(default=None, alias=JWT_COOKIE_NAME),
) -> int:
    token = read_token(authorization, jwt_cookie)
    return read_jwt(token)


class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/signup")
async def signup(body: SignupRequest, db: Session = Depends(get_db)):
    from passlib.hash import bcrypt
    u = User(email=body.email, username=body.email, password_hash=bcrypt.hash(body.password))
    db.add(u)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(400, "Email exists")
    return {"token": make_jwt(u.id)}  

@router.post("/auth/login")
async def login(body: LoginRequest, response: Response, db: Session = Depends(get_db)):
    from passlib.hash import bcrypt
    u = (await db.execute(select(User).where(User.username == body.username))).scalar_one_or_none()
    if not u or not bcrypt.verify(body.password, u.password_hash):
        raise HTTPException(401, "Bad credentials")

    token = make_jwt(u.id)
    response.set_cookie(
        key=JWT_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,      
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
        path="/",
        domain=settings.DOMAIN_NAME,
    )
    return {"ok": True}

@router.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie(JWT_COOKIE_NAME, path="/", domain=settings.DOMAIN_NAME)
    return {"ok": True}


@router.get("/auth/me")
async def me(
    authorization: Optional[str] = Header(None),
    jwt: Optional[str] = Cookie(default=None, alias=JWT_COOKIE_NAME),
):
    uid = user_from_auth(authorization, jwt)
    return {"user_id": uid}
@router.get("/debug/cookies")
async def debug_cookies(request: Request):
    return {"cookies": request.cookies}

