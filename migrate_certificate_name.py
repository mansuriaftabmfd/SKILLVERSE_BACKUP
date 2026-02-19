"""
Migration Script: Add certificate_name field to orders table
"""

import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from models import db

def migrate():
    """Add certificate_name column to orders table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Add certificate_name column (stores the name user wants on certificate)
            db.session.execute(db.text("""
                ALTER TABLE orders 
                ADD COLUMN IF NOT EXISTS certificate_name VARCHAR(200)
            """))
            
            db.session.commit()
            print("[OK] Migration completed successfully!")
            print("  - Added 'certificate_name' column to orders table")
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Migration failed: {e}")

if __name__ == '__main__':
    migrate()
