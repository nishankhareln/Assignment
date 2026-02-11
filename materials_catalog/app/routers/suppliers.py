from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter()

@router.post("/suppliers", response_model=schemas.Supplier, dependencies=[Depends(auth.get_current_user)])
def create_supplier(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    db_supplier = models.Supplier(
        name=supplier.name,
        tier=supplier.tier,
        tags=supplier.tags
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier