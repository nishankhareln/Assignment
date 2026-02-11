from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter()

@router.get("/products", response_model=List[schemas.Product])
def get_products(
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    supplier_tier: Optional[str] = None,
    supplier_tag: Optional[str] = None,
    unit_system: schemas.UnitSystem = schemas.UnitSystem.metric,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(models.Product)
    
    # Apply filters
    if category:
        query = query.filter(models.Product.category == category)
    
    if supplier_tier or supplier_tag:
        query = query.join(models.Offer).join(models.Supplier)
        
        if supplier_tier:
            query = query.filter(models.Supplier.tier == supplier_tier)
        
        if supplier_tag:
            query = query.filter(models.Supplier.tags.contains([supplier_tag]))
    
    # Execute query and convert to response format
    products = query.offset(skip).limit(limit).all()
    return [schemas.Product.from_orm_with_units(p, unit_system) for p in products]

@router.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.Product.from_orm_with_units(product)

@router.post("/products", response_model=schemas.Product, dependencies=[Depends(auth.get_current_user)])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(
        name=product.name,
        category=product.category,
        attributes=product.attributes
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return schemas.Product.from_orm_with_units(db_product)