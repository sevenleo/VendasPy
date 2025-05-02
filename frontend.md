# Guia para Desenvolvimento do Frontend - VendasPy API

Este documento fornece as informações essenciais para construir uma aplicação frontend que interaja com a API VendasPy.

## Informações Gerais

*   **URL Base da API:** `https://vendaspy.onrender.com`
*   **Porta Padrão:** 80 (implícita para HTTP) / 443 (implícita para HTTPS). Use a URL base diretamente.
*   **Formato de Dados:** JSON

## Autenticação

*   **Método:** JSON Web Tokens (JWT)
*   **Endpoint de Login:** `POST /login`
    *   **Corpo da Requisição:** `username` (string) e `password` (string) em formato `application/x-www-form-urlencoded`.
    *   **Resposta:** Retorna um `access_token` e `token_type` (Bearer).
*   **Uso do Token:** Para acessar endpoints protegidos, inclua o token no cabeçalho `Authorization` da requisição:
    ```
    Authorization: Bearer <seu_token_jwt>
    ```

## Endpoints da API

### Produtos (`/produtos`)

*   **Obter Schema da Tabela:**
    *   `GET /produtos/schema`
    *   **Descrição:** Retorna a estrutura da tabela `produtos`, incluindo nome das colunas, tipos de dados, se são nulos e se são chave primária. Útil para construir formulários dinamicamente.
    *   **Autenticação:** Pública
    *   **Exemplo de Uso:** `https://vendaspy.onrender.com/produtos/schema`
    *   **Exemplo de Resposta:**
        ```json
        {
          "table_name": "produtos",
          "columns": [
            {
              "name": "id",
              "type": "integer",
              "nullable": false,
              "primary_key": true
            },
            {
              "name": "nome",
              "type": "string",
              "nullable": false,
              "primary_key": false
            },
            // ... outros campos
          ]
        }
        ```

*   **Listar Todos os Produtos:**
    *   `GET /produtos/`
    *   **Descrição:** Retorna uma lista de todos os produtos. Suporta paginação com query parameters `skip` (padrão 0) e `limit` (padrão 100).
    *   **Autenticação:** Pública
    *   **Exemplo de Uso:** `https://vendaspy.onrender.com/produtos/?skip=0&limit=10`

*   **Obter Contagem de Produtos:**
    *   `GET /produtos/count`
    *   **Descrição:** Retorna o número total de produtos cadastrados.
    *   **Autenticação:** Pública
    *   **Exemplo de Uso:** `https://vendaspy.onrender.com/produtos/count`

*   **Obter um Produto Específico:**
    *   `GET /produtos/{produto_id}`
    *   **Descrição:** Retorna os detalhes de um produto específico pelo seu ID.
    *   **Autenticação:** Pública
    *   **Exemplo de Uso:** `https://vendaspy.onrender.com/produtos/1`

*   **Criar um Novo Produto:**
    *   `POST /produtos/`
    *   **Descrição:** Cria um novo registro de produto.
    *   **Autenticação:** Requer JWT (Usuário logado)
    *   **Corpo da Requisição:** Objeto JSON com os dados do produto (conforme schema `ProdutoCreate` - use o endpoint `/schema` para referência, excluindo `id` e `criado_em`).
    *   **Exemplo de Uso:** `https://vendaspy.onrender.com/produtos/`

*   **Atualizar um Produto Existente:**
    *   `PUT /produtos/{produto_id}`
    *   **Descrição:** Atualiza os dados de um produto existente.
    *   **Autenticação:** Requer JWT (Usuário logado)
    *   **Corpo da Requisição:** Objeto JSON com os dados atualizados do produto (conforme schema `ProdutoCreate`).
    *   **Exemplo de Uso:** `https://vendaspy.onrender.com/produtos/1`

*   **Deletar um Produto:**
    *   `DELETE /produtos/{produto_id}`
    *   **Descrição:** Remove um produto do banco de dados.
    *   **Autenticação:** Requer JWT (Usuário logado)
    *   **Exemplo de Uso:** `https://vendaspy.onrender.com/produtos/1`

## Considerações Adicionais

*   **CORS:** A API está configurada para aceitar requisições de qualquer origem (`*`). Em produção, pode ser necessário restringir isso.
*   **Rate Limiting:** Existe um limite de requisições por IP para prevenir abuso (configurado no backend, atualmente `100/minute`). O frontend deve tratar possíveis erros `429 Too Many Requests`.
*   **Tratamento de Erros:** A API retorna códigos de status HTTP apropriados (e.g., 404 para não encontrado, 401/403 para não autorizado, 422 para validação, 500 para erros internos). O frontend deve tratar esses erros adequadamente.