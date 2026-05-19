from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from app.banco import get_db
from app.core.auth import autenticar, criar_token_acesso
from app.schemas.user import UserCreate, UserResponse
from app.crud import user as crud_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auntenticar(email=form_data.username, senha=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")
    
    access_token = criar_token_acesso(sub=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud_user.create_user(db=db, user=user)

@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_user.get_users(db, skip=skip, limit=limit)