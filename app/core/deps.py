#dependencia para proteger rotas
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.banco import get_db
from app.core.auth import oauth2_schema
from app.core.config import settings
from app.modelos.user import UserModel


class TokenData(BaseModel):
    username: Optional[str] = None


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_schema)) -> UserModel:
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

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    usuario = db.query(UserModel).filter(UserModel.user_id == int(token_data.username)).first()

    if usuario is None:
        raise credential_exception

    return usuario
