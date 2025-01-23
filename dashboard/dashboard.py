import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk memuat dataset lokal

def load_data():
    data = pd.read_csv("dashboard/all_data.csv")  # Sesuaikan dengan nama file dataset
    return data

# Load data
data = load_data()

# Judul Dashboard
st.title("Dashboard Analisis Polusi Udara")

# Sidebar untuk memilih kota
st.sidebar.header("Filter")
cities = data['station'].unique()
selected_city = st.sidebar.selectbox("Pilih Kota", cities)

# Filter data berdasarkan kota yang dipilih
filtered_data = data[data['station'] == selected_city]

# Tab Menu
tab1, tab2, tab3 = st.tabs(["📊 Statistik", "🔍 Korelasi", "🌡️ Heatmap"])

# Tab 1: Statistik Rata-rata Polusi
with tab1:
    st.subheader(f"Statistik Rata-rata Polusi di {selected_city}")
    avg_pm25 = filtered_data['PM2.5'].mean()
    avg_pm10 = filtered_data['PM10'].mean()

    st.write(f"**Rata-rata PM2.5:** {avg_pm25:.2f}")
    st.write(f"**Rata-rata PM10:** {avg_pm10:.2f}")
    
    st.write("Distribusi PM2.5 dan PM10:")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(filtered_data['PM2.5'], bins=30, kde=True, color='blue', label='PM2.5', ax=ax)
    sns.histplot(filtered_data['PM10'], bins=30, kde=True, color='orange', label='PM10', ax=ax)
    ax.legend()
    st.pyplot(fig)

# Tab 2: Korelasi
with tab2:
    st.subheader(f"Korelasi antara Faktor Cuaca dan PM2.5 di {selected_city}")
    corr = filtered_data[['PM2.5', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title(f"Korelasi antara Faktor Cuaca dan PM2.5 di {selected_city}")
    st.pyplot(fig)

# Tab 3: Heatmap Polusi
with tab3:
    st.subheader(f"Pola Musiman PM2.5 di {selected_city}")

    # Tambahkan kolom bulan untuk visualisasi musiman
    filtered_data['month'] = pd.to_datetime(filtered_data[['year', 'month', 'day']]).dt.month
    seasonal_avg = filtered_data.groupby('month')['PM2.5'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='month', y='PM2.5', data=seasonal_avg, palette='viridis', ax=ax)
    ax.set_title(f"Rata-rata PM2.5 Bulanan di {selected_city}")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("PM2.5")
    st.pyplot(fig)
