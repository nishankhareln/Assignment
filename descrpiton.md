# Materials Catalog API - What It Is & What It Does

## In Simple Terms (Non-Technical)

### What is this?
**A digital catalog system for construction/building materials** - like an online inventory system for companies that sell things like insulation, fireproofing materials, acoustic panels, etc.

### Who would use it?
- **Material suppliers** to list their products
- **Builders/contractors** to find materials they need
- **Project managers** to compare prices from different suppliers
- **Business owners** to see what materials are popular

### What can you do with it?

1. **Browse materials** - Search through different types of building materials
2. **Compare suppliers** - See which suppliers are premium (tier 1) or standard (tier 2)
3. **Check prices** - View different price offers for the same material
4. **Track popularity** - See which materials people are looking at most
5. **Manage inventory** - Add new materials, suppliers, and prices (if you're logged in)

### Real-life example:
Imagine you're building a house and need soundproofing materials. You could:
- Search for "acoustic" materials
- See only materials from top-quality suppliers
- Compare prices from different companies
- Check which soundproofing materials are most popular right now

---

## Technical Explanation (For Developers)

### Project Overview
A FastAPI-based RESTful API for a B2B materials catalog system with:
- Product management with JSON attributes
- Supplier tier system (tier_1/tier_2)
- Real-time analytics tracking
- JWT authentication
- Unit conversion (metric/imperial)

### Core Components

#### 1. **Authentication System**
- User registration/login
- JWT token-based security
- Protected endpoints for admin operations
- Token expiration (30 minutes)

#### 2. **Product Catalog**
```python
# Product structure
{
  "name": "Acoustic Panel",
  "category": "Acoustic",
  "attributes": {  # Flexible JSON fields
    "thickness_mm": 50.0,      # Required
    "coverage_sqm": 1.2,       # Required
    "material": "Polyester",   # Optional
    "color": "White"           # Optional
  }
}
```

#### 3. **Supplier Management**
- Tier-based classification (tier_1 = premium, tier_2 = standard)
- Tag system for categorization (e.g., "high_performance")
- Many-to-many relationships with products via Offers

#### 4. **Pricing System**
- Multiple suppliers can offer the same product
- Different prices per supplier
- Currency support (USD, EUR, GBP, etc.)

#### 5. **Analytics Engine**
- Event tracking for product views
- Real-time trending analysis
- Time-window based insights (last 24 hours, 48 hours, etc.)

#### 6. **Unit Conversion**
- Automatic metric ↔ imperial conversion
- Supports both systems simultaneously
- Mathematical conversions:
  - mm → inches: divide by 25.4
  - sqm → sqft: multiply by 10.7639

### Data Flow

```
User Action → API Request → Database Operation → Response
     ↓           ↓               ↓                ↓
Browse products → GET /products → Query database → Return filtered list
View product → POST /events → Record view → Track for analytics
Add product → POST /products → Create record → Return confirmation
```

### Database Schema
```
Users
├── email (unique)
└── password (hashed)

Products
├── name
├── category
└── attributes (JSON with thickness_mm, coverage_sqm)

Suppliers
├── name
├── tier (tier_1/tier_2)
└── tags (array)

Offers (connects Products & Suppliers)
├── product_id
├── supplier_id
├── price
└── currency

Events (analytics)
├── product_id
├── session_id
└── timestamp
```

---

## Key Features Explained

### 1. **Smart Filtering**
```python
# You can filter by:
- Category: "Show me only acoustic materials"
- Supplier quality: "Only from premium suppliers"
- Supplier tags: "Only from high-performance suppliers"
- Multiple filters: "Acoustic materials from premium, high-performance suppliers"
```

### 2. **Flexible Product Attributes**
Unlike rigid database structures, each product can have different attributes:
- Acoustic panels might have "noise_reduction_rating"
- Fireproofing might have "fire_rating"
- Insulation might have "r_value"

All stored in JSON, so you don't need database changes for new attributes.

### 3. **Real Analytics**
- Every product view is tracked
- Anonymous session tracking (no personal data)
- Real-time trending calculation
- Configurable time windows (last hour, day, week)

### 4. **Automatic Unit Conversion**
```python
# Request: GET /products?unit_system=imperial
# Response includes both:
{
  "thickness_mm": 50.0,     # Original metric
  "thickness_in": 1.9685,   # Converted imperial
  "coverage_sqm": 1.2,
  "coverage_sqft": 12.9167
}
```

### 5. **Security Model**
- Public: Anyone can browse products
- Protected: Only logged-in users can add/modify data
- Token-based: Secure API access
- Password hashing: No plain-text passwords stored

---

## How Different Users Interact

### **Supplier Company Admin**
```
Actions:
1. Register company account
2. Add their products to catalog
3. Set up their supplier profile
4. Create price offers for their products
5. Monitor which of their products are trending

Permissions:
- Can create products
- Can create their supplier entry
- Can create offers
- Cannot modify other suppliers' data
```

### **Building Contractor**
```
Actions:
1. Browse materials by category
2. Filter by supplier quality
3. Compare prices from different suppliers
4. Save interesting products
5. See what's popular in the market

Permissions:
- Read-only access
- Can view all products/suppliers
- Cannot modify data
```

### **System Administrator**
```
Actions:
1. Monitor overall system usage
2. View trending analytics
3. Manage user accounts
4. Ensure data quality

Permissions:
- Full access to all features
- Can view analytics dashboard
- Can manage all data
```

---

## Business Value

### For Material Suppliers
- **Digital catalog** - Move from paper/Excel to API
- **Market insights** - See what customers are looking for
- **Competitive analysis** - Compare with other suppliers
- **Lead generation** - Get visibility with contractors

### For Contractors/Builders
- **Centralized search** - One place for all materials
- **Quality filtering** - Find premium suppliers easily
- **Price comparison** - Get best deals
- **Trend awareness** - Know what's popular in market

### For Project Managers
- **Standardized data** - Consistent product information
- **Budget planning** - Accurate price comparisons
- **Supplier evaluation** - Tier system helps choose partners
- **Documentation** - All decisions tracked in system

---

## Technical Architecture

### Backend Stack
- **Python 3.8+** - Main programming language
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Simple file-based database (can switch to PostgreSQL)
- **JWT** - Secure authentication
- **Pydantic** - Data validation

### Project Structure
```
app/
├── main.py           # Application entry point
├── database.py       # Database connection
├── models.py         # Database models (Users, Products, etc.)
├── schemas.py        # Request/response data shapes
├── auth.py           # Authentication logic
└── routers/          # API endpoints
    ├── auth.py       # Login/register
    ├── products.py   # Product operations
    ├── suppliers.py  # Supplier operations
    ├── offers.py     # Price offers
    └── analytics.py  # Events and insights
```

### API Design Principles
1. **RESTful** - Standard HTTP methods (GET, POST, etc.)
2. **Consistent** - Uniform response formats
3. **Documented** - Auto-generated OpenAPI docs
4. **Secure** - Proper authentication/authorization
5. **Scalable** - Ready for more users/products

---

## Example Use Cases

### Case 1: New Material Launch
```
Scenario: A supplier launches new eco-friendly insulation
Steps:
1. Supplier logs into system
2. Creates new product: "Eco Insulation 3000"
3. Sets attributes: thickness, coverage, material, eco-certifications
4. Creates price offer for this product
5. Contractors discover it while browsing
6. Analytics show it's getting views
7. Supplier sees interest and can adjust marketing
```

### Case 2: Large Construction Project
```
Scenario: Hospital construction needs specific materials
Steps:
1. Project manager searches "fireproofing" materials
2. Filters to "tier_1" suppliers only (hospital requires premium)
3. Compares prices from 3 different suppliers
4. Checks which fireproofing materials are most used recently
5. Makes purchasing decision based on data
6. Tracks views for reporting/auditing
```

### Case 3: Supplier Performance Review
```
Scenario: Company evaluates which suppliers to keep
Steps:
1. Check supplier tiers (who are our premium partners?)
2. Review product offerings from each supplier
3. Analyze which suppliers' products get most views
4. Compare pricing competitiveness
5. Make data-driven decisions on partnerships
```

---

## What Makes This Special

### 1. **Flexible Yet Structured**
- JSON attributes allow customization
- But required fields (thickness, coverage) ensure consistency
- Best of both worlds: flexible but not chaotic

### 2. **Real Business Insights**
- Not just a catalog, but intelligence system
- Know what's trending before competitors
- Make decisions based on actual user behavior

### 3. **Global Ready**
- Built-in unit conversion
- Multi-currency support
- Timezone-aware analytics

### 4. **Easy to Extend**
- Add new product categories without code changes
- New supplier tags with simple configuration
- More analytics endpoints as needed

### 5. **Production Quality**
- Proper error handling
- Input validation
- Security best practices
- Comprehensive testing

---

## In Summary

This is **not just another CRUD app**. It's a **complete business solution** for the building materials industry that:

✅ **Digitizes** physical catalogs into searchable APIs  
✅ **Connects** suppliers with potential customers  
✅ **Provides** real market intelligence through analytics  
✅ **Simplifies** complex comparisons (quality, price, units)  
✅ **Scales** from small business to enterprise use  

Whether you're a developer integrating this into a larger system, a business owner managing materials inventory, or a contractor finding the right products for a job - this system provides the tools and data needed to make better decisions faster.