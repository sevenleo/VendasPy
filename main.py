from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware # Adicionado para permitir requisições do front-end
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
import os

from database import engine, Base, get_db # Importar engine e Base
import models # Importar models para criar tabelas
from routers import auth, produtos # Importar os roteadores

# Carregar variáveis de ambiente do .env
load_dotenv()

# Criar tabelas do banco de dados (se não existirem)
# Em produção, é melhor usar ferramentas de migração como Alembic
models.Base.metadata.create_all(bind=engine)

# Configurar o limitador de taxa (rate limiter)
RATE_LIMIT = os.getenv("RATE_LIMIT", "100/minute") # Pega do .env ou usa default
limiter = Limiter(key_func=get_remote_address, default_limits=[RATE_LIMIT])

app = FastAPI(
    title="VendasPy API",
    description="API para gestão de links de vendas de produtos.",
    version="0.1.0"
)

# Adicionar middleware do rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Adicionar middleware CORS para permitir requisições de diferentes origens (ex: front-end)
# Ajuste origins conforme necessário para produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite todas as origens (cuidado em produção)
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

# Incluir os roteadores
app.include_router(auth.router)
app.include_router(produtos.router)

# Endpoint raiz simples
@app.get("/")
async def root():
    return {"message": "Bem-vindo à VendasPy API"}

# Comando para rodar a aplicação (exemplo):
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload