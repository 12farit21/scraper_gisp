import sqlite3
from pathlib import Path

DB_PATH = "gisp_products.db"

def init_db():
    """Initialize database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create companies table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY,
            catalogId INTEGER,
            gispId INTEGER,
            name TEXT,
            inn TEXT,
            ogrn TEXT,
            regionId INTEGER,
            contactFio TEXT,
            UNIQUE(id)
        )
    """)

    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            company_id INTEGER,
            name TEXT,
            createdAt_gisp TEXT,
            updatedAt_gisp TEXT,
            UNIQUE(id),
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
    """)

    conn.commit()
    conn.close()

def insert_company(company_data):
    """Insert company into database. Uses INSERT OR IGNORE for uniqueness."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT OR IGNORE INTO companies
            (id, catalogId, gispId, name, inn, ogrn, regionId, contactFio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            company_data.get('id'),
            company_data.get('catalogId'),
            company_data.get('gispId'),
            company_data.get('name'),
            company_data.get('inn'),
            company_data.get('ogrn'),
            company_data.get('regionId'),
            company_data.get('contactFio')
        ))
        conn.commit()
    finally:
        conn.close()

def insert_product(product_data):
    """Insert product into database. Uses INSERT OR IGNORE for uniqueness."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT OR IGNORE INTO products
            (id, company_id, name, createdAt_gisp, updatedAt_gisp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            product_data.get('id'),
            product_data.get('company_id'),
            product_data.get('name'),
            product_data.get('createdAt_gisp'),
            product_data.get('updatedAt_gisp')
        ))
        conn.commit()
    finally:
        conn.close()

def get_product_count():
    """Get total number of products in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_company_count():
    """Get total number of companies in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM companies")
    count = cursor.fetchone()[0]
    conn.close()
    return count
