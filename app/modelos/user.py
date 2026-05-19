from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from datetime import datetime
from app.banco import Base

class UserModel(Base):
    __tablename__ = "shophub_users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password= Column(String, nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(255))
    account_type = Column(String(20), default='cliente', nullable=False)
    terms_accepted = Column(String(1), default='Y', nullable=False)
    is_active = Column(String(1), default='Y', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint("account_type IN ('cliente', 'loja')", name='chk_account_type'),
        CheckConstraint("terms_accepted = 'Y'", name='chk_terms'),
        CheckConstraint("is_active IN ('Y', 'N')", name='chk_is_active'),
    )

