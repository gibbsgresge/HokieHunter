import sys
import os
from sqlalchemy import create_engine, text
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_test.config import SQLALCHEMY_DATABASE_URI

def test_connection():
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Connected to MySQL! Result:", result.fetchone())
    except Exception as e:
        print("❌ Failed to connect:", e)

if __name__ == "__main__":
    test_connection()
