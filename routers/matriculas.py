from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

import models
import schemas
from database import get_db


router = APIRouter(prefix="/matriculas", tags=["Matrículas de alunos"])


def _buscar_matricula_ou_404(matricula_id: int, db: Session) -> models.MatriculaAluno:
    matricula = (
        db.query(models.MatriculaAluno)
        .options(
            joinedload(models.MatriculaAluno.aluno),
            joinedload(models.MatriculaAluno.personal),
        )
        .filter(models.MatriculaAluno.id == matricula_id)
        .first()
    )
    if not matricula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matrícula do aluno não encontrada.",
        )
    return matricula


def _buscar_pessoa_por_matricula_e_tipo(
    matricula: int,
    tipo_pessoa_id: int,
    descricao: str,
    db: Session,
) -> models.Pessoa:
    pessoa = (
        db.query(models.Pessoa)
        .filter(
            models.Pessoa.matricula == matricula,
            models.Pessoa.tipo_pessoa_id == tipo_pessoa_id,
        )
        .first()
    )
    if not pessoa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{descricao} não encontrado com a matrícula informada.",
        )
    return pessoa


@router.get("/", response_model=List[schemas.MatriculaAlunoResponseSchema])
def listar_matriculas(db: Session = Depends(get_db)):
    return (
        db.query(models.MatriculaAluno)
        .options(
            joinedload(models.MatriculaAluno.aluno),
            joinedload(models.MatriculaAluno.personal),
        )
        .order_by(models.MatriculaAluno.id)
        .all()
    )


@router.get("/{matricula_id}", response_model=schemas.MatriculaAlunoResponseSchema)
def buscar_matricula(matricula_id: int, db: Session = Depends(get_db)):
    return _buscar_matricula_ou_404(matricula_id, db)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.MatriculaAlunoResponseSchema,
)
def criar_matricula(
    dados: schemas.MatriculaAlunoCreateSchema,
    db: Session = Depends(get_db),
):
    _buscar_pessoa_por_matricula_e_tipo(dados.aluno_matricula, 1, "Aluno", db)
    _buscar_pessoa_por_matricula_e_tipo(dados.personal_matricula, 2, "Personal", db)

    matricula_existente = (
        db.query(models.MatriculaAluno)
        .filter(models.MatriculaAluno.aluno_matricula == dados.aluno_matricula)
        .first()
    )
    if matricula_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este aluno já possui um personal vinculado.",
        )

    nova_matricula = models.MatriculaAluno(**dados.model_dump())
    db.add(nova_matricula)
    db.commit()
    db.refresh(nova_matricula)
    return _buscar_matricula_ou_404(nova_matricula.id, db)


@router.put("/{matricula_id}", response_model=schemas.MatriculaAlunoResponseSchema)
def alterar_matricula(
    matricula_id: int,
    dados: schemas.MatriculaAlunoUpdateSchema,
    db: Session = Depends(get_db),
):
    matricula = _buscar_matricula_ou_404(matricula_id, db)
    _buscar_pessoa_por_matricula_e_tipo(dados.personal_matricula, 2, "Personal", db)

    matricula.personal_matricula = dados.personal_matricula
    matricula.usuario_alteracao = dados.usuario_alteracao
    db.commit()
    db.refresh(matricula)
    return _buscar_matricula_ou_404(matricula.id, db)


@router.delete("/{matricula_id}")
def excluir_matricula(matricula_id: int, db: Session = Depends(get_db)):
    matricula = _buscar_matricula_ou_404(matricula_id, db)
    db.delete(matricula)
    db.commit()
    return {"mensagem": "Matrícula removida com sucesso."}
