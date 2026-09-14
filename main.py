from fastapi import FastAPI

from database import Base, engine
from routers import matriculas, pessoas


# Para a atividade, as tabelas são criadas automaticamente ao iniciar a API.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Academia API",
    description="API para gerenciamento de pessoas e matrículas de alunos.",
    version="2.0.0",
)

app.include_router(pessoas.router)
app.include_router(matriculas.router)


@app.get("/", tags=["Início"])
def inicio():
    return {"status": "API da Academia funcionando!"}
