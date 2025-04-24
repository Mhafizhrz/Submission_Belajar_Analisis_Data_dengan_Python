import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Memuat data dari file CSV
file_path = "Dashboard/data.csv"
bike_df = pd.read_csv(file_path)

# Judul Dashboard
st.title("Analisis Penggunaan Bike Sharing")

# Sidebar untuk navigasi dan eksplorasi data
with st.sidebar:
    st.subheader('🚴 Statistik Bike Sharing 🚴')
    st.image("https://images.pexels.com/photos/100582/pexels-photo-100582.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2")
    
    st.header("📃 Cek Data")
    with st.expander("📊 Tampilkan Data"):
        show_overview = st.checkbox("Tampilkan Overview Data", value=True)
        show_head = st.checkbox("Tampilkan 5 Baris Pertama", value=True)
        show_summary_stats = st.checkbox("Tampilkan Statistik Ringkas", value=True)
        show_graphs = st.checkbox("Tampilkan Grafik", value=True)

# Menampilkan data berdasarkan status checkbox
if show_overview:
    st.subheader("Deskripsi Dataset")
    st.write("""Dataset ini mencakup data penggunaan bike sharing, dengan informasi terkait cuaca, 
    hari dalam minggu, serta jam-jam tertentu yang mempengaruhi frekuensi peminjaman sepeda.""")

if show_head:
    st.subheader("5 Baris Pertama Data")
    st.write(bike_df.head())

if show_summary_stats:
    st.subheader("Ringkasan Statistik Dataset")
    st.write(bike_df.describe())

# Visualisasi data
if show_graphs:
    st.subheader("Visualisasi Data Penggunaan Bike Sharing")

    # 1. Pie chart: Penyewaan sepeda pada hari kerja vs akhir pekan
    avg_workingday = bike_df.groupby('workingday_day')['cnt_day'].mean()
    labels = ['Akhir Pekan', 'Hari Kerja']
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(avg_workingday, labels=labels, autopct='%1.1f%%', colors=['lightgreen', 'skyblue'], startangle=90)
    ax.set_title("Perbandingan Penyewaan Bike Sharing: Hari Kerja vs Akhir Pekan")
    st.pyplot(fig)
    
    # 2. Bar chart: Pengaruh cuaca terhadap jumlah penyewaan sepeda
    weather_impact = bike_df.groupby('weather_label')['cnt_day'].mean().reset_index()
    weather_impact_sorted = weather_impact.sort_values("cnt_day", ascending=False)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=weather_impact_sorted, x='cnt_day', y='weather_label', hue='weather_label', palette='coolwarm', ax=ax2, legend=False)
    ax2.set_title("Pengaruh Kondisi Cuaca terhadap Penyewaan Bike Sharing")
    ax2.set_xlabel("Rata-rata Penyewaan")
    ax2.set_ylabel("Jenis Cuaca")
    st.pyplot(fig2)
    
    # 3. Line chart: Tren penyewaan sepeda antara pengguna casual dan registered per jam
    hourly_trend = bike_df.groupby('hr')[['casual_hour', 'registered_hour']].mean().reset_index()
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    ax3.plot(hourly_trend['hr'], hourly_trend['casual_hour'], label='Casual', marker='o', color='orange')
    ax3.plot(hourly_trend['hr'], hourly_trend['registered_hour'], label='Registered', marker='s', color='purple')
    ax3.set_title("Pola Penyewaan Bike Sharing per Jam: Casual vs Registered")
    ax3.set_xlabel("Jam dalam Sehari")
    ax3.set_ylabel("Jumlah Penyewaan")
    ax3.set_xticks(range(0, 24))
    ax3.legend(title="Tipe Pengguna")
    ax3.grid(axis='y', linestyle='--', alpha=0.6)
    st.pyplot(fig3)

st.caption('Hak Cipta (c) Hafizh')
