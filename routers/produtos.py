from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# Remover import inspect e engine, pois não serão mais usados aqui
from typing import List, Dict, Any # Importar Dict e Any

import models
import schemas # Importar schemas para usar Produto
import database
# Remover import engine
import dependencies

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"],
)

# Endpoint para obter o schema da tabela Produto usando Pydantic
@router.get("/schema", response_model=Dict[str, Any])
def get_produto_schema():
    produto_schema = schemas.Produto.model_json_schema()
    properties = produto_schema.get('properties', {})
    required_fields = set(produto_schema.get('required', []))

    columns_info = []
    for prop_name, prop_details in properties.items():
        # Determina o tipo
        field_type = prop_details.get('type')
        if not field_type and 'anyOf' in prop_details:
            # Tenta encontrar um tipo não nulo em 'anyOf' (comum para Optional)
            types = [t.get('type') for t in prop_details['anyOf'] if t.get('type') != 'null']
            field_type = types[0] if types else 'any'
        elif not field_type and 'format' in prop_details:
             # Caso especial para tipos como datetime ou decimal
             field_type = prop_details.get('format', 'any')
        elif not field_type:
            field_type = 'any' # Fallback

        columns_info.append({
            "name": prop_name,
            "type": field_type,
            "nullable": prop_name not in required_fields,
            "primary_key": prop_name == 'id' # Suposição comum para PK
        })

    schema_info = {
        "table_name": models.Produto.__tablename__,
        "columns": columns_info
    }
    return schema_info

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