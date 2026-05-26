from sqlalchemy.orm import Session
from app.modelos.user import UserModel
from app.schemas.user import UserCreate
from app.core.security import gerar_hash_senha

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.user_id == user_id).first()

def create_user(db: Session, user: UserCreate):
    senha_criptografada = gerar_hash_senha(user.password)
    new_user = UserModel(
        full_name=user.full_name,
        email=user.email,
        password_hash=senha_criptografada,
        phone=user.phone,
        address=user.address,
        account_type=user.account_type,
        terms_accepted=user.terms_accepted,
        is_active=user.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
