# Materials Catalog API - Complete User Guide

## Getting Started

### First-Time Setup

1. **Download and prepare the project**
```bash
# Download the project files
git clone <repository-link>
cd materials-catalog

# Create a Python virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Or on Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Copy environment file
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux
```

2. **Set up the database**
```bash
# Create database tables
alembic upgrade head

# Or if it's your first time, use this simple command:
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Add sample data
python seed_data.py
```

3. **Start the server**
```bash
uvicorn app.main:app --reload
```
The server will start at: **http://localhost:8000**

4. **View the documentation**
- Interactive documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc

---

## Getting Access (Authentication)

### Step 1: Create Your Account

**Where to go**: In your browser, open http://localhost:8000/docs

**What to do**:
1. Look for the section that says "POST /api/register"
2. Click the "Try it out" button
3. Fill in your details:
```json
{
  "email": "your_email@example.com",
  "password": "your_password"
}
```
4. Click "Execute"

**Or use the command line**:
```bash
curl -X POST "http://localhost:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"your_email@example.com","password":"your_password"}'
```

**You'll get back**:
```json
{
  "id": 1,
  "email": "your_email@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Step 2: Log In to Get Your Access Token

**Where to go**: Same documentation page (http://localhost:8000/docs)

**What to do**:
1. Find "POST /api/login"
2. Click "Try it out"
3. Use the same email and password:
```json
{
  "email": "your_email@example.com",
  "password": "your_password"
}
```
4. Click "Execute"

**Or use command line**:
```bash
curl -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"your_email@example.com","password":"your_password"}'
```

**IMPORTANT**: Save the token you get back! It looks like this:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...long.string.here...",
  "token_type": "bearer"
}
```

### Step 3: Set Up Authorization in the Documentation

1. Click the **"Authorize"** button at the top right (looks like a lock 🔒)
2. In the box that says "Value", type:
```
Bearer YOUR_TOKEN_HERE
```
(Replace YOUR_TOKEN_HERE with the actual token you got)
3. Click "Authorize"
4. Click "Close"

Now you're ready to use all the features!

---

## Working with Products

### Browse Products

**Get all products**:
```bash
curl "http://localhost:8000/api/products"
```

**Search by category** (like "Acoustic" or "Fireproofing"):
```bash
curl "http://localhost:8000/api/products?category=Acoustic"
```

**Filter by supplier quality**:
```bash
# Get products from top-tier suppliers
curl "http://localhost:8000/api/products?supplier_tier=tier_1"

# Get products from suppliers with "high_performance" tag
curl "http://localhost:8000/api/products?supplier_tag=high_performance"
```

**Change measurement units**:
```bash
# Get measurements in inches and square feet (Imperial)
curl "http://localhost:8000/api/products?unit_system=imperial"

# Get measurements in millimeters and square meters (Metric - default)
curl "http://localhost:8000/api/products?unit_system=metric"
```

**See one specific product**:
```bash
curl "http://localhost:8000/api/products/1"
```

### Add New Products (Need Login)

To create a product, you must be logged in. Make sure you have your token ready.

**Important**: Every product must have thickness and coverage information in the attributes.

**Example**:
```bash
curl -X POST "http://localhost:8000/api/products" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Heavy Duty Insulation",
    "category": "Insulation",
    "attributes": {
      "thickness_mm": 80.0,
      "coverage_sqm": 15.0,
      "material": "Rock Wool",
      "fire_rating": "Class A"
    }
  }'
```

---

## Working with Suppliers

### Add New Suppliers (Need Login)

Suppliers can be either "tier_1" (premium) or "tier_2" (standard).

```bash
curl -X POST "http://localhost:8000/api/suppliers" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Quality Materials Inc",
    "tier": "tier_1",
    "tags": ["high_performance", "reliable", "fast_shipping"]
  }'
```

Tags help categorize suppliers. Use any tags that make sense for your business.

---

## Creating Price Offers

### Link Products with Suppliers (Need Login)

Before creating an offer, make sure:
1. The product exists (check /api/products)
2. The supplier exists

```bash
curl -X POST "http://localhost:8000/api/offers" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "supplier_id": 1,
    "price": 299.99,
    "currency": "USD"
  }'
```

You can use any currency code like USD, EUR, GBP, etc.

---

## Analytics & Tracking

### Track Product Views

Whenever someone looks at a product detail page, record it:

```bash
curl -X POST "http://localhost:8000/api/events" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "session_id": "user_456_browser_session"
  }'
```

This doesn't need login - anyone can record views.

### See What's Popular

Get trending products based on views:

```bash
# Top 5 products in last 24 hours (default)
curl "http://localhost:8000/api/insights/trending"

# Top 10 products in last 48 hours
curl "http://localhost:8000/api/insights/trending?window_hours=48&limit=10"
```

You'll see something like:
```json
[
  {
    "product_id": 1,
    "product_name": "Premium Acoustic Panel",
    "category": "Acoustic",
    "view_count": 42
  },
  {
    "product_id": 3,
    "product_name": "Fire Resistant Board",
    "category": "Fireproofing",
    "view_count": 28
  }
]
```

---

## Real Examples

### Example 1: Setting Up as a New User

