#dependencia para proteger rotas
from typing import Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel

from app.core.auth import oauth2_schema
from app.core.config import settings

class TokenData(BaseModel):
    username: Optional[str] = None

def get_current_user(token: str = Depends(oauth2_schema)) -> str:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível autenticar a credencial',
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )

        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        return username
    except JWTError:
        raise credential_exception
