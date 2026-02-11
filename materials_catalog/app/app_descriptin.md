# APP FOLDER - Complete Description

##  **D:\Assignment\materials_catalog\app\**

This is the **heart of the application** - all backend code lives here. Each file has a specific purpose. Here's a complete breakdown:

---

## **1. main.py - The Application Entry Point**

**What it does:** 
This is the **main file** that creates and configures the FastAPI application. It's like the "control center" that brings everything together.

**Purpose:**
- Creates the FastAPI app instance
- Sets up CORS (security settings for browser access)
- Connects all the routers to make endpoints available
- Creates database tables on startup
- Defines the root endpoint ("/")

**Without this file:** The entire API wouldn't exist. It's the glue that holds everything together.

---

##  **2. database.py - Database Connection Manager**

**What it does:**
Manages everything related to the database connection. It's the **bridge between your Python code and the SQLite database file**.

**Purpose:**
- Creates the database engine (the connection)
- Defines the Base class (all models inherit from this)
- Creates SessionLocal (used to talk to the database)
- Provides get_db() function (dependency for database sessions)

**Why it's important:** Without this, you can't save or retrieve any data. It's like the power cable for your database.

---

##  **3. models.py - Database Table Definitions**

**What it does:**
Defines the **structure of your database tables** using Python classes. Each class becomes a table in the database.

**Purpose:**

**User Model:**
- Stores user accounts
- Fields: id, email, hashed_password, created_at

**Product Model:**
- Stores material/product information
- Fields: id, name, category, attributes (JSON), created_at
- Relationships: has many offers, has many events

**Supplier Model:**
- Stores supplier company information
- Fields: id, name, tier (tier_1/tier_2), tags (JSON)
- Relationships: has many offers

**Offer Model:**
- Connects products with suppliers and their prices
- Fields: id, product_id, supplier_id, price, currency, created_at
- Relationships: belongs to product, belongs to supplier

**Event Model:**
- Tracks product views for analytics
- Fields: id, event_type, product_id, session_id, timestamp
- Relationships: belongs to product

**Why it's important:** This defines WHAT data you can store and HOW it's organized. Without models, you have no structure.

---

##  **4. schemas.py - Data Validation Rules**

**What it does:**
Defines the **shape and validation rules** for data coming into and going out of your API. Uses Pydantic for validation.

**Purpose:**

**User Schemas:**
- UserBase: email field
- UserCreate: email + password (for registration)
- User: what gets returned (id, email, created_at)
- Token: JWT token response
- TokenData: extracted token info

**Product Schemas:**
- ProductBase: name, category, attributes
- ProductCreate: validates thickness_mm and coverage_sqm are present
- Product: includes unit conversions (thickness_in, coverage_sqft)

**Supplier Schemas:**
- SupplierBase: name, tier, tags
- SupplierCreate: same as base
- Supplier: includes id

**Offer Schemas:**
- OfferBase: product_id, supplier_id, price, currency
- OfferCreate: same as base
- Offer: includes id and created_at

**Event Schemas:**
- EventBase: product_id, session_id
- EventCreate: same as base
- Event: includes id and timestamp

**Analytics Schemas:**
- TrendingProduct: product_id, product_name, category, view_count

**Why it's important:** This prevents bad data from entering your system. If someone tries to create a product without thickness_mm, this will reject it with a helpful error message.

---

## **5. auth.py - Authentication Logic**

**What it does:**
Contains all the **security and authentication functions**. This is where passwords are hashed and tokens are created.

**Purpose:**

**Password Functions:**
- verify_password(): checks if plain password matches hashed version
- get_password_hash(): converts plain password to secure hash

**Token Functions:**
- create_access_token(): generates JWT token with expiration
- SECRET_KEY: signs the token (change in production!)
- ALGORITHM: HS256
- ACCESS_TOKEN_EXPIRE_MINUTES: 30

**User Functions:**
- authenticate_user(): checks email and password
- get_current_user(): extracts user from token

**Why it's important:** Without this, anyone could access any endpoint. This is your security guard.

---

##  **6. routers/ - API Endpoints Folder**

This folder contains all the **actual API endpoints**. Each file handles a different group of related endpoints.

---

###  **routers/auth.py - Authentication Endpoints**

**What it does:**
Handles user registration and login.

**Endpoints:**

**POST /api/register**
- Takes: email, password
- Does: creates new user in database
- Returns: user info (id, email, created_at)

**POST /api/login**
- Takes: email, password
- Does: verifies credentials, creates JWT token
- Returns: access_token, token_type

**Why it's important:** This is how users get into the system and get their access tokens.

---

###  **routers/products.py - Product Endpoints**

**What it does:**
Handles everything related to products - viewing, searching, creating.

**Endpoints:**

**GET /api/products**
- Takes: filters (category, supplier_tier, supplier_tag, unit_system)
- Does: searches database, applies filters, converts units
- Returns: list of products with unit conversions

