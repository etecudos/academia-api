from pydantic import BaseModel

class AlunoBase(BaseModel):
    nome: str
    email: str
    telefone: str

class AlunoCreateSchema(AlunoBase):
    pass

class AlunoResponseSchema(AlunoBase):
    id: int

    class Config:
        from_attributes = True