
from database import engine, SessionLocal
from models import DocGia, TaiLieu, NhanVien
from sqlalchemy import text

def test_connection():
    print("--- Testing Database Connection ---")
    try:
        # Try to connect and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Successfully connected to the database!")
            
            # Check for tables
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"Tables found: {', '.join(tables) if tables else 'None'}")
            
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return

    print("\n--- Testing Data Query ---")
    db = SessionLocal()
    try:
        # Count documents
        doc_count = db.query(TaiLieu).count()
        print(f"Number of documents (TaiLieu): {doc_count}")
        
        # Count readers
        reader_count = db.query(DocGia).count()
        print(f"Number of readers (DocGia): {reader_count}")

        # Count staff
        staff_count = db.query(NhanVien).count()
        print(f"Number of staff (NhanVien): {staff_count}")

    except Exception as e:
        print(f"Error querying data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