**GET /api/products/{id}**
- Takes: product ID
- Does: finds specific product
- Returns: single product with details

**POST /api/products** (protected)
- Takes: name, category, attributes
- Does: creates new product
- Returns: created product

**Why it's important:** This is the core functionality - browsing and managing the catalog.

---

###  **routers/suppliers.py - Supplier Endpoints**

**What it does:**
Handles supplier management.

**Endpoints:**

**POST /api/suppliers** (protected)
- Takes: name, tier, tags
- Does: creates new supplier
- Returns: created supplier

**Why it's important:** This builds your supplier database.

---

###  **routers/offers.py - Offer Endpoints**

**What it does:**
Handles pricing offers - connecting products to suppliers with prices.

**Endpoints:**

**POST /api/offers** (protected)
- Takes: product_id, supplier_id, price, currency
- Does: verifies product and supplier exist, creates offer
- Returns: created offer

**Why it's important:** This creates the actual business relationship - who sells what for how much.

---

###  **routers/analytics.py - Analytics Endpoints**

**What it does:**
Handles event tracking and insights generation.

**Endpoints:**

**POST /api/events**
- Takes: product_id, session_id
- Does: records that someone viewed a product
- Returns: success message

**GET /api/insights/trending**
- Takes: window_hours, limit
- Does: counts views per product in time window
- Returns: top products by view count

**Why it's important:** This turns raw data into business intelligence. It tells you what's popular.

---

##  **7. Additional Important Files**

###  **__init__.py files**

**What they do:**
Empty files that tell Python: "This folder is a Python package."

**Where they are:**
- `/app/__init__.py`
- `/app/routers/__init__.py`

**Why they're important:** Without these, you can't do `from routers import auth`. They make the folder structure importable.

---

##  **HOW ALL FILES WORK TOGETHER**

Here's the **data flow** through the application:

```
1. HTTP Request comes in
        ↓
2. routers/products.py catches it
   (based on URL: /api/products)
        ↓
3. schemas.py validates the data
   (checks if required fields exist)
        ↓
4. auth.py checks if user is authenticated
   (for protected endpoints)
        ↓
5. database.py provides database connection
   (get_db() function)
        ↓
6. models.py defines how to query/save
   (Product, Supplier, Offer classes)
        ↓
7. CRUD operations happen
   (save to database, retrieve data)
        ↓
8. schemas.py formats the response
   (adds unit conversions, removes sensitive data)
        ↓
9. HTTP Response goes back to client
```

---

##  **FILE RESPONSIBILITIES SUMMARY**

| File | Responsibility | Simple Explanation |
|------|---------------|-------------------|
| **main.py** | Application setup | "The CEO - makes all departments work together" |
| **database.py** | Database connection | "The power supply - keeps the data flowing" |
| **models.py** | Table structure | "The blueprint - defines what data looks like" |
| **schemas.py** | Data validation | "The quality control - checks all incoming/outgoing data" |
| **auth.py** | Security | "The security guard - controls who gets in" |
| **routers/auth.py** | Login/Register | "The reception desk - handles new and returning users" |
| **routers/products.py** | Product management | "The catalog department - manages all products" |
| **routers/suppliers.py** | Supplier management | "The vendor relations - manages suppliers" |
| **routers/offers.py** | Price management | "The pricing department - connects products to suppliers with prices" |
| **routers/analytics.py** | Analytics | "The market research - tracks what people view" |

---

##  **VISUAL REPRESENTATION**

```
                    ┌─────────────────┐
                    │     main.py     │
                    │   (The Boss)    │
                    └────────┬────────┘   │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────┴────┐        ┌────┴────┐        ┌─────┴─────┐
    │database │        │  auth   │        │  routers  │
    │   .py   │        │   .py   │        │  folder   │
    └────┬────┘        └────┬────┘        └─────┬─────┘
         │                  │                   │
    ┌────┴────┐        ┌────┴────┐        ┌────┴─────┐
    │ models  │        │ schemas │        │ auth.py  │
    │   .py   │        │   .py   │        │ products │
    └─────────┘        └─────────┘        │suppliers │
                                          │ offers   │
                                          │analytics │
                                          └──────────┘
```

---

##  **WHAT EACH FILE DOES - ONE LINERS**

**main.py** - Starts the server and connects everything

**database.py** - Talks to the SQLite database file

**models.py** - Defines what a User, Product, Supplier, Offer, Event look like in the database

**schemas.py** - Defines what data should look like when it comes in and goes out

**auth.py** - Hashes passwords and creates/verifies JWT tokens

**routers/auth.py** - Endpoints for /register and /login

**routers/products.py** - Endpoints for viewing and creating products

**routers/suppliers.py** - Endpoint for creating suppliers

**routers/offers.py** - Endpoint for creating price offers

**routers/analytics.py** - Endpoints for recording views and getting trending products

---

 