from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductSpecBase(BaseModel):
    spec_key: str
    spec_value: str

class ProductSpecResponse(ProductSpecBase):
    spec_id: int
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    price: float
    category: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    stock_quantity: int = 0
    rating: Optional[float] = None
    is_active: str = 'Y'

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    product_id: int
    created_at: datetime
    specs: List[ProductSpecResponse] = []
    class Config:
        orm_mode = True
