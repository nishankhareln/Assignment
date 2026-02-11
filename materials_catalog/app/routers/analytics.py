from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter()

@router.post("/events")
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    # Check if product exists
    product = db.query(models.Product).filter(models.Product.id == event.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_event = models.Event(
        event_type=event.event_type,
        product_id=event.product_id,
        session_id=event.session_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return {"message": "Event recorded successfully"}

@router.get("/insights/trending", response_model=List[schemas.TrendingProduct])
def get_trending_products(
    db: Session = Depends(get_db),
    window_hours: int = Query(24, ge=1),
    limit: int = Query(5, ge=1, le=100)
):
    # Calculate time window
    time_threshold = datetime.utcnow() - timedelta(hours=window_hours)
    
    # Query trending products
    trending = (
        db.query(
            models.Event.product_id,
            models.Product.name,
            models.Product.category,
            func.count(models.Event.id).label('view_count')
        )
        .join(models.Product, models.Event.product_id == models.Product.id)
        .filter(models.Event.timestamp >= time_threshold)
        .group_by(models.Event.product_id, models.Product.name, models.Product.category)
        .order_by(desc('view_count'))
        .limit(limit)
        .all()
    )
    
    return [
        schemas.TrendingProduct(
            product_id=row.product_id,
            product_name=row.name,
            category=row.category,
            view_count=row.view_count
        )
        for row in trending
    ]