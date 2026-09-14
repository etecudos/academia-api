from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db


router = APIRouter(prefix="/pessoas", tags=["Pessoas"])


def _buscar_pessoa_ou_404(pessoa_id: int, db: Session) -> models.Pessoa:
    pessoa = db.query(models.Pessoa).filter(models.Pessoa.id == pessoa_id).first()
    if not pessoa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pessoa não encontrada.",
        )
    return pessoa


def _salvar_ou_409(db: Session, mensagem: str) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=mensagem,
        )


@router.get("/", response_model=List[schemas.PessoaResponseSchema])
def listar_pessoas(
    nome: str | None = None,
    tipo_pessoa: schemas.TipoPessoa | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Pessoa)
    if nome:
        query = query.filter(models.Pessoa.nome.ilike(f"%{nome}%"))
    if tipo_pessoa:
        query = query.filter(models.Pessoa.tipo_pessoa == tipo_pessoa.value)
    return query.order_by(models.Pessoa.id).all()


@router.get("/{pessoa_id}", response_model=schemas.PessoaResponseSchema)
def buscar_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    return _buscar_pessoa_ou_404(pessoa_id, db)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PessoaResponseSchema,
)
def cadastrar_pessoa(
    pessoa: schemas.PessoaCreateSchema,
    db: Session = Depends(get_db),
):
    nova_pessoa = models.Pessoa(**pessoa.model_dump(mode="json"))
    db.add(nova_pessoa)
    _salvar_ou_409(db, "Matrícula ou e-mail já cadastrado.")
    db.refresh(nova_pessoa)
    return nova_pessoa


@router.put("/{pessoa_id}", response_model=schemas.PessoaResponseSchema)
def atualizar_pessoa(
    pessoa_id: int,
    dados: schemas.PessoaUpdateSchema,
    db: Session = Depends(get_db),
):
    pessoa = _buscar_pessoa_ou_404(pessoa_id, db)
    alteracoes = dados.model_dump(exclude_unset=True, mode="json")

    for campo, valor in alteracoes.items():
        setattr(pessoa, campo, valor)

    _salvar_ou_409(db, "Matrícula ou e-mail já cadastrado.")
    db.refresh(pessoa)
    return pessoa


@router.delete("/{pessoa_id}")
def excluir_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    pessoa = _buscar_pessoa_ou_404(pessoa_id, db)

    possui_vinculo = (
        db.query(models.MatriculaAluno)
        .filter(
            (models.MatriculaAluno.aluno_id == pessoa_id)
            | (models.MatriculaAluno.personal_id == pessoa_id)
        )
        .first()
    )
    if possui_vinculo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A pessoa possui uma matrícula vinculada e não pode ser removida.",
        )

    db.delete(pessoa)
    db.commit()
    return {"mensagem": "Pessoa removida com sucesso."}
