from fastapi import FastAPI

import models
from database import Base, SessionLocal, engine
from routers import fichas_treino, matriculas, pessoas, tipos_pessoa, treinos


Base.metadata.create_all(bind=engine)


def criar_tipos_pessoa_padrao():
    db = SessionLocal()
    try:
        tipos = [
            (1, "ALUNO"),
            (2, "PERSONAL"),
        ]
        for tipo_id, descricao in tipos:
            existe = db.query(models.TipoPessoa).filter(models.TipoPessoa.id == tipo_id).first()
            if not existe:
                db.add(models.TipoPessoa(id=tipo_id, descricao=descricao))
        db.commit()
    finally:
        db.close()


criar_tipos_pessoa_padrao()

app = FastAPI(
    title="Academia FitTec",
    description=(
        "API da Academia FitTec para gerenciamento de alunos, personal trainers, "
        "matrículas, treinos e fichas de treino."
    ),
    version="3.0.0",
)

app.include_router(pessoas.router)
app.include_router(tipos_pessoa.router)
app.include_router(matriculas.router)
app.include_router(treinos.router)
app.include_router(fichas_treino.router)


@app.get("/", tags=["Início"])
def inicio():
    return {"status": "API Academia FitTec funcionando!"}
