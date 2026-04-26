from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.banco import Base

class ProductModel(Base):
    __tablename__ = "shophub_products"
    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    image_url = Column(String(500))
    description = Column(String(1000))
    stock_quantity = Column(Integer, default=0, nullable=False)
    rating = Column(Float)
    is_active = Column(String(1), default='Y', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    specs = relationship("ProductSpecModel", back_populates="product", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("price >= 0", name='chk_product_price'),
        CheckConstraint("stock_quantity >= 0", name='chk_product_stock'),
        CheckConstraint("is_active IN ('Y', 'N')", name='chk_product_active'),
    )

class ProductSpecModel(Base):
    __tablename__ = "shophub_product_specs"
    spec_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("shophub_products.product_id", ondelete="CASCADE"), nullable=False)
    spec_key = Column(String(100), nullable=False)
    spec_value = Column(String(500), nullable=False)

    product = relationship("ProductModel", back_populates="specs")

    __table_args__ = (
        UniqueConstraint('product_id', 'spec_key', name='uk_product_spec'),
    )

