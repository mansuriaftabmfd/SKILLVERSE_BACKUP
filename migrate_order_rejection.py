"""
Migration Script: Add Order Rejection Fields
Adds rejection_reason and can_review fields to orders table
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import create_app
from models import db

def migrate():
    """Add new columns to orders table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Add rejection_reason column
            db.session.execute(db.text("""
                ALTER TABLE orders 
                ADD COLUMN IF NOT EXISTS rejection_reason TEXT
            """))
            
            # Add can_review column (default TRUE for existing orders)
            db.session.execute(db.text("""
                ALTER TABLE orders 
                ADD COLUMN IF NOT EXISTS can_review BOOLEAN DEFAULT TRUE
            """))
            
            db.session.commit()
            print("[OK] Migration completed successfully!")
            print("  - Added 'rejection_reason' column to orders table")
            print("  - Added 'can_review' column to orders table")
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Migration failed: {e}")

if __name__ == '__main__':
    migrate()
