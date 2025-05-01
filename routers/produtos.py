from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
import database
import dependencies

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"],
)

# Endpoint público para obter a contagem de produtos
@router.get("/count", response_model=int)
def count_produtos(db: Session = Depends(database.get_db)):
    count = db.query(models.Produto).count()
    return count

# Endpoint público para listar todos os produtos
@router.get("/", response_model=List[schemas.Produto])
def read_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    produtos = db.query(models.Produto).offset(skip).limit(limit).all()
    return produtos

# Endpoint público para obter um produto específico pelo ID
@router.get("/{produto_id}", response_model=schemas.Produto)
def read_produto(produto_id: int, db: Session = Depends(database.get_db)):
    db_produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

# Endpoint protegido para criar um novo produto (requer autenticação)
@router.post("/", response_model=schemas.Produto, status_code=status.HTTP_201_CREATED)
def create_produto(
    produto: schemas.ProdutoCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.TokenData = Depends(dependencies.get_current_user) # Protege a rota
):
    # Aqui você pode adicionar lógica extra, como gerar thumbnail se imagem_url for fornecida
    db_produto = models.Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

# Endpoint protegido para atualizar um produto existente (requer autenticação)
@router.put("/{produto_id}", response_model=schemas.Produto)
def update_produto(
    produto_id: int,
    produto: schemas.ProdutoCreate, # Usa o mesmo schema da criação para atualização
    db: Session = Depends(database.get_db),
    current_user: schemas.TokenData = Depends(dependencies.get_current_user) # Protege a rota
):
    db_produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Atualiza os campos do produto existente com os dados recebidos
    for var, value in vars(produto).items():
        setattr(db_produto, var, value) if value is not None else None

    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

# Endpoint protegido para deletar um produto (requer autenticação)
@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produto(
    produto_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.TokenData = Depends(dependencies.get_current_user) # Protege a rota
):
    db_produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(db_produto)
    db.commit()
    return # Retorna None com status 204