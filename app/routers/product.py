from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.banco import get_db
from app.core.deps import get_current_user
from app.schemas.product import ProductCreate, ProductResponse, ProductSpecBase, ProductSpecResponse
from app.crud import product as crud_product

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return crud_product.create_product(db=db, product=product)

@router.get("/", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_product.get_products(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud_product.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    product = crud_product.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    crud_product.delete_product(db, product_id=product_id)
    return {"message": "Produto deletado com sucesso. Especificações também foram deletadas via CASCADE."}

@router.post("/{product_id}/specs/", response_model=ProductSpecResponse)
def create_product_spec(product_id: int, spec: ProductSpecBase, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    product = crud_product.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    try:
        return crud_product.create_product_spec(db, product_id=product_id, spec=spec)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro ao adicionar spec (Possível chave duplicada).")
