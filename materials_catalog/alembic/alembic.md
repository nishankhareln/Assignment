# ALEMBIC FOLDER - Complete Description

##  **D:\Assignment\materials_catalog\alembic\**

## WHAT IS ALEMBIC?

**Alembic is a database migration tool for SQLAlchemy.** Think of it as **Git for your database schema**.

Just like Git tracks changes to your code files, Alembic tracks changes to your database structure. Every time you add a new column, create a new table, or change any database structure, Alembic creates a "migration" file that records exactly what changed.

---

##  **WHY DO YOU NEED ALEMBIC?**

### **The Problem Alembic Solves:**

Imagine you're working on this project with a team:

1. **Day 1:** You create the database with tables: users, products, suppliers
2. **Day 7:** You realize you need to add a "phone_number" column to suppliers table
3. **Day 14:** You need to add a "discount" column to offers table
4. **Day 21:** Your teammate adds a "rating" column to products table

**Without Alembic:**
- Everyone has to manually remember what changes were made
- You'd have to delete the database and recreate it every time
- Team members have inconsistent database structures
- Production database updates become risky manual operations

**With Alembic:**
- Every change is recorded in a migration file
- Anyone can run `alembic upgrade head` and get the exact same database structure
- Changes can be rolled back if something goes wrong
- Production updates are automated and safe

---

##  **ALEMBIC FOLDER STRUCTURE**

```
alembic/
├── versions/          #  Where all migration files live
│   ├── 0001_initial_migration.py
│   ├── 0002_add_phone_to_suppliers.py
│   └── 0003_add_discount_to_offers.py
├── env.py            #  Alembic environment configuration
├── README            # Alembic instructions
└── script.py.mako    # Template for creating new migrations
```

---

##  **1. alembic/versions/ - The Migration Files**

**What it is:** 
This folder contains **every single database change ever made** to the project, in chronological order.

### **What a Migration File Looks Like:**

```python
"""add phone number to suppliers table

Revision ID: 0002_add_phone_to_suppliers
Revises: 0001_initial_migration
Create Date: 2024-02-12 10:30:45.123456

"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = '0002_add_phone_to_suppliers'
down_revision = '0001_initial_migration'
branch_labels = None
depends_on = None

def upgrade():
    """What happens when you apply this migration"""
    op.add_column('suppliers', 
        sa.Column('phone_number', sa.String(), nullable=True)
    )

def downgrade():
    """What happens when you roll back this migration"""
    op.drop_column('suppliers', 'phone_number')
```

### **Why Each Migration Has Two Functions:**

- **upgrade()** - How to apply the change (add column, create table, etc.)
- **downgrade()** - How to undo the change (remove column, drop table, etc.)

This allows you to move **forward** and **backward** through database versions.

---

##  **2. alembic/env.py - The Configuration File**

**What it is:**
This is the **brain** of Alembic. It tells Alembic:

1. **Where your database is** (SQLite, PostgreSQL, etc.)
2. **What your models look like** (so it knows what to compare against)
3. **How to run migrations** (offline vs online mode)

### **What env.py Does:**

```python
# 1. Imports your SQLAlchemy models
from app.database import Base
from app import models

# 2. Gets your database URL
from app.database import engine

# 3. Tells Alembic about your models
target_metadata = Base.metadata

# 4. Provides functions to run migrations
def run_migrations_online():
    # Connects to your actual database
    connectable = engine_from_config(...)
    
def run_migrations_offline():
    # Generates SQL without connecting to database
    context.configure(url=url, target_metadata=target_metadata)
```

**Why two modes?**
- **Online mode:** Actually connects to your database and makes changes
- **Offline mode:** Generates SQL script you can review before running

---

##  **3. alembic/script.py.mako - The Template File**

**What it is:**
A **template** that Alembic uses when you create a new migration. Instead of writing every migration from scratch, Alembic uses this template to generate the basic structure.

### **What It Contains:**

