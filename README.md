# Academia API

API em FastAPI para cadastrar pessoas e vincular cada aluno a um personal.

Grupo: Alexandre Malta, Christiano Santos, Rafael Santana, João dos Anjos e Luiz Henrique.

## Alterações desta versão

- A antiga tabela `alunos` foi substituída pela tabela `pessoas`.
- Cada pessoa possui o tipo `ALUNO` ou `PERSONAL`.
- Foi criada a tabela `matriculas_alunos`, que relaciona um aluno a um personal.
- O `POST /matriculas/` recebe o ID do aluno e a matrícula do personal.
- O `GET /matriculas/` mostra os dados e o tipo de cada pessoa vinculada.
- A inclusão registra usuário e data; a data é gerada automaticamente.
- O `PUT /matriculas/{id}` registra o usuário e a data da alteração.

## Estrutura das tabelas

### Pessoas

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| matricula | VARCHAR(30) | Matrícula única da pessoa |
| nome | VARCHAR(100) | Nome completo |
| email | VARCHAR(150) | E-mail único |
| telefone | VARCHAR(20) | Telefone |
| tipo_pessoa | ENUM | `ALUNO` ou `PERSONAL` |

### Matrículas dos alunos

| Campo | Tipo | Descrição |
|---|---|---|
| id | INTEGER | Chave primária |
| aluno_id | INTEGER | FK para `pessoas.id` do tipo `ALUNO` |
| personal_id | INTEGER | FK para `pessoas.id` do tipo `PERSONAL` |
| usuario_inclusao | VARCHAR(100) | Usuário que criou o vínculo |
| data_inclusao | DATETIME | Criada automaticamente pelo banco |
| usuario_alteracao | VARCHAR(100) | Usuário da última alteração |
| data_alteracao | DATETIME | Criada automaticamente na alteração |

> No SQLite, o tipo usado é `DATETIME`, equivalente ao uso solicitado para data e hora. Em SQL Server, esse campo pode ser declarado como `SMALLDATETIME`.

## Como executar

No PowerShell, entre na pasta do projeto e execute:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Depois abra:

- Documentação Swagger: <http://127.0.0.1:8000/docs>
- API: <http://127.0.0.1:8000>

Se você executar esta versão dentro da pasta de uma versão antiga, apague uma vez o arquivo `academia.db` antes de iniciar. Ele será recriado automaticamente com as novas tabelas. O ZIP entregue não contém banco antigo.

## Ordem para testar no Swagger

### 1. Criar um personal

`POST /pessoas/`

```json
{
  "matricula": "P001",
  "nome": "Carlos Silva",
  "email": "carlos@email.com",
  "telefone": "11988887777",
  "tipo_pessoa": "PERSONAL"
}
```

### 2. Criar um aluno

`POST /pessoas/`

```json
{
  "matricula": "A001",
  "nome": "João dos Anjos",
  "email": "joao@email.com",
  "telefone": "11999998888",
  "tipo_pessoa": "ALUNO"
}
```

### 3. Vincular o aluno ao personal

Use no campo `aluno_id` o ID retornado ao criar o aluno. No campo `matricula_personal`, use a matrícula do personal:

`POST /matriculas/`

```json
{
  "aluno_id": 2,
  "matricula_personal": "P001",
  "usuario_inclusao": "admin"
}
```

`data_inclusao` não aparece no corpo do POST porque é preenchida automaticamente.

### 4. Alterar o personal do aluno

Depois de cadastrar outro personal, use:

`PUT /matriculas/1`

```json
{
  "matricula_personal": "P002",
  "usuario_alteracao": "rafael"
}
```

`data_alteracao` também não é enviada manualmente.

## Rotas

| Método | Rota | Função |
|---|---|---|
| GET | `/pessoas/` | Lista pessoas; aceita filtros `nome` e `tipo_pessoa` |
| GET | `/pessoas/{id}` | Busca uma pessoa |
| POST | `/pessoas/` | Cadastra aluno ou personal |
| PUT | `/pessoas/{id}` | Atualiza uma pessoa |
| DELETE | `/pessoas/{id}` | Exclui uma pessoa sem vínculo |
| GET | `/matriculas/` | Lista vínculos com tipos das pessoas |
| GET | `/matriculas/{id}` | Busca um vínculo |
| POST | `/matriculas/` | Vincula aluno a personal pela matrícula do personal |
| PUT | `/matriculas/{id}` | Altera o personal e registra auditoria |
| DELETE | `/matriculas/{id}` | Exclui um vínculo |
