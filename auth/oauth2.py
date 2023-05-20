from typing import Optional
from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from db.usuario_db import get_usuario_by_email
from schemas.schemas import UsuarioResponse

from core.settings import setting

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY: str = setting.get_secret_key()
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire.timestamp()})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def is_token_expired(exp_time: int) -> bool:
    curr_dt = datetime.utcnow()
    timestamp = curr_dt.timestamp()

    if timestamp > exp_time:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    return False


def get_current_user(token: str = Depends(oauth2_schema)) -> UsuarioResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        exp_time: Optional[int] = payload.get("exp")
        username: Optional[str] = payload.get("username")

        if username is None or exp_time is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    if not is_token_expired(exp_time):
        user: Optional[UsuarioResponse] = get_usuario_by_email(username)

        if user is None:
            raise credentials_exception

        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token has expired"
    )
