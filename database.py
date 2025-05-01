from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv() # Carrega variáveis do arquivo .env

DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não está definida no arquivo .env")

# Configuração do engine SQLAlchemy com base no DB_TYPE
if DB_TYPE == "sqlite":
    # Para SQLite, connect_args é necessário para habilitar o check_same_thread
    # Garante que o caminho seja relativo à raiz do projeto se começar com ./ ou .
    if DATABASE_URL.startswith("sqlite:///./"): 
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), DATABASE_URL.split("sqlite:///./")[1])
        DATABASE_URL = f"sqlite:///{db_path}"
    elif DATABASE_URL.startswith("sqlite:///."): # Caso use apenas .
         db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), DATABASE_URL.split("sqlite:///.")[1])
         DATABASE_URL = f"sqlite:///{db_path}"
    
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
elif DB_TYPE == "mysql":
    # Assume mysql+mysqlconnector
    engine = create_engine(DATABASE_URL)
elif DB_TYPE == "postgresql":
    # Assume postgresql+psycopg2
    engine = create_engine(DATABASE_URL)
else:
    raise ValueError(f"Tipo de banco de dados não suportado: {DB_TYPE}. Use 'sqlite', 'mysql' ou 'postgresql'.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()