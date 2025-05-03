from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import decimal # Import decimal for Numeric type handling

# Schema base para Produto, com campos comuns
class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    valor: decimal.Decimal # Use decimal.Decimal for currency/numeric precision
    nota: int
    link_principal: str
    link_secundario: Optional[str] = None
    imagem_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    categoria: Optional[str] = None
    subcategorias: Optional[str] = None

    # Pydantic v2 config for ORM mode
    class Config:
       #orm_mode = True
       from_attributes = True
        # If using Pydantic v1, use: from_attributes = True

# Schema para criação de Produto (herda de ProdutoBase)
class ProdutoCreate(ProdutoBase):
    pass # No extra fields needed for creation beyond base

# Schema para leitura de Produto (herda de ProdutoBase, adiciona campos do DB)
class Produto(ProdutoBase):
    id: int
    criado_em: datetime

# Schema para o Token JWT
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema para os dados dentro do Token JWT
class TokenData(BaseModel):
    username: Optional[str] = None

# Schema para o login do usuário
class User(BaseModel):
    username: str
    password: str