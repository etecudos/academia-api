# Academia API

API para gerenciamento de alunos e treinos de uma academia.
Grupo: Alexandre Malta, Christiano Santos, Rafael Santana, João dos Anjos e Luiz Henrique.

## Estrutura das Tabelas

### Tabela 1 — Alunos

| Campo | Tipo | Descrição |
|---|---|---|
| id | INT | Identificador único do aluno |
| nome | VARCHAR(100) | Nome completo do aluno |
| email | VARCHAR(150) | E-mail do aluno |
| telefone | VARCHAR(20) | Telefone do aluno |

### Tabela 2 — Treinos

| Campo | Tipo | Descrição |
|---|---|---|
| id | INT | Identificador único do treino |
| nome | VARCHAR(100) | Nome do treino |
| descricao | VARCHAR(255) | Descrição do treino |
| aluno_id | INT | Identificador do aluno relacionado |

### Relacionamento

A tabela `treinos` possui o campo `aluno_id`, que funciona como chave estrangeira relacionada ao campo `id` da tabela `alunos`.

**Relacionamento:** `treinos.aluno_id` -> `alunos.id`

## Contrato das Rotas HTTP

### GET /

Retorna uma mensagem informando que a API está funcionando.

**Resposta de sucesso — HTTP 200:**

```json
{
  "status": "API da Academia funcionando!"
}

## Atualização - Entrega 03 (Arquitetura em Camadas)

Nesta etapa, a API foi refatorada para seguir o padrão de **Arquitetura em Camadas** e agora possui persistência de dados utilizando banco de dados relacional.

* **Banco de Dados:** SQLite
* **ORM:** SQLAlchemy
* **Validação de Dados:** Pydantic (Schemas separados para Requisição e Resposta)
* **Controladores:** FastAPI (APIRouter)

### Rotas Implementadas (CRUD de Alunos)

As seguintes rotas interagem diretamente com o banco de dados SQLite:

* **`GET /alunos/`**: Lista todos os alunos cadastrados. Permite busca opcional pelo nome via *Query Parameter*.
* **`GET /alunos/{id}`**: Retorna os detalhes de um aluno específico pelo seu ID. Retorna erro 404 se não existir.
* **`POST /alunos/`**: Cadastra um novo aluno no banco de dados. Retorna status `201 Created` em caso de sucesso.
* **`DELETE /alunos/{id}`**: Remove um aluno do banco de dados pelo seu ID. Retorna erro 404 caso o aluno não seja encontrado.
