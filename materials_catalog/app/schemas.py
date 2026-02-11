from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class SupplierTier(str, Enum):
    tier_1 = "tier_1"
    tier_2 = "tier_2"

class UnitSystem(str, Enum):
    metric = "metric"
    imperial = "imperial"

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Product schemas
class ProductBase(BaseModel):
    name: str
    category: str
    attributes: Dict[str, Any]

class ProductCreate(ProductBase):
    @validator('attributes')
    def validate_attributes(cls, v):
        if 'thickness_mm' not in v or 'coverage_sqm' not in v:
            raise ValueError('Attributes must include thickness_mm and coverage_sqm')
        return v

class Product(ProductBase):
    id: int
    created_at: datetime
    thickness_mm: Optional[float] = None
    coverage_sqm: Optional[float] = None
    thickness_in: Optional[float] = None
    coverage_sqft: Optional[float] = None
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_orm_with_units(cls, obj, unit_system: UnitSystem = UnitSystem.metric):
        data = {
            "id": obj.id,
            "name": obj.name,
            "category": obj.category,
            "created_at": obj.created_at,
            "attributes": obj.attributes
        }
        
        # Extract numeric fields
        thickness_mm = obj.attributes.get('thickness_mm', 0)
        coverage_sqm = obj.attributes.get('coverage_sqm', 0)
        
        # Add both metric and imperial values
        data['thickness_mm'] = thickness_mm
        data['coverage_sqm'] = coverage_sqm
        
        if unit_system == UnitSystem.imperial:
            data['thickness_in'] = thickness_mm / 25.4
            data['coverage_sqft'] = coverage_sqm * 10.7639
        else:
            data['thickness_in'] = thickness_mm / 25.4
            data['coverage_sqft'] = coverage_sqm * 10.7639
        
        return cls(**data)

# Supplier schemas
class SupplierBase(BaseModel):
    name: str
    tier: SupplierTier
    tags: List[str] = []

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    id: int
    
    class Config:
        from_attributes = True

# Offer schemas
class OfferBase(BaseModel):
    product_id: int
    supplier_id: int
    price: float
    currency: str = "USD"

class OfferCreate(OfferBase):
    pass

class Offer(OfferBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Event schemas
class EventBase(BaseModel):
    event_type: str = "product_view"
    product_id: int
    session_id: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Analytics schemas
class TrendingProduct(BaseModel):
    product_id: int
    product_name: str
    view_count: int
    category: str
    
    class Config:
        from_attributes = True