## MIGRAÇÃO DO PROJETO VENDAS - BACKEND EM PYTHON COM FASTAPI  

Este documento serve como prompt detalhado para um desenvolvedor sênior especialista em FastAPI, com o objetivo de replicar exatamente o funcionamento deste backend criado originalmente em PHP, agora totalmente em Python.

## Descrição do Projeto  

O sistema continua sendo um gestor de links de vendas de produtos, pensado para simplificar o cadastro, edição e divulgação de catálogos online. O administrador faz login, gerencia produtos (CRUD) e define categoria e subcategoria. Usuários comuns acessam informações de forma pública sem autenticação.

O fluxo esperado é:  
- O administrador autentica-se via JWT e executa operações de criação, atualização e remoção de produtos;  
- Usuários acessam endpoints públicos para listar ou detalhar produtos;  
- Todas as chamadas administrativas exigem o token válido, enquanto as consultas ficam abertas.

Casos de uso típicos incluem gestão de catálogos de pequenos negócios, criação de landing pages de afiliados e centralização de links para redes sociais.

## Objetivos  

- API minimalista com FastAPI para cadastro, edição, listagem e remoção de produtos, com filtros por categoria e subcategoria;  
- Restringir métodos POST, PUT e DELETE ao administrador autenticado;  
- Endpoints GET públicos;  
- Front-end simples sugerido: navegação, busca por nome/categoria/subcategoria e cards dinâmicos consumindo a API via fetch.

## Requisitos Técnicos  

- Python 3.9 ou superior  
- FastAPI  
- Uvicorn (servidor ASGI)  
- SQLAlchemy ou Tortoise ORM  
- Banco de dados relacional (PostgreSQL, MySQL/MariaDB)  
- Biblioteca PyJWT para tokens  
- Dependência de rate limiting (por exemplo, slowapi)

## Variáveis de Ambiente  

- `API_HOST`: Host onde a API será executada  
- `API_PORT`: Porta ASGI (ex: 8000)  
- `DATABASE_URL`: URL completa de conexão (ex: `postgresql+asyncpg://user:pass@host:port/db`)  
- `ADMIN_USER`: Nome de usuário administrador  
- `ADMIN_PASS`: Senha do administrador  
- `JWT_SECRET`: Segredo para geração e validação de tokens  
- `RATE_LIMIT`: Limite de requisições GET por IP por hora

## Estrutura do Banco de Dados  

```sql
CREATE TABLE IF NOT EXISTS produtos (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  descricao TEXT,
  valor NUMERIC(10,2) NOT NULL,
  nota SMALLINT NOT NULL,
  link_principal VARCHAR(512) NOT NULL,
  link_secundario VARCHAR(512),
  imagem_url VARCHAR(512),
  thumbnail_url VARCHAR(512),
  categoria VARCHAR(128),
  subcategoria VARCHAR(128),
  criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_nome ON produtos(nome);
```  

## Endpoints e Regras  

- Respostas em JSON;  
- JWT obrigatório em POST, PUT e DELETE (via cabeçalho `Authorization: Bearer <token>`);  
- Rate limiting definido por variável de ambiente;  
- Cabeçalhos esperados: `Content-Type: application/json` sempre.

### Endpoints via FastAPI  

- `POST /login`  
  - Body: `{ "usuario": "admin", "senha": "senha123" }`  
  - Retorna: `{ "access_token": "...", "token_type": "bearer" }`  

- `GET /produtos`  
  - Lista todos os produtos  

- `GET /produtos/{id}`  
  - Retorna o produto com o ID especificado  

- `POST /produtos`  
  - Cria novo produto (admin)  

- `PUT /produtos/{id}`  
  - Atualiza produto existente (admin)  

- `DELETE /produtos/{id}`  
  - Remove produto (admin)

### Exemplos de Uso (cURL)  

- Login:
```
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"usuario":"admin","senha":"senha123"}'
```

- Listar produtos:
```
curl http://localhost:8000/produtos
```

- Criar produto:
```
curl -X POST http://localhost:8000/produtos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"nome":"Produto X","descricao":"Desc","valor":99.90,"nota":5,"link_principal":"https://exemplo.com","link_secundario":"","imagem_url":""}'
```

## Lógica de Negócio e Validações  

- Validação de todos os campos obrigatórios via Pydantic;  
- Autenticação e autorização via dependências de FastAPI;  
- Endpoints GET sem necessidade de token;  
- Tokens gerados e verificados com PyJWT em cada chamada protegida;  
- Geração de thumbnails usando biblioteca PIL ou similar (função `generate_thumbnail`).

## Observações de Segurança  

- Jamais commit o `JWT_SECRET` e credenciais no repositório;  
- Use HTTPS em produção;  
- Aplique rate limiting para evitar abuso de API.

## Estrutura de Arquivos Sugerida  

- `main.py`: inicializa a aplicação e inclui roteadores  
- `database.py`: configura conexão e sessão com SQLAlchemy  
- `models.py`: define modelos ORM  
- `schemas.py`: define schemas Pydantic para requisições/respostas  
- `routers/`: contém módulos para endpoints (login, produtos)  
- `dependencies.py`: verificação de token e rate limiting  
- `utils.py`: funções auxiliares (ex: `generate_thumbnail`)

## Prompt para Desenvolvedor Sênior  

Nós precisamos replicar exatamente esta API descrita, garantindo autenticação JWT, rate limiting, estrutura de banco, validações, endpoints e retornos JSON. O sistema deve ser seguro, performático e fácil de manter, com front-end simples consumindo a API via fetch e exibindo produtos em cards dinâmicos.

