from sqlalchemy.orm import Session
from app.modelos.product import ProductModel, ProductSpecModel
from app.schemas.product import ProductCreate, ProductSpecBase

def create_product(db: Session, product: ProductCreate):
    new_product = ProductModel(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductModel).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.product_id == product_id).first()

def delete_product(db: Session, product: ProductModel):
    db.delete(product)
    db.commit()

def create_product_spec(db: Session, product_id: int, spec: ProductSpecBase):
    new_spec = ProductSpecModel(
        product_id=product_id,
        spec_key=spec.spec_key,
        spec_value=spec.spec_value
    )
    db.add(new_spec)
    db.commit()
    db.refresh(new_spec)
    return new_spec