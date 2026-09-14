from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

import models
import schemas
from database import get_db


router = APIRouter(prefix="/matriculas", tags=["Matrículas de alunos"])


def _buscar_matricula_ou_404(
    matricula_id: int,
    db: Session,
) -> models.MatriculaAluno:
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


def _buscar_personal_por_matricula(
    matricula_personal: str,
    db: Session,
) -> models.Pessoa:
    personal = (
        db.query(models.Pessoa)
        .filter(
            models.Pessoa.matricula == matricula_personal,
            models.Pessoa.tipo_pessoa == models.TipoPessoa.PERSONAL,
        )
        .first()
    )
    if not personal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personal não encontrado com a matrícula informada.",
        )
    return personal


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


@router.get(
    "/{matricula_id}",
    response_model=schemas.MatriculaAlunoResponseSchema,
)
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
    aluno = db.query(models.Pessoa).filter(models.Pessoa.id == dados.aluno_id).first()
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado.",
        )
    if aluno.tipo_pessoa != models.TipoPessoa.ALUNO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O ID informado não pertence a uma pessoa do tipo ALUNO.",
        )

    matricula_existente = (
        db.query(models.MatriculaAluno)
        .filter(models.MatriculaAluno.aluno_id == dados.aluno_id)
        .first()
    )
    if matricula_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este aluno já possui matrícula e personal vinculados.",
        )

    personal = _buscar_personal_por_matricula(dados.matricula_personal, db)
    nova_matricula = models.MatriculaAluno(
        aluno_id=dados.aluno_id,
        personal_id=personal.id,
        usuario_inclusao=dados.usuario_inclusao,
    )
    db.add(nova_matricula)
    db.commit()
    db.refresh(nova_matricula)
    return _buscar_matricula_ou_404(nova_matricula.id, db)


@router.put(
    "/{matricula_id}",
    response_model=schemas.MatriculaAlunoResponseSchema,
)
def alterar_matricula(
    matricula_id: int,
    dados: schemas.MatriculaAlunoUpdateSchema,
    db: Session = Depends(get_db),
):
    matricula = _buscar_matricula_ou_404(matricula_id, db)
    personal = _buscar_personal_por_matricula(dados.matricula_personal, db)

    matricula.personal_id = personal.id
    matricula.usuario_alteracao = dados.usuario_alteracao

    # O onupdate do modelo envia CURRENT_TIMESTAMP para o próprio banco.
    # Assim, a data nunca é recebida no corpo da requisição nem criada à mão.
    db.commit()
    db.refresh(matricula)
    return _buscar_matricula_ou_404(matricula.id, db)


@router.delete("/{matricula_id}")
def excluir_matricula(matricula_id: int, db: Session = Depends(get_db)):
    matricula = _buscar_matricula_ou_404(matricula_id, db)
    db.delete(matricula)
    db.commit()
    return {"mensagem": "Matrícula removida com sucesso."}
