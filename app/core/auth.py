#geração de tokens
from pytz import timezone
from typing import Optional
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from pydantic import EmailStr

from app.modelos.user import UserModel
from app.core.config import settings
from app.core.security import verificar_senha


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)


def autenticar(email: EmailStr, senha: str, db: Session) -> Optional[UserModel]:
    usuario = db.query(UserModel).filter(UserModel.email == email).first()

    if not usuario:
        return None

    if not verificar_senha(senha, usuario.password_hash):
        return None

    return usuario


def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    payload = {}

    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida

    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def criar_token_acesso(sub: str) -> str:
    """
    https://jwt.io
    """
    return _criar_token(
        tipo_token='access_token',
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
