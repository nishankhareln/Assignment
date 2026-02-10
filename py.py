import os

BASE_DIR = "materials-catalog"

# Helper functions
def make_dir(path):
    os.makedirs(path, exist_ok=True)

def make_file(path):
    open(path, "a").close()

# -----------------------------
# Create base project directory
# -----------------------------
make_dir(BASE_DIR)

# -----------------------------
# App directory structure
# -----------------------------
app_dirs = [
    "app/models",
    "app/schemas",
    "app/api",
    "app/core",
    "app/utils"
]

for d in app_dirs:
    make_dir(os.path.join(BASE_DIR, d))

# -----------------------------
# Alembic structure
# -----------------------------
make_dir(os.path.join(BASE_DIR, "alembic/versions"))

# -----------------------------
# Tests directory
# -----------------------------
make_dir(os.path.join(BASE_DIR, "tests"))

# -----------------------------
# __init__.py files
# -----------------------------
init_files = [
    "app/__init__.py",
    "app/models/__init__.py",
    "app/schemas/__init__.py",
    "app/api/__init__.py",
    "app/core/__init__.py",
    "app/utils/__init__.py",
    "tests/__init__.py"
]

for f in init_files:
    make_file(os.path.join(BASE_DIR, f))

# -----------------------------
# Model files
# -----------------------------
model_files = [
    "app/models/user.py",
    "app/models/product.py",
    "app/models/supplier.py",
    "app/models/offer.py",
    "app/models/event.py"
]

for f in model_files:
    make_file(os.path.join(BASE_DIR, f))

# -----------------------------
# Schema files
# -----------------------------
schema_files = [
    "app/schemas/user.py",
    "app/schemas/product.py",
    "app/schemas/supplier.py",
    "app/schemas/offer.py",
    "app/schemas/event.py"
]

for f in schema_files:
    make_file(os.path.join(BASE_DIR, f))

# -----------------------------
# API route files
# -----------------------------
api_files = [
    "app/api/deps.py",
    "app/api/auth.py",
    "app/api/products.py",
    "app/api/suppliers.py",
    "app/api/offers.py",
    "app/api/events.py",
    "app/api/insights.py"
]

for f in api_files:
    make_file(os.path.join(BASE_DIR, f))

# -----------------------------
# Core files
# -----------------------------
core_files = [
    "app/core/security.py",
    "app/core/conversions.py"
]

for f in core_files:
    make_file(os.path.join(BASE_DIR, f))

# -----------------------------
# Utility files
# -----------------------------
make_file(os.path.join(BASE_DIR, "app/utils/seed.py"))

# -----------------------------
# Main app files
# -----------------------------
main_files = [
    "app/main.py",
    "app/config.py",
    "app/database.py"
]

for f in main_files:
    make_file(os.path.join(BASE_DIR, f))

# -----------------------------
# Test files
# -----------------------------
test_files = [
    "tests/conftest.py",
    "tests/test_auth.py",
    "tests/test_products.py",
    "tests/test_conversions.py",
    "tests/test_insights.py"
]

for f in test_files:
    make_file(os.path.join(BASE_DIR, f))

# -----------------------------
# Root-level files
# -----------------------------
root_files = [
    "requirements.txt",
    ".env.example",
    ".gitignore",
    "README.md",
    "alembic.ini"
]

for f in root_files:
    make_file(os.path.join(BASE_DIR, f))

print("Folder structure created successfully!")
print(f"Project directory: {BASE_DIR}")
