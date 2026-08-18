from fastapi import FastAPI

app = FastAPI(
    title="Academia API",
    description="API para gerenciamento de alunos e treinos.",
    version="1.0.0"
)

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
def listar_alunos():
    return alunos