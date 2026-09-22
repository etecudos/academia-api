from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db


router = APIRouter(prefix="/treinos", tags=["Treinos"])


def _buscar_treino_ou_404(treino_id: int, db: Session) -> models.Treino:
    treino = db.query(models.Treino).filter(models.Treino.id == treino_id).first()
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado.")
    return treino


@router.get("/", response_model=List[schemas.TreinoResponseSchema])
def listar_treinos(
    nome: str | None = None,
    objetivo: str | None = None,
    nivel: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Treino)
    if nome:
        query = query.filter(models.Treino.nome.ilike(f"%{nome}%"))
    if objetivo:
        query = query.filter(models.Treino.objetivo.ilike(f"%{objetivo}%"))
    if nivel:
        query = query.filter(models.Treino.nivel.ilike(f"%{nivel}%"))
    return query.order_by(models.Treino.id).all()


@router.get("/{treino_id}", response_model=schemas.TreinoResponseSchema)
def buscar_treino(treino_id: int, db: Session = Depends(get_db)):
    return _buscar_treino_ou_404(treino_id, db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TreinoResponseSchema)
def criar_treino(dados: schemas.TreinoCreateSchema, db: Session = Depends(get_db)):
    treino = models.Treino(**dados.model_dump())
    db.add(treino)
    db.commit()
    db.refresh(treino)
    return treino


@router.put("/{treino_id}", response_model=schemas.TreinoResponseSchema)
def atualizar_treino(
    treino_id: int,
    dados: schemas.TreinoUpdateSchema,
    db: Session = Depends(get_db),
):
    treino = _buscar_treino_ou_404(treino_id, db)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(treino, campo, valor)
    db.commit()
    db.refresh(treino)
    return treino


@router.delete("/{treino_id}")
def excluir_treino(treino_id: int, db: Session = Depends(get_db)):
    treino = _buscar_treino_ou_404(treino_id, db)
    db.delete(treino)
    db.commit()
    return {"mensagem": "Treino removido com sucesso."}
