import sqlite3
import time
from contextlib import contextmanager

DATABASE_PATH = 'app.db'

def init_db():
    """Initialize the database with sample data"""
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Check if we need to insert sample data
        if conn.execute('SELECT COUNT(*) FROM products').fetchone()[0] == 0:
            # Insert 1000 sample products
            for i in range(1, 1001):
                conn.execute(
                    'INSERT INTO products (name, description, price) VALUES (?, ?, ?)',
                    (f'Product {i}', f'Description for product {i}', i * 10.99)
                )

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
