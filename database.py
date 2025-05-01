from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv() # Carrega variáveis do arquivo .env

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./vendas.db") # Default para SQLite se não definida

# Ajuste para diferentes dialetos de banco de dados
if DATABASE_URL.startswith("sqlite"):
    # Para SQLite, connect_args é necessário para habilitar o check_same_thread
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Handles PostgreSQL, MySQL, etc. SQLAlchemy lida com os dialetos.
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()