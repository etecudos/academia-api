from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/alunos", tags=["Alunos"])

@router.get("/", response_model=List[schemas.AlunoResponseSchema])
def listar_alunos(nome: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Aluno)
    if nome: # Mantendo sua lógica de busca por nome (agora no banco)
        query = query.filter(models.Aluno.nome.ilike(f"%{nome}%"))
    return query.all()

@router.get("/{id}", response_model=schemas.AlunoResponseSchema)
def buscar_aluno(id: int, db: Session = Depends(get_db)):
    aluno = db.query(models.Aluno).filter(models.Aluno.id == id).first()
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado."
        )
    return aluno

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AlunoResponseSchema)
def cadastrar_aluno(aluno: schemas.AlunoCreateSchema, db: Session = Depends(get_db)):
    novo_aluno = models.Aluno(**aluno.model_dump())
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return novo_aluno

@router.delete("/{id}")
def excluir_aluno(id: int, db: Session = Depends(get_db)):
    aluno = db.query(models.Aluno).filter(models.Aluno.id == id).first()
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado."
        )
    db.delete(aluno)
    db.commit()
    return {"mensagem": "Aluno removido com sucesso."}