"""
Fix NULL values in supplier column
"""
from sqlalchemy import text
from database import engine

def fix_nulls():
    with engine.connect() as conn:
        try:
            # Update NULL supplier values to empty string
            result = conn.execute(text("""
                UPDATE products 
                SET supplier = '' 
                WHERE supplier IS NULL;
            """))
            conn.commit()
            print(f"✓ Updated {result.rowcount} products with NULL supplier values")
            
            # Update NULL description values to empty string
            result = conn.execute(text("""
                UPDATE products 
                SET description = '' 
                WHERE description IS NULL;
            """))
            conn.commit()
            print(f"✓ Updated {result.rowcount} products with NULL description values")
            
            # Update NULL category values to empty string
            result = conn.execute(text("""
                UPDATE products 
                SET category = '' 
                WHERE category IS NULL;
            """))
            conn.commit()
            print(f"✓ Updated {result.rowcount} products with NULL category values")
            
            print("\nDatabase cleanup completed!")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    fix_nulls()
