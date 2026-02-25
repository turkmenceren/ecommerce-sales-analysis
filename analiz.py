import pandas as pd
from sqlalchemy import create_engine

# 1. ADIM: Veriyi Oku ve SQL'e Aktar
yol = r'D:\CEREN\Documents\ecommerce-sales-analysis\Sample - Superstore.csv'
df = pd.read_csv(yol, encoding='ISO-8859-1')

# Sütun isimlerini temizle (boşlukları _ yap, küçük harfe çevir)
df.columns = [c.replace(' ', '_').lower() for c in df.columns]

# SQL Motorunu hazırla ve veriyi yükle
engine = create_engine('sqlite:///ecommerce.db')
df.to_sql('satislar', con=engine, index=False, if_exists='replace')

print("--- VERİ TABANI HAZIR VE ANALİZLER BAŞLIYOR ---\n")

# 2. ADIM: SQL Sorgularını Çalıştır

# ANALİZ 1: Kategori Bazlı Kârlılık
sorgu_kategori = """
SELECT 
    category, 
    ROUND(SUM(sales), 2) as toplam_satis, 
    ROUND(SUM(profit), 2) as toplam_kar,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) as kar_marji
FROM satislar
GROUP BY category
ORDER BY toplam_kar DESC;
"""
print("1. KATEGORİ BAZLI KÂRLILIK:")
print(pd.read_sql_query(sorgu_kategori, engine))
print("-" * 30)

# ANALİZ 2: En Çok Zarar Ettiren 5 Ürün
sorgu_zarar = """
SELECT 
    product_name, 
    category,
    ROUND(SUM(profit), 2) as net_zarar
FROM satislar
GROUP BY product_name
HAVING net_zarar < 0
ORDER BY net_zarar ASC
LIMIT 5;
"""
print("2. EN ÇOK ZARAR ETTİREN 5 ÜRÜN:")
print(pd.read_sql_query(sorgu_zarar, engine))
print("-" * 30)

# ANALİZ 3: En Sadık Müşteriler (En çok sipariş veren ilk 5)
sorgu_musteri = """
SELECT 
    customer_name, 
    COUNT(order_id) as siparis_sayisi,
    ROUND(SUM(sales), 2) as toplam_harcama
FROM satislar
GROUP BY customer_id
ORDER BY siparis_sayisi DESC
LIMIT 5;
"""
print("3. EN ÇOK SİPARİŞ VEREN MÜŞTERİLER:")
print(pd.read_sql_query(sorgu_musteri, engine))
# Analiz dosyanın sonuna ekle
sorgu_rfm = """
SELECT 
    customer_name,
    COUNT(order_id) as frekans,
    SUM(sales) as parasal_deger,
    MAX(order_date) as son_alisveris
FROM satislar
GROUP BY customer_id
ORDER BY parasal_deger DESC;
"""
rfm_df = pd.read_sql_query(sorgu_rfm, engine)
print("\n--- RFM ANALİZİ İÇİN HAM VERİ ---")
print(rfm_df.head())
sorgu_eyalet = """
SELECT 
    state, 
    SUM(sales) as eyalet_satis, 
    SUM(profit) as eyalet_kar
FROM satislar
GROUP BY state
ORDER BY eyalet_kar ASC;
"""
eyalet_df = pd.read_sql_query(sorgu_eyalet, engine)
print("\n--- EYALET BAZLI KAR/ZARAR TABLOSU ---")
print(eyalet_df.head())