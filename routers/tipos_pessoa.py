from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db


router = APIRouter(prefix="/tipos-pessoa", tags=["Tipos de pessoa"])


@router.get("/", response_model=List[schemas.TipoPessoaResponseSchema])
def listar_tipos_pessoa(db: Session = Depends(get_db)):
    return db.query(models.TipoPessoa).order_by(models.TipoPessoa.id).all()
