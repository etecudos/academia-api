from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

import models
import schemas
from database import get_db


router = APIRouter(prefix="/fichas-treino", tags=["Fichas de treino"])


def _buscar_ficha_ou_404(ficha_id: int, db: Session) -> models.FichaTreino:
    ficha = (
        db.query(models.FichaTreino)
        .options(
            joinedload(models.FichaTreino.aluno),
            joinedload(models.FichaTreino.personal),
            joinedload(models.FichaTreino.treino),
        )
        .filter(models.FichaTreino.id == ficha_id)
        .first()
    )
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha de treino não encontrada.")
    return ficha


def _validar_pessoa(matricula: int, tipo_id: int, descricao: str, db: Session) -> None:
    existe = (
        db.query(models.Pessoa)
        .filter(models.Pessoa.matricula == matricula, models.Pessoa.tipo_pessoa_id == tipo_id)
        .first()
    )
    if not existe:
        raise HTTPException(status_code=404, detail=f"{descricao} não encontrado.")


def _validar_treino(treino_id: int, db: Session) -> None:
    treino = db.query(models.Treino).filter(models.Treino.id == treino_id).first()
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado.")


@router.get("/", response_model=List[schemas.FichaTreinoResponseSchema])
def listar_fichas(
    aluno_matricula: int | None = None,
    personal_matricula: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.FichaTreino).options(
        joinedload(models.FichaTreino.aluno),
        joinedload(models.FichaTreino.personal),
        joinedload(models.FichaTreino.treino),
    )
    if aluno_matricula:
        query = query.filter(models.FichaTreino.aluno_matricula == aluno_matricula)
    if personal_matricula:
        query = query.filter(models.FichaTreino.personal_matricula == personal_matricula)
    return query.order_by(models.FichaTreino.id).all()


@router.get("/{ficha_id}", response_model=schemas.FichaTreinoResponseSchema)
def buscar_ficha(ficha_id: int, db: Session = Depends(get_db)):
    return _buscar_ficha_ou_404(ficha_id, db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.FichaTreinoResponseSchema)
def criar_ficha(dados: schemas.FichaTreinoCreateSchema, db: Session = Depends(get_db)):
    _validar_pessoa(dados.aluno_matricula, 1, "Aluno", db)
    _validar_pessoa(dados.personal_matricula, 2, "Personal", db)
    _validar_treino(dados.treino_id, db)

    ficha = models.FichaTreino(**dados.model_dump())
    db.add(ficha)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Este treino já está vinculado à ficha do aluno.")
    db.refresh(ficha)
    return _buscar_ficha_ou_404(ficha.id, db)


@router.put("/{ficha_id}", response_model=schemas.FichaTreinoResponseSchema)
def atualizar_ficha(
    ficha_id: int,
    dados: schemas.FichaTreinoUpdateSchema,
    db: Session = Depends(get_db),
):
    ficha = _buscar_ficha_ou_404(ficha_id, db)
    alteracoes = dados.model_dump(exclude_unset=True)

    if "personal_matricula" in alteracoes:
        _validar_pessoa(alteracoes["personal_matricula"], 2, "Personal", db)
    if "treino_id" in alteracoes:
        _validar_treino(alteracoes["treino_id"], db)

    for campo, valor in alteracoes.items():
        setattr(ficha, campo, valor)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Este treino já está vinculado à ficha do aluno.")
    db.refresh(ficha)
    return _buscar_ficha_ou_404(ficha.id, db)


@router.delete("/{ficha_id}")
def excluir_ficha(ficha_id: int, db: Session = Depends(get_db)):
    ficha = _buscar_ficha_ou_404(ficha_id, db)
    db.delete(ficha)
    db.commit()
    return {"mensagem": "Ficha de treino removida com sucesso."}
