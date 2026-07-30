import pandas as pd
import numpy as np
from datetime import datetime

# ----------------------------------------------------------------
#                          VERİ OKUMA
# ----------------------------------------------------------------

try:
    df = pd.read_csv("datasets/weatherHistory.csv")
except FileNotFoundError:
    print("HATA: 'datasets/weatherHistory.csv' bulunamadı. Dosya yolunu kontrol et.")
    raise
except pd.errors.EmptyDataError:
    print("HATA: CSV dosyası boş.")
    raise
except pd.errors.ParserError:
    print("HATA: CSV dosyası okunurken format hatası oluştu.")
    raise

# ----------------------------------------------------------------
#                          VERİ TEMİZLİĞİ
# ----------------------------------------------------------------

column = df.columns
isnull_test = df.isnull().sum()
df.fillna(value='unknown', inplace=True)

# ----------------------------------------------------------------
#               ZAMAN SERİSİ VE TARİH MANİPÜLASYONU
# ----------------------------------------------------------------

try:
    df['Formatted Date'] = pd.to_datetime(df['Formatted Date'], utc=True)
    df['Year'] = df['Formatted Date'].dt.year
    df['Month'] = df['Formatted Date'].dt.month
    df['Day'] = df['Formatted Date'].dt.day
except KeyError:
    print("HATA: 'Formatted Date' sütunu bulunamadı. Sütun adlarını kontrol et:", df.columns.tolist())
    raise
except (ValueError, TypeError) as e:
    print(f"HATA: Tarih dönüşümü sırasında sorun oluştu: {e}")
    raise

# ----------------------------------------------------------------
#            Sütun İsimlerini SQL'e Uyumlu Hale Getirme
# ----------------------------------------------------------------

df.columns = (
    df.columns.str.lower()
    .str.replace('(', '', regex=False)
    .str.replace(')', '', regex=False)
    .str.replace(' ', '_', regex=False)
    .str.replace('/', '', regex=False)
    .str.strip()
)

try:
    df.drop("loud_cover", axis=1, inplace=True)
except KeyError:
    print("UYARI: 'loud_cover' sütunu bulunamadı, atlanıyor.")

try:
    status_types = df[['summary', 'precip_type']].drop_duplicates().reset_index(drop=True)
except KeyError as e:
    print(f"HATA: Beklenen sütun bulunamadı: {e}")
    raise

# ----------------------------------------------------------------
#            İlişkisel Veritabanı İçin Tabloları Ayırma (Merge)
# ----------------------------------------------------------------

status_types['status_id'] = range(1, len(status_types) + 1)

try:
    df = df.merge(status_types, on=['summary', 'precip_type'], how='left')
except (KeyError, ValueError) as e:
    print(f"HATA: Merge işlemi sırasında sorun oluştu: {e}")
    raise

# Merge sonrası status_id ataması kontrolü - eşleşmeyen satır kaldı mı?
unmatched = df['status_id'].isnull().sum()
if unmatched > 0:
    print(f"UYARI: {unmatched} satırda status_id eşleşmesi bulunamadı (NULL kaldı).")

df.drop(['summary', 'precip_type'], axis=1, inplace=True)

# ----------------------------------------------------------------
#                      CSV Olarak Dışa Aktarma
# ----------------------------------------------------------------

try:
    df.to_csv("datasets/lastWeatherHistory.csv", index=False)
    status_types.to_csv("datasets/statusTypes.csv", index=False)
except (PermissionError, OSError) as e:
    print(f"HATA: CSV dosyaları yazılırken sorun oluştu: {e}")
    raise

print("İşlem tamamlandı.")
print("weather_data sütunları:", df.columns.tolist())
print("status_types sütunları:", status_types.columns.tolist())
