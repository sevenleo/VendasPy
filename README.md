# VendasPy - API de Gestão de Produtos com FastAPI

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Descrição do Projeto

Sistema desenvolvido com arquitetura moderna para gestão completa de catálogos de produtos, combinando alta performance com segurança robusta. Desenvolvido em Python 3.9+ e FastAPI 0.68+, oferece:

**Principais características técnicas:**
- Arquitetura assíncrona para alta concorrência
- Sistema de autenticação JWT com refresh tokens
- Camada ORM modular para suporte multiplataforma a bancos de dados (PostgreSQL, MySQL, SQLite)
- Interface administrativa integrada com Swagger UI
- Validação de dados em tempo real com Pydantic v2
- Sistema de rate limiting adaptável

**Benefícios chave:**
✅ Escalabilidade vertical e horizontal
✅ Documentação API automática (OpenAPI 3.0)
✅ Configuração via ambiente com herança de perfis
✅ Logs estruturados para monitoramento
✅ Testes unitários e de integração (pytest)

- Autenticação JWT segura
- CRUD completo de produtos
- Interface web dinâmica
- API RESTful com documentação automática
- Suporte a múltiplos bancos de dados (PostgreSQL, MySQL, SQLite)

## Funcionalidades Principais

✅ Autenticação via JWT com tempo de expiração
✅ Operações CRUD completas para produtos
✅ Validação de dados com Pydantic
✅ Rate limiting configurável
✅ Geração automática de documentação OpenAPI
✅ Configuração via variáveis de ambiente

## Instalação e Configuração

1. **Clonar repositório**
```bash
git clone https://github.com/seu-usuario/VendasPy.git
cd VendasPy
```

2. **Instalar dependências**
```bash
pip install -r requirements.txt
```

3. **Configurar ambiente**
Criar arquivo `.env` com:
```ini
ADMIN_USER=admin
ADMIN_PASS=senha_segura
JWT_SECRET=chave_secreta_aleatoria
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dbname
```

4. **Executar servidor**
```bash
uvicorn main:app --reload
```

## Documentação da API

Acesse a documentação interativa em:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (Redoc)

### Endpoints Principais

| Método | Endpoint       | Descrição                  | Autenticação |
|--------|----------------|---------------------------|--------------|
| POST   | /login         | Obter token JWT           | Pública      |
| GET    | /produtos      | Listar todos produtos      | Pública      |
| POST   | /produtos      | Criar novo produto         | Admin        |
| PUT    | /produtos/{id} | Atualizar produto          | Admin        |
| DELETE | /produtos/{id} | Remover produto            | Admin        |

## Estrutura do Projeto

```
VendasPy/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── routers/
│   ├── auth.py
│   └── produtos.py
├── dependencies.py
├── requirements.txt
└── README.md
```