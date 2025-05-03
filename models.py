from sqlalchemy import Column, Integer, String, Text, Numeric, SmallInteger, DateTime, Index
from sqlalchemy.sql import func
from database import Base
import datetime

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, index=True)
    descricao = Column(Text)
    valor = Column(Numeric(10, 2), nullable=False)
    nota = Column(SmallInteger, nullable=True)
    link_principal = Column(String(512), nullable=False)
    link_secundario = Column(String(512))
    imagem_url = Column(String(512))
    thumbnail_url = Column(String(512))
    categoria = Column(String(128))
    subcategorias = Column(String(128))
    # Usando timezone=True para TIMESTAMP WITH TIME ZONE
    # Default no lado do servidor é geralmente preferível, mas func.now() funciona bem
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    # O índice idx_nome já está coberto pelo index=True no campo nome
    # Se precisar de índices compostos ou outros tipos, defina-os aqui:
    # __table_args__ = (Index('idx_categoria_subcategorias', 'categoria', 'subcategorias'),)