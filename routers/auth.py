from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

import schemas
import dependencies
import database

load_dotenv()

router = APIRouter(
    tags=["Authentication"],
)

ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS") # Lembre-se que a senha no .env deve ser a real

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Neste MVP simples, verificamos diretamente contra as variáveis de ambiente
    # Em um sistema real, você buscaria o usuário no banco e compararia o hash da senha
    is_correct_username = form_data.username == ADMIN_USER
    # Usar verify_password se a senha no .env estivesse hasheada
    # is_correct_password = dependencies.verify_password(form_data.password, HASHED_ADMIN_PASS)
    # Como a senha no .env está em texto plano (não ideal para produção), comparamos diretamente
    is_correct_password = form_data.password == ADMIN_PASS

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = dependencies.create_access_token(
        data={"sub": form_data.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}