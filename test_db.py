from sqlalchemy import text
from app.core.database import engine

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("\n-----------------------------------")
            print("BAŞARILI: Veritabanı bağlantısı sağlandı!")
            print("-----------------------------------\n")
    except Exception as e:
        print("\n-----------------------------------")
        print(f"HATA: Bağlantı başarısız oldu.\nDetay: {e}")
        print("-----------------------------------\n")

if __name__ == "__main__":
    test_connection()