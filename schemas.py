from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TipoPessoaResponseSchema(BaseModel):
    id: int
    descricao: str

    model_config = ConfigDict(from_attributes=True)


class PessoaBase(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=150)
    telefone: str = Field(min_length=11, max_length=11, pattern=r"^\d{11}$")
    tipo_pessoa_id: int = Field(ge=1, le=2)


class PessoaCreateSchema(PessoaBase):
    pass


class PessoaUpdateSchema(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=100)
    email: str | None = Field(default=None, min_length=5, max_length=150)
    telefone: str | None = Field(default=None, min_length=11, max_length=11, pattern=r"^\d{11}$")
    tipo_pessoa_id: int | None = Field(default=None, ge=1, le=2)


class PessoaResponseSchema(PessoaBase):
    matricula: int
    data_criacao: datetime
    tipo: TipoPessoaResponseSchema

    model_config = ConfigDict(from_attributes=True)


class PessoaResumoSchema(BaseModel):
    matricula: int
    nome: str
    tipo_pessoa_id: int

    model_config = ConfigDict(from_attributes=True)


class MatriculaAlunoCreateSchema(BaseModel):
    aluno_matricula: int = Field(gt=0)
    personal_matricula: int = Field(gt=0)
    usuario_inclusao: str = Field(min_length=2, max_length=100)


class MatriculaAlunoUpdateSchema(BaseModel):
    personal_matricula: int = Field(gt=0)
    usuario_alteracao: str = Field(min_length=2, max_length=100)


class MatriculaAlunoResponseSchema(BaseModel):
    id: int
    aluno: PessoaResumoSchema
    personal: PessoaResumoSchema
    usuario_inclusao: str
    data_inclusao: datetime
    usuario_alteracao: str | None
    data_alteracao: datetime | None

    model_config = ConfigDict(from_attributes=True)


class TreinoBaseSchema(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    descricao: str | None = Field(default=None, max_length=1000)
    objetivo: str | None = Field(default=None, max_length=150)
    nivel: str | None = Field(default=None, max_length=30)


class TreinoCreateSchema(TreinoBaseSchema):
    pass


class TreinoUpdateSchema(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=100)
    descricao: str | None = Field(default=None, max_length=1000)
    objetivo: str | None = Field(default=None, max_length=150)
    nivel: str | None = Field(default=None, max_length=30)


class TreinoResponseSchema(TreinoBaseSchema):
    id: int
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)


class FichaTreinoCreateSchema(BaseModel):
    aluno_matricula: int = Field(gt=0)
    personal_matricula: int = Field(gt=0)
    treino_id: int = Field(gt=0)
    observacoes: str | None = Field(default=None, max_length=1500)


class FichaTreinoUpdateSchema(BaseModel):
    personal_matricula: int | None = Field(default=None, gt=0)
    treino_id: int | None = Field(default=None, gt=0)
    observacoes: str | None = Field(default=None, max_length=1500)


class FichaTreinoResponseSchema(BaseModel):
    id: int
    aluno: PessoaResumoSchema
    personal: PessoaResumoSchema
    treino: TreinoResponseSchema
    observacoes: str | None
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)
