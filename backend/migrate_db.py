"""
Database migration script to add missing columns
"""
from sqlalchemy import text
from database import engine

def migrate():
    with engine.connect() as conn:
        try:
            # Add supplier column to products table if it doesn't exist
            conn.execute(text("""
                ALTER TABLE products 
                ADD COLUMN IF NOT EXISTS supplier VARCHAR;
            """))
            conn.commit()
            print("✓ Added supplier column to products table")
        except Exception as e:
            print(f"Error adding supplier column: {e}")
        
        try:
            # Create inventory_history table if it doesn't exist
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS inventory_history (
                    id SERIAL PRIMARY KEY,
                    product_id INTEGER NOT NULL,
                    action VARCHAR NOT NULL,
                    quantity_change INTEGER DEFAULT 0,
                    performed_by VARCHAR,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            conn.commit()
            print("✓ Created inventory_history table")
        except Exception as e:
            print(f"Error creating inventory_history table: {e}")
        
        try:
            # Create users table if it doesn't exist
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR UNIQUE NOT NULL,
                    email VARCHAR UNIQUE NOT NULL,
                    password VARCHAR NOT NULL,
                    role VARCHAR DEFAULT 'customer',
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            conn.commit()
            print("✓ Created users table")
        except Exception as e:
            print(f"Error creating users table: {e}")
        
        print("\nMigration completed!")

if __name__ == "__main__":
    migrate()
