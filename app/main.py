# -----------------------------------------------------------------------------------
# E-Commerce Backend - ShopHub API
# executando app:
# 1. Instalar as dependências: pip install fastapi uvicorn sqlalchemy pydantic
# 2. servidor: python -muvicorn app.main:app --reload
# 3. SWAGGER: http://localhost:8000/docs
# -----------------------------------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.banco import engine, Base
from app.routers import product, user

# Criação das tabelas no banco de dados SQLite
Base.metadata.create_all(bind=engine)

# CONFIGURAÇÃO DO FASTAPI
app = FastAPI(
    title="ShopHub API",
    description="API para o E-Commerce ShopHub com FastAPI e SQLite",
    version="1.0.0"
)

# Adicionando CORS para permitir conexões do Frontend visual
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo os roteadores modulares (endpoints)
app.include_router(user.router)
app.include_router(product.router)
