from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

import schemas
import database

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token expira em 30 minutos

# Contexto para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema OAuth2 para obter o token do cabeçalho Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Função para verificar a senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para gerar o hash da senha
def get_password_hash(password):
    return pwd_context.hash(password)

# Função para criar o token de acesso JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    # Implementar expiração se necessário
    # expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

# Função de dependência para obter o usuário atual a partir do token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # Aqui você poderia buscar o usuário no banco de dados se necessário
    # Por simplicidade, vamos apenas retornar os dados do token por enquanto
    # user = get_user(db, username=token_data.username)
    # if user is None:
    #     raise credentials_exception

    # Verifica se o usuário é o admin definido nas variáveis de ambiente
    admin_user = os.getenv("ADMIN_USER")
    if token_data.username != admin_user:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )

    return token_data # Retorna os dados do token (contendo o username)

# Aqui poderia ser adicionada a dependência de rate limiting (slowapi)
# Exemplo básico (requer instalação e configuração do slowapi):
# from slowapi import Limiter, _rate_limit_exceeded_handler
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded

# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# # Exemplo de uso em um endpoint:
# @app.get("/limitado")
# @limiter.limit("5/minute")
# async def limited_route(request: Request):
#     return {"message": "Esta rota tem limite de taxa"}