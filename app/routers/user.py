from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.banco import get_db
from app.core.auth import criar_token_acesso
from app.core.deps import get_current_user
from app.schemas.user import UserCreate, UserResponse
from app.crud import user as crud_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Sistema simplificado para Administrador
    if form_data.password != "Adm@1":
        raise HTTPException(status_code=400, detail="Senha ou email incorretos")
    
    access_token = criar_token_acesso(sub=form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud_user.create_user(db=db, user=user)

@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return crud_user.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = crud_user.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user