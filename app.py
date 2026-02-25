import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# 1. Veritabanı Bağlantısı
engine = create_engine('sqlite:///ecommerce.db')

# Sayfa Ayarları
st.set_page_config(page_title="E-Ticaret Analiz Paneli", layout="wide")
st.title("📊 E-Ticaret Satış Analizi Dashboard")
st.markdown("SQL Sorguları ile Hazırlanmış Canlı Veri Analizi")

# --- SOL MENÜ (Filtreler için hazırlık) ---
st.sidebar.header("Analiz Seçenekleri")
analiz_turu = st.sidebar.selectbox("Bir Analiz Seçin", 
    ["Genel Bakış", "Kategori Analizi", "Zarar Eden Ürünler", "Müşteri Analizi"])

# --- ANALİZLER ---

if analiz_turu == "Genel Bakış":
    st.subheader("📍 Şehirlere Göre Toplam Satış")
    # SQL Sorguları:
    sorgu = "SELECT city, SUM(sales) as toplam_satis FROM satislar GROUP BY city ORDER BY toplam_satis DESC LIMIT 10"
    df = pd.read_sql_query(sorgu, engine)
    
    # Grafik oluşturma
    fig = px.bar(df, x='toplam_satis', y='city', orientation='h', 
                 title="En Çok Satış Yapan 10 Şehir", color='toplam_satis')
    st.plotly_chart(fig, use_container_width=True)

elif analiz_turu == "Kategori Analizi":
    st.subheader("📦 Kategori Bazlı Kârlılık")
    sorgu = """
    SELECT category, SUM(sales) as satis, SUM(profit) as kar 
    FROM satislar GROUP BY category
    """
    df = pd.read_sql_query(sorgu, engine)
    st.table(df) # Tablo olarak göster
    
    fig = px.pie(df, values='kar', names='category', title="Kâr Dağılımı")
    st.plotly_chart(fig)

elif analiz_turu == "Zarar Eden Ürünler":
    st.subheader("⚠️ Acil Müdahale Gereken Ürünler (Zarar)")
    sorgu = """
    SELECT product_name, SUM(profit) as net_kar 
    FROM satislar GROUP BY product_name HAVING net_kar < 0 
    ORDER BY net_kar ASC LIMIT 10
    """
    df = pd.read_sql_query(sorgu, engine)
    st.dataframe(df) # İnteraktif tablo

elif analiz_turu == "Müşteri Analizi":
    st.subheader("👤 En Çok Harcama Yapan VIP Müşteriler")
    sorgu = "SELECT customer_name, SUM(sales) as harcama FROM satislar GROUP BY customer_id ORDER BY harcama DESC LIMIT 10"
    df = pd.read_sql_query(sorgu, engine)
    st.bar_chart(df.set_index('customer_name'))