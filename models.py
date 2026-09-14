import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from database import Base


class TipoPessoa(str, enum.Enum):
    ALUNO = "ALUNO"
    PERSONAL = "PERSONAL"


class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String(30), nullable=False, unique=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    telefone = Column(String(20), nullable=False)
    tipo_pessoa = Column(Enum(TipoPessoa), nullable=False, index=True)

    matricula_como_aluno = relationship(
        "MatriculaAluno",
        foreign_keys="MatriculaAluno.aluno_id",
        back_populates="aluno",
        uselist=False,
    )
    alunos_atendidos = relationship(
        "MatriculaAluno",
        foreign_keys="MatriculaAluno.personal_id",
        back_populates="personal",
    )


class MatriculaAluno(Base):
    __tablename__ = "matriculas_alunos"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(
        Integer,
        ForeignKey("pessoas.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    personal_id = Column(
        Integer,
        ForeignKey("pessoas.id"),
        nullable=False,
        index=True,
    )
    usuario_inclusao = Column(String(100), nullable=False)
    data_inclusao = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )
    usuario_alteracao = Column(String(100), nullable=True)
    data_alteracao = Column(DateTime, nullable=True, onupdate=func.current_timestamp())

    aluno = relationship(
        "Pessoa",
        foreign_keys=[aluno_id],
        back_populates="matricula_como_aluno",
    )
    personal = relationship(
        "Pessoa",
        foreign_keys=[personal_id],
        back_populates="alunos_atendidos",
    )