```python
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

def upgrade():
    ${upgrades if upgrades else "pass"}

def downgrade():
    ${downgrades if downgrades else "pass"}
```

The `${variables}` get filled in automatically when you run:
```bash
alembic revision --autogenerate -m "your message here"
```

---

##  **4. alembic/README - Documentation File**

**What it is:**
A simple text file with basic Alembic instructions. Usually contains:

```
Generic single-database configuration.

This Alembic migration environment was generated with:

    alembic init alembic

To create a new migration:

    alembic revision --autogenerate -m "description"

To upgrade database to latest version:

    alembic upgrade head

To downgrade to a specific version:

    alembic downgrade <revision_id>
```

---

##  **5. alembic.ini (in root folder, not inside alembic/)**

**What it is:**
The **master configuration file** located in your project root. This connects your project to Alembic.

### **What It Contains:**

```ini
# Where Alembic finds your migration files
script_location = alembic

# Your database connection string
sqlalchemy.url = sqlite:///./materials.db

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

# Post-migration hooks (auto-format code)
[post_write_hooks]
hooks = black
```

---

##  **ALEMBIC COMMANDS - WHAT THEY DO**

### **Command 1: Initialize Alembic**
```bash
alembic init alembic
```
**What it does:** Creates the entire alembic folder structure the first time.

---

### **Command 2: Create a Migration**
```bash
alembic revision --autogenerate -m "add phone to suppliers"
```
**What it does:**
1. Compares your current database with your models.py
2. Detects what changed (new tables, new columns, etc.)
3. Generates a new migration file in versions/ folder
4. Names it something like: `0002_add_phone_to_suppliers.py`

---

### **Command 3: Apply Migrations**
```bash
alembic upgrade head
```
**What it does:**
1. Checks which migrations have been applied
2. Applies all pending migrations in order
3. Updates your database to match your models.py

---

### **Command 4: Rollback Migration**
```bash
alembic downgrade -1
```
**What it does:**
1. Reverts the last migration
2. Calls the downgrade() function
3. Restores database to previous state

---

### **Command 5: Check Status**
```bash
alembic current
```
**What it does:** Shows which migration is currently applied

```bash
alembic history
```
**What it does:** Shows all migrations and their relationships

---

##  **REAL-WORLD EXAMPLE: ADDING A NEW COLUMN**

Let's say you want to add a "stock_quantity" column to your products table:

### **Step 1: Update models.py**
```python
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # ... existing columns ...
    stock_quantity = Column(Integer, default=0)  # NEW COLUMN
```

### **Step 2: Generate Migration**
```bash
alembic revision --autogenerate -m "add stock quantity to products"
```

**What Alembic does:**
1. Looks at your current database
2. Looks at your updated models.py
3. Detects: "Hey, there's a new column 'stock_quantity'!"
4. Creates a migration file with upgrade() and downgrade()

### **Step 3: Apply Migration**
```bash
alembic upgrade head
```

**What Alembic does:**
1. Reads the new migration file
2. Executes: `ALTER TABLE products ADD COLUMN stock_quantity INTEGER`
3. Updates the migration tracking table
4. Your database now has the new column

### **Step 4: If Something Goes Wrong**
```bash
alembic downgrade -1
```

**What Alembic does:**
1. Reads the downgrade() function
2. Executes: `ALTER TABLE products DROP COLUMN stock_quantity`
3. Your database is back to how it was before

---

##  **WHY YOU NEED ALEMBIC FOR THIS PROJECT**

### **Scenario 1: Team Development**
- **You** add supplier tags feature (requires new tags table)
- **Your teammate** adds product ratings feature (requires new column)
- Without Alembic: Chaos, manual SQL scripts, "works on my machine"
- With Alembic: `alembic upgrade head` and everyone's database is identical

### **Scenario 2: Production Deployment**
- Your API is live with real customer data
- You need to add a new feature that requires database changes
- Without Alembic: Fear, manual backups, risky ALTER TABLE statements
- With Alembic: Run `alembic upgrade head` on production server, zero downtime

### **Scenario 3: Bug Fixes**
- You realize a migration accidentally deleted important data
- Without Alembic: Panic, restore from backup, lose recent data
- With Alembic: `alembic downgrade` and you're back to working state

### **Scenario 4: Code Review**
- Teammate submits a pull request with database changes
- Without Alembic: How do you review what changed in the database?
- With Alembic: Open the migration file, see exact SQL changes in plain text

---

##  **THE ALEMBIC_TRACKING TABLE**

Alembic creates a special table in your database called:

**`alembic_version`**

| version_num |
|-------------|
| 0003_add_discount_to_offers |

**What it does:** 
This single-row table tracks which migration is currently applied. When you run `alembic upgrade head`, Alembic:
1. Reads this table to see where you are
2. Applies migrations until you reach the target version
3. Updates this table with the new version

---

##  **ALEMBIC VS GIT - ANALOGY**

| Git (Code) | Alembic (Database) |
|------------|-------------------|
| `git init` | `alembic init` |
| `git add file.py` | `alembic revision --autogenerate` |
| `git commit -m "message"` | Creates migration file |
| `git push` | `alembic upgrade head` |
| `git log` | `alembic history` |
| `git checkout HEAD~1` | `alembic downgrade -1` |
| `git status` | `alembic current` |
| `.git/` folder | `alembic/` folder |
| `.gitignore` | `alembic.ini` |

**Just like you wouldn't code without Git, you shouldn't change database schemas without Alembic!**

---

## **ALEMBIC IN YOUR PROJECT - SPECIFIC USE**

For your Materials Catalog API, Alembic tracks changes to:

### **Initial Migration (Created when you run `alembic upgrade head` first time)**
```python
"""initial migration

Creates all tables:
- users
- products
- suppliers
- offers
- events
"""
```

### **Potential Future Migrations:**

**Migration 2:** Add phone_number to suppliers
```python
"""add contact info to suppliers"""
```

**Migration 3:** Add discount column to offers
```python
"""add discount field for promotions"""
```

**Migration 4:** Add rating column to products
```python
"""add user rating system"""
```

**Migration 5:** Add category_metadata table
```python
"""separate categories into their own table"""
```

---

##  **SUMMARY - WHAT ALEMBIC DOES FOR YOU**

| Without Alembic | With Alembic |
|-----------------|--------------|
| Manual SQL scripts |  Automated migrations |
| Different team members have different DBs |  Everyone has identical DB |
| Fear of production changes |  Safe, reversible upgrades |
| No history of changes |  Complete version history |
| Hard to review DB changes |  Migration files are code reviewable |
| Risk of data loss |  Rollback capability |
| "Works on my machine" |  Works everywhere |

---

##  **ALEMBIC COMMANDS CHEAT SHEET**

```bash
# First time setup
alembic init alembic                    # Create alembic folder

# Creating migrations
alembic revision --autogenerate -m "description"  # Create migration
alembic revision -m "manual description"          # Create empty migration

# Applying migrations
alembic upgrade head                   # Apply all pending migrations
alembic upgrade +2                     # Apply next 2 migrations
alembic upgrade <revision_id>         # Upgrade to specific version

# Rolling back
alembic downgrade -1                  # Undo last migration
alembic downgrade base                # Undo all migrations
alembic downgrade <revision_id>      # Downgrade to specific version

# Information
alembic current                       # Show current version
alembic history                       # Show all migrations
alembic show <revision_id>           # Show specific migration
```

---

##  **FINAL THOUGHT**

**Alembic is your database's time machine and backup system in one.** 

It's not just a nice-to-have - it's **essential** for any serious application. Your Materials Catalog API will evolve over time, and Alembic ensures that your database evolves with it, safely and consistently.

Without Alembic, you're flying blind. With Alembic, you have complete control and confidence when changing your database schema.