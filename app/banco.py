#colocar recursos de banco e url para chamar o banco
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#configurando o banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./shophub.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#dependencias para pegar a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()