from sqlalchemy.orm import Session
from app.modelos.user import UserModel
from app.schemas.user import UserCreate

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    fake_password_hash = f"hashed_{user.password}"
    new_user = UserModel(
        full_name=user.full_name,
        email=user.email,
        password_hash=fake_password_hash,
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
