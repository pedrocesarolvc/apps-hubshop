# -----------------------------------------------------------------------------------
# E-Commerce Backend - ShopHub API
# executando app:
# 1. Instalar as dependências: pip install fastapi uvicorn sqlalchemy pydantic
# 2. servidor: uvicorn main:app --reload
# 3. SWAGGER: http://localhost:8000/docs
# -----------------------------------------------------------------------------------


from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

#tabelas SQLite
Base.metadata.create_all(bind=engine)


#CONFIGURAÇÃO DO FASTAPI
app = FastAPI(
    title="ShopHub API",
    description="API para o E-Commerce ShopHub com FastAPI e SQLite",
    version="1.0.0"
)

#Adicionando CORS para permitir conexões do Frontend visual
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#ENDPOINTS DE USUÁRIOS(CRUD) 


@app.get("/users/", response_model=List[UserResponse], tags=["Users"])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users


#ENDPOINTS DE PRODUTOS(CRUD)

@app.post("/products/", response_model=ProductResponse, tags=["Products"])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = ProductModel(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products/", response_model=List[ProductResponse], tags=["Products"])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(ProductModel).offset(skip).limit(limit).all()
    return products

@app.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/products/{product_id}", tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Produto deletado com sucesso. Especificações também foram deletadas via CASCADE."}


#ENDPOINTS DE ESPECIFICAÇÕES DE PRODUTOS(CRUD)

@app.post("/products/{product_id}/specs/", response_model=ProductSpecResponse, tags=["Product Specs"])
def create_product_spec(product_id: int, spec: ProductSpecBase, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    new_spec = ProductSpecModel(
        product_id=product_id,
        spec_key=spec.spec_key,
        spec_value=spec.spec_value
    )
    try:
        db.add(new_spec)
        db.commit()
        db.refresh(new_spec)
        return new_spec
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro ao adicionar spec (Possível chave duplicada).")