# Academia API

API para gerenciamento de alunos e treinos de uma academia.

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