```bash
# Start the server
uvicorn app.main:app --reload

# Create account
curl -X POST "http://localhost:8000/api/register" \
  -d '{"email":"mike@builder.com","password":"build123"}'

# Log in and save token (on Linux/Mac)
TOKEN=$(curl -s -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"mike@builder.com","password":"build123"}' | \
  python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "Your access token: $TOKEN"

# Browse acoustic materials
curl "http://localhost:8000/api/products?category=Acoustic"

# Add your own product
curl -X POST "http://localhost:8000/api/products" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mike\'s Sound Panels",
    "category": "Acoustic",
    "attributes": {
      "thickness_mm": 45.0,
      "coverage_sqm": 2.0,
      "material": "Eco-friendly foam"
    }
  }'
```

### Example 2: Customer Looking for Materials

```bash
# Customer wants materials in inches/feet
curl "http://localhost:8000/api/products?unit_system=imperial"

# Customer looks at product #2
curl "http://localhost:8000/api/products/2"

# Track that view
curl -X POST "http://localhost:8000/api/events" \
  -d '{"product_id": 2, "session_id": "customer_789"}'

# Check what's popular right now
curl "http://localhost:8000/api/insights/trending"
```

---

## Testing Key Features

### Test 1: Login Protection
Try to create a product without logging in:
```bash
curl -X POST "http://localhost:8000/api/products" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","category":"Test","attributes":{"thickness_mm":10,"coverage_sqm":5}}'
```
Should show: `{"detail":"Not authenticated"}`

### Test 2: Unit Conversion
```bash
# Check metric
curl "http://localhost:8000/api/products/1"

# Check imperial - should show inches and square feet
curl "http://localhost:8000/api/products/1?unit_system=imperial"
```

### Test 3: Search Filters
```bash
# Fireproof materials
curl "http://localhost:8000/api/products?category=Fireproofing"

# Top-tier suppliers only
curl "http://localhost:8000/api/products?supplier_tier=tier_1"

# Both filters together
curl "http://localhost:8000/api/products?category=Acoustic&supplier_tier=tier_1"
```

### Test 4: View Tracking
```bash
# Record some views
curl -X POST "http://localhost:8000/api/events" \
  -d '{"product_id": 1, "session_id": "test1"}'
curl -X POST "http://localhost:8000/api/events" \
  -d '{"product_id": 1, "session_id": "test2"}'
curl -X POST "http://localhost:8000/api/events" \
  -d '{"product_id": 2, "session_id": "test1"}'

# See which is more popular
curl "http://localhost:8000/api/insights/trending?window_hours=1"
# Product 1 should show 2 views, product 2 should show 1 view
```

---

## If Something Goes Wrong

### Common Problems and Solutions

1. **"Could not validate credentials"**
   - Your token expired (they last 30 minutes)
   - Fix: Log in again to get a new token

2. **"Email already registered"**
   - Someone already used that email
   - Fix: Use a different email or log in with existing one

3. **"Product not found"**
   - You're using a product ID that doesn't exist
   - Fix: First check `/api/products` to see available IDs

4. **Database issues**
   - If things seem really broken:
   ```bash
   # Remove old database
   rm materials.db
   
   # Create fresh database
   python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
   
   # Add sample data
   python seed_data.py
   
   # Restart server
   uvicorn app.main:app --reload
   ```

5. **Missing thickness or coverage**
   - When adding products, make sure attributes include:
   ```json
   "attributes": {
     "thickness_mm": 25.0,    // Must have this
     "coverage_sqm": 5.0,     // Must have this
     "other_info": "value"    // Can add anything else
   }
   ```

---

## What's Already in the System

After running `seed_data.py`, you'll have:

**Test Accounts** (password for both: "secret"):
- `admin@example.com`
- `user@example.com`

**Sample Products**:
1. Premium Acoustic Panel
2. Basic Acoustic Foam  
3. Fire Resistant Board
4. Thermal Insulation Roll
5. Soundproofing Mat
6. Firestop Sealant

**Sample Suppliers**:
- Acme Materials Corp (premium tier, high performance)
- Budget Build Supplies (standard tier, economical)

**Sample Offers**: 6 price offers connecting products and suppliers

---

## Running Tests

To make sure everything works:

```bash
# Run all tests
pytest

# Run just authentication tests
pytest tests/test_auth.py

# See detailed test output
pytest -v
```

---

## Quick Reference Commands

**Start fresh**:
```bash
# Stop server with Ctrl+C
rm materials.db
alembic upgrade head
python seed_data.py
uvicorn app.main:app --reload
```

**Check database**:
```bash
sqlite3 materials.db
.tables
SELECT * FROM products;
.exit
```

**Get help**:
1. Always check http://localhost:8000/docs first
2. Look at server logs in your terminal
3. Make sure `materials.db` file exists
4. Check you installed all packages with `pip list`

---

## Ready to Go!

Start with these steps:
1. ✅ Start the server
2. ✅ Create your account
3. ✅ Log in and save your token
4. ✅ Browse products
5. ✅ Try creating your own products
6. ✅ Test the analytics features

The system is now ready for you to manage materials, suppliers, prices, and track what customers are looking at!