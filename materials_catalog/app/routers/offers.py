from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter()

@router.post("/offers", response_model=schemas.Offer, dependencies=[Depends(auth.get_current_user)])
def create_offer(offer: schemas.OfferCreate, db: Session = Depends(get_db)):
    # Check if product exists
    product = db.query(models.Product).filter(models.Product.id == offer.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if supplier exists
    supplier = db.query(models.Supplier).filter(models.Supplier.id == offer.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    db_offer = models.Offer(
        product_id=offer.product_id,
        supplier_id=offer.supplier_id,
        price=offer.price,
        currency=offer.currency
    )
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer