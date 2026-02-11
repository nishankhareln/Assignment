import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models

# Create tables
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    try:
        # Create users
        users = [
            models.User(
                email="admin@example.com",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # password = "secret"
            ),
            models.User(
                email="user@example.com",
                hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
            )
        ]
        db.add_all(users)
        db.flush()
        
        # Create products
        products = [
            models.Product(
                name="Premium Acoustic Panel",
                category="Acoustic",
                attributes={
                    "thickness_mm": 50.0,
                    "coverage_sqm": 1.2,
                    "material": "Polyester",
                    "color": "White"
                }
            ),
            models.Product(
                name="Basic Acoustic Foam",
                category="Acoustic",
                attributes={
                    "thickness_mm": 30.0,
                    "coverage_sqm": 0.6,
                    "material": "Polyurethane",
                    "color": "Black"
                }
            ),
            models.Product(
                name="Fire Resistant Board",
                category="Fireproofing",
                attributes={
                    "thickness_mm": 12.5,
                    "coverage_sqm": 2.4,
                    "material": "Calcium Silicate",
                    "fire_rating": "A1"
                }
            ),
            models.Product(
                name="Thermal Insulation Roll",
                category="Insulation",
                attributes={
                    "thickness_mm": 100.0,
                    "coverage_sqm": 10.0,
                    "material": "Glass Wool",
                    "r_value": 3.5
                }
            ),
            models.Product(
                name="Soundproofing Mat",
                category="Acoustic",
                attributes={
                    "thickness_mm": 25.0,
                    "coverage_sqm": 5.0,
                    "material": "Rubber",
                    "weight_kg": 15.0
                }
            ),
            models.Product(
                name="Firestop Sealant",
                category="Fireproofing",
                attributes={
                    "thickness_mm": 10.0,
                    "coverage_sqm": 0.1,
                    "material": "Intumescent",
                    "tube_size": "300ml"
                }
            )
        ]
        db.add_all(products)
        db.flush()
        
        # Create suppliers
        suppliers = [
            models.Supplier(
                name="Acme Materials Corp",
                tier="tier_1",
                tags=["high_performance", "reliable"]
            ),
            models.Supplier(
                name="Budget Build Supplies",
                tier="tier_2",
                tags=["economical"]
            )
        ]
        db.add_all(suppliers)
        db.flush()
        
        # Create offers
        offers = []
        for i in range(6):
            product_id = products[i % len(products)].id
            supplier_id = suppliers[0 if i % 2 == 0 else 1].id
            offers.append(
                models.Offer(
                    product_id=product_id,
                    supplier_id=supplier_id,
                    price=100.0 + (i * 20),
                    currency="USD"
                )
            )
        
        db.add_all(offers)
        
        # Create some events for analytics
        events = []
        import random
        from datetime import datetime, timedelta
        
        for i in range(20):
            events.append(
                models.Event(
                    product_id=random.choice([p.id for p in products]),
                    session_id=f"session_{random.randint(1, 5)}",
                    timestamp=datetime.utcnow() - timedelta(hours=random.randint(0, 48))
                )
            )
        
        db.add_all(events)
        
        db.commit()
        print("✅ Seed data created successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()