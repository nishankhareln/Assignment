from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Association table for supplier tags
supplier_tags = Table(
    'supplier_tags',
    Base.metadata,
    Column('supplier_id', Integer, ForeignKey('suppliers.id')),
    Column('tag', String)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    attributes = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    offers = relationship("Offer", back_populates="product")
    events = relationship("Event", back_populates="product")

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tier = Column(String, nullable=False)  # tier_1 or tier_2
    
    # Tags as array (SQLite doesn't support native arrays, so we use JSON or association table)
    # We'll use JSON for simplicity with SQLite
    tags = Column(JSON, default=list)
    
    # Relationships
    offers = relationship("Offer", back_populates="supplier")

class Offer(Base):
    __tablename__ = "offers"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="offers")
    supplier = relationship("Supplier", back_populates="offers")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False, default="product_view")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    session_id = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="events")