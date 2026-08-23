from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title="Academia API",
    description="API para gerenciamento de alunos e treinos.",
    version="1.0.0"
)


class AlunoSchema(BaseModel):
    nome: str
    email: str
    telefone: str


alunos = [
    {
        "id": 1,
        "nome": "João dos Anjos",
        "email": "joao@email.com",
        "telefone": "11999999999"
    },
    {
        "id": 2,
        "nome": "Rafael Alves",
        "email": "rafael@email.com",
        "telefone": "11888888888"
    },
    {
        "id": 3,
        "nome": "Luiz Henrique",
        "email": "luiz@email.com",
        "telefone": "11777777777"
    },
    {
        "id": 4,
        "nome": "Alexandre Malta",
        "email": "ale@email.com",
        "telefone": "11666666666"
    },
    {
        "id": 5,
        "nome": "Cristiano Santos",
        "email": "cristiano@email.com",
        "telefone": "11555555555"
    }
]


@app.get("/")
def inicio():
    return {
        "status": "API da Academia funcionando!"
    }


@app.get("/alunos")
def listar_alunos(nome: str | None = None):
    if nome:
        return [
            aluno for aluno in alunos
            if nome.lower() in aluno["nome"].lower()
        ]

    return alunos


@app.get("/alunos/{id}")
def buscar_aluno(id: int):
    for aluno in alunos:
        if aluno["id"] == id:
            return aluno

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Aluno não encontrado."
    )


@app.post("/alunos", status_code=status.HTTP_201_CREATED)
def cadastrar_aluno(aluno: AlunoSchema):
    novo_id = max([aluno["id"] for aluno in alunos], default=0) + 1

    novo_aluno = {
        "id": novo_id,
        "nome": aluno.nome,
        "email": aluno.email,
        "telefone": aluno.telefone
    }

    alunos.append(novo_aluno)

    return novo_aluno


@app.delete("/alunos/{id}")
def excluir_aluno(id: int):
    for aluno in alunos:
        if aluno["id"] == id:
            alunos.remove(aluno)

            return {
                "mensagem": "Aluno removido com sucesso."
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Aluno não encontrado."
    )