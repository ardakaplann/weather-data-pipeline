"""
Bu script, weather_schema.sql ve weather_load_data.sql dosyalarını sırasıyla
MySQL veritabanına karşı çalıştırır ve foreign key ilişkisinin doğru
kurulduğunu doğrular.

Kullanmadan önce:
1. `pip install mysql-connector-python python-dotenv`
2. Proje klasöründe bir `.env` dosyası oluştur ve içine şunları yaz:
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=senin_sifren
   DB_NAME=weather_db
"""

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            allow_local_infile=True,
        )
        return connection
    except Error as e:
        print(f"HATA: Veritabanına bağlanılamadı: {e}")
        raise


def run_sql_file(cursor, filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            sql_script = f.read()
    except FileNotFoundError:
        print(f"HATA: '{filepath}' bulunamadı.")
        raise

    # Yorum satırlarını atlayarak sorguları ';' ile ayırıyoruz
    statements = [s.strip() for s in sql_script.split(";") if s.strip()]

    for statement in statements:
        try:
            cursor.execute(statement)
        except Error as e:
            # 1826: Duplicate foreign key constraint name
            # Bu, script'in daha önce çalıştırılmış olduğu ve constraint'in
            # zaten kurulu olduğu anlamına gelir - durdurmaya gerek yok.
            if e.errno == 1826:
                print("UYARI: Foreign key zaten mevcut, atlanıyor.")
                continue
            print(f"HATA: Şu sorgu çalıştırılırken sorun oluştu:\n{statement}\n{e}")
            raise


def validate_foreign_key(cursor):
    try:
        cursor.execute("SELECT COUNT(*) FROM weather_data WHERE status_id IS NULL")
        result = cursor.fetchone()
        null_count = result[0]

        if null_count == 0:
            print("Doğrulama başarılı: status_id ilişkisi tam olarak kuruldu (0 NULL).")
        else:
            print(f"UYARI: {null_count} satırda status_id NULL kaldı. Eşleştirmeyi kontrol et.")
    except Error as e:
        print(f"HATA: Doğrulama sorgusu çalıştırılamadı: {e}")
        raise


def main():
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        print("Tablo yapısı oluşturuluyor (weather_schema.sql)...")
        run_sql_file(cursor, "weather_schema.sql")
        connection.commit()

        print("Veriler yükleniyor (weather_load_data.sql)...")
        run_sql_file(cursor, "weather_load_data.sql")
        connection.commit()

        print("Foreign key ilişkisi doğrulanıyor...")
        validate_foreign_key(cursor)

        cursor.close()
        print("Pipeline başarıyla tamamlandı.")

    except Error as e:
        print(f"Pipeline sırasında bir veritabanı hatası oluştu: {e}")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
    finally:
        if connection is not None and connection.is_connected():
            connection.close()
            print("Veritabanı bağlantısı kapatıldı.")


if __name__ == "__main__":
    main()
