# **Complete Setup Guide for GitHub Users**

## **For Someone Who Clones Your Repository**

### **Step 1: Clone and First-Time Setup**

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/materials-catalog.git
cd materials-catalog

# 2. Check what's in the project
dir  # Windows
ls -la  # Mac/Linux

# You should see:
# - app/ (main application code)
# - alembic/ (database migrations)
# - tests/ (test files)
# - requirements.txt (Python packages)
# - .env.example (environment template)
# - README.md (this file)
```

### **Step 2: Set Up Python Environment**

```bash
# 3. Create virtual environment
python -m venv venv

# 4. Activate it
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Your terminal should now show (venv) at the beginning
```

### **Step 3: Install Dependencies**

```bash
# 5. Install required packages
pip install -r requirements.txt

# This installs:
# - FastAPI (web framework)
# - SQLAlchemy (database)
# - Alembic (migrations)
# - JWT (authentication)
# - Pytest (testing)
```

### **Step 4: Configure Environment**

```bash
# 6. Create environment file from template
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# 7. Check the .env file (optional edit)
# The default should work:
# DATABASE_URL=sqlite:///./materials.db
# SECRET_KEY=your-secret-key-here-change-in-production
```

### **Step 5: Set Up Database**

```bash
# 8. Create database tables
# Method A: Using migrations (recommended)
alembic upgrade head

# Method B: Direct creation (if migrations fail)
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# 9. Add sample data
python seed_data.py

# You should see: "✅ Seed data created successfully!"
```

### **Step 6: Start the Server**

```bash
# 10. Run the FastAPI server
uvicorn app.main:app --reload

# You'll see output like:
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process [1234]
# INFO:     Started server process [5678]
```

### **Step 7: Verify Installation**

Open your browser and go to:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

If you see a webpage with API documentation, congratulations! 🎉 The setup is complete.

---

## **Quick Verification Test**

Open a **new terminal window** (keep server running in first terminal) and run:

```bash
# Test 1: Check if server is responding
curl http://localhost:8000/
# Should return: {"message":"Materials Catalog API"}

# Test 2: Check sample products (should work without login)
curl http://localhost:8000/api/products

# Test 3: Try unit conversion
curl "http://localhost:8000/api/products?unit_system=imperial"

# Test 4: Check trending products
curl http://localhost:8000/api/insights/trending
```

---

## **Ready-to-Use Credentials**

After running `seed_data.py`, you can immediately use these accounts:

### **Pre-loaded Users:**
| Email | Password | Role |
|-------|----------|------|
| `admin@example.com` | `secret` | Administrator |
| `user@example.com` | `secret` | Regular User |

### **How to Login with Pre-loaded User:**

**Using Swagger UI:**
1. Go to http://localhost:8000/docs
2. Find `POST /api/login`
3. Click "Try it out"
4. Enter:
```json
{
  "email": "admin@example.com",
  "password": "secret"
}
```
5. Click "Execute"
6. Copy the `access_token`

**Using curl:**
```bash
curl -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"secret"}'
```

Save the token you get back!

---

## **Immediate Testing Script**

Here's a complete test script to verify everything works:

```bash
# Save this as test_api.sh (Mac/Linux) or test_api.bat (Windows)

echo "=== Testing Materials Catalog API ==="
echo ""

# 1. Test basic endpoint
echo "1. Testing root endpoint..."
curl -s http://localhost:8000/ | grep -q "Materials Catalog API" && echo "✅ Root endpoint OK" || echo "❌ Root endpoint failed"

echo ""
echo "2. Getting all products..."
curl -s "http://localhost:8000/api/products" | python -c "import sys,json; data=json.load(sys.stdin); print(f'Found {len(data)} products')"

echo ""
echo "3. Testing unit conversion..."
curl -s "http://localhost:8000/api/products?unit_system=imperial" | python -c "
import sys,json
data=json.load(sys.stdin)
if data:
    p = data[0]
    if 'thickness_in' in p and 'coverage_sqft' in p:
        print('✅ Unit conversion working')
        print(f'   Sample: {p[\"thickness_mm\"]}mm = {p[\"thickness_in\"]:.2f} inches')
    else:
        print('❌ Unit conversion missing')
"

echo ""
echo "4. Testing analytics..."
curl -s -X POST "http://localhost:8000/api/events" \
  -H "Content-Type: application/json" \
  -d '{"product_id":1,"session_id":"test_user"}'
echo "✅ Recorded test view"

echo ""
echo "5. Getting trending products..."
curl -s "http://localhost:8000/api/insights/trending?window_hours=1"
echo ""

echo ""
echo "=== Testing Complete ==="
```

---

## **Common Issues & Fixes**

### **Issue 1: "Module not found" errors**
```bash
# Make sure you activated virtual environment
# Windows: Check for (venv) in prompt
# If not activated:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall packages
pip install -r requirements.txt
```

### **Issue 2: Database errors**
```bash
# Delete and recreate database
rm materials.db  # or del materials.db on Windows
alembic upgrade head
python seed_data.py
```

### **Issue 3: Port 8000 already in use**
```bash
# Change port
uvicorn app.main:app --reload --port 8001
# Then access: http://localhost:8001/docs
```

### **Issue 4: Alembic migration errors**
```bash
# Skip alembic and create directly
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
python seed_data.py
```

---

## **Development Workflow**

### **If you want to modify the code:**

1. Make your changes in the `app/` directory
2. Test locally:
```bash
# Restart server (auto-restarts with --reload flag)
# If changes don't reflect, stop and restart:
uvicorn app.main:app --reload
```

3. Run tests:
```bash
pytest
```

4. Create database migration (if you changed models.py):
```bash
# Generate migration
alembic revision --autogenerate -m "Description of changes"

# Apply migration
alembic upgrade head
```

---

## **Project Structure Explained**

```
materials-catalog/
├── app/                    # Main application
│   ├── main.py            # FastAPI app setup
│   ├── database.py        # Database connection
│   ├── models.py          # Database tables (Users, Products, etc.)
│   ├── schemas.py         # Data validation shapes
│   ├── auth.py            # Login/authentication
│   └── routers/           # API endpoints
│       ├── auth.py        # /api/register, /api/login
│       ├── products.py    # /api/products
│       ├── suppliers.py   # /api/suppliers
│       ├── offers.py      # /api/offers
│       └── analytics.py   # /api/events, /api/insights
├── alembic/               # Database migrations
│   ├── versions/          # Migration files
│   └── alembic.ini        # Alembic config
├── tests/                 # Test files
│   ├── test_auth.py       # Authentication tests
│   ├── test_products.py   # Product API tests
│   └── test_analytics.py  # Analytics tests
├── seed_data.py           # Sample data loader
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

---

## **Quick Start Cheat Sheet**

```bash
# ONE-LINER for quick start (after cloning):

# Windows:
git clone https://github.com/yourusername/materials-catalog.git && cd materials-catalog && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && copy .env.example .env && python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)" && python seed_data.py && uvicorn app.main:app --reload

# Mac/Linux:
git clone https://github.com/yourusername/materials-catalog.git && cd materials-catalog && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && cp .env.example .env && python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)" && python seed_data.py && uvicorn app.main:app --reload
```

---

## **Ready-to-Use API Examples**

Copy and paste these in your terminal:

### **1. Complete Registration to Product Creation**
```bash
# Register new user
curl -X POST "http://localhost:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'

# Login and save token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}' | \
  python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "Token: $TOKEN"

# Create a product
curl -X POST "http://localhost:8000/api/products" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Material",
    "category": "Testing",
    "attributes": {
      "thickness_mm": 25.0,
      "coverage_sqm": 5.0,
      "notes": "Test product"
    }
  }'
```

### **2. Complete Analytics Demo**
```bash
# Record multiple views
for i in {1..5}; do
  curl -X POST "http://localhost:8000/api/events" \
    -H "Content-Type: application/json" \
    -d "{\"product_id\":1,\"session_id\":\"demo_user_$i\"}"
  echo "Recorded view $i"
done

# Check trending
curl "http://localhost:8000/api/insights/trending?window_hours=1&limit=3"
```

---

## **Need Help?**

If the setup doesn't work:

1. **Check Python version** (need 3.8+):
```bash
python --version
```

2. **Check virtual environment**:
```bash
# Should show (venv) in terminal prompt
echo $VIRTUAL_ENV  # Mac/Linux
echo %VIRTUAL_ENV%  # Windows
```

3. **Check installed packages**:
```bash
pip list | grep -E "fastapi|sqlalchemy|alembic"
```

4. **Check database file exists**:
```bash
ls -la materials.db  # Should show file
```

5. **Check server logs** for errors in the terminal where uvicorn is running

---

## **You're All Set! 🎯**

**Now you can:**
1. **Browse** the API at http://localhost:8000/docs
2. **Test** with pre-loaded users (admin@example.com / secret)
3. **Create** your own products/suppliers
4. **Track** analytics
5. **Run** the test suite

**Next steps:**
- Explore all endpoints in Swagger UI
- Try the curl commands above
- Check out the test files to understand expected behavior
- Modify the code for your needs!

**Remember:** The server must stay running (don't close that terminal) while using the API.