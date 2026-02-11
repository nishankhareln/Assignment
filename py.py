import os

BASE_DIR = "materials_catalog"

folders = [
    "alembic/versions",
    "app/routers",
    "tests"
]

files = [
    "README.md",
    "TESTING.md",
    "PROJECT_SUMMARY.md",
    "INTEGRATION_GUIDE.md",
    "FOLDER_STRUCTURE.md",
    "requirements.txt",
    ".gitignore",
    "alembic.ini",
    "quickstart.sh",
    "seed_data.py",

    "alembic/env.py",
    "alembic/script.py.mako",

    "app/__init__.py",
    "app/main.py",
    "app/database.py",
    "app/models.py",
    "app/schemas.py",
    "app/auth.py",

    "app/routers/__init__.py",
    "app/routers/auth.py",
    "app/routers/products.py",
    "app/routers/suppliers.py",
    "app/routers/offers.py",
    "app/routers/analytics.py",

    "tests/__init__.py",
    "tests/conftest.py",
    "tests/test_auth.py",
    "tests/test_products.py",
    "tests/test_conversion.py",
    "tests/test_analytics.py",
]

# Create base directory
os.makedirs(BASE_DIR, exist_ok=True)

# Create folders
for folder in folders:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

# Create files
for file in files:
    file_path = os.path.join(BASE_DIR, file)
    with open(file_path, "a"):
        pass

print("✅ materials_catalog folder structure created successfully!")
