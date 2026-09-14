from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TipoPessoa(str, Enum):
    ALUNO = "ALUNO"
    PERSONAL = "PERSONAL"


class PessoaBase(BaseModel):
    matricula: str = Field(min_length=1, max_length=30)
    nome: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=150)
    telefone: str = Field(
        min_length=8,
        max_length=20,
        pattern=r"^\d+$"
    )
    tipo_pessoa: TipoPessoa


class PessoaCreateSchema(PessoaBase):
    pass


class PessoaUpdateSchema(BaseModel):
    matricula: str | None = Field(
        default=None,
        min_length=1,
        max_length=30
    )
    nome: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    email: str | None = Field(
        default=None,
        min_length=5,
        max_length=150
    )
    telefone: str | None = Field(
        default=None,
        min_length=8,
        max_length=20,
        pattern=r"^\d+$"
    )
    tipo_pessoa: TipoPessoa | None = None


class PessoaResponseSchema(PessoaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PessoaResumoSchema(BaseModel):
    id: int
    matricula: str
    nome: str
    tipo_pessoa: TipoPessoa

    model_config = ConfigDict(from_attributes=True)


class MatriculaAlunoCreateSchema(BaseModel):
    aluno_id: int = Field(gt=0)
    matricula_personal: str = Field(
        min_length=1,
        max_length=30
    )
    usuario_inclusao: str = Field(
        min_length=2,
        max_length=100
    )


class MatriculaAlunoUpdateSchema(BaseModel):
    matricula_personal: str = Field(
        min_length=1,
        max_length=30
    )
    usuario_alteracao: str = Field(
        min_length=2,
        max_length=100
    )


class MatriculaAlunoResponseSchema(BaseModel):
    id: int
    aluno: PessoaResumoSchema
    personal: PessoaResumoSchema
    usuario_inclusao: str
    data_inclusao: datetime
    usuario_alteracao: str | None
    data_alteracao: datetime | None

    model_config = ConfigDict(from_attributes=True)