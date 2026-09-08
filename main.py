from fastapi import FastAPI
from database import engine, Base
from routers import alunos

# Cria as tabelas no banco de dados ao iniciar
Base.metadata.create_all(bind=engine)

# Mantendo as informações do seu projeto original
app = FastAPI(
    title="Academia API",
    description="API para gerenciamento de alunos e treinos.",
    version="1.0.0"
)

# Incluindo as rotas
app.include_router(alunos.router)

# Mantendo sua rota principal original
@app.get("/")
def inicio():
    return {
        "status": "API da Academia funcionando!"
    }