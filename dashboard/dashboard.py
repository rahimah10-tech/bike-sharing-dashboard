from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

# Load data bersih (hasil cleaning di notebook)
# main_data.csv = data harian (day_df), hour_data.csv = data per jam (hour_df)
# Path dihitung dari lokasi file dashboard.py ini, bukan dari folder
# tempat perintah dijalankan — jadi tetap jalan di Streamlit Cloud,
# yang menjalankannya dari root repo, bukan dari folder dashboard/.
BASE_DIR = Path(__file__).parent
day_df = pd.read_csv(BASE_DIR / "main_data.csv", parse_dates=["dteday"])
hour_df = pd.read_csv(BASE_DIR / "hour_data.csv", parse_dates=["dteday"])

st.title("Dashboard Penyewaan Sepeda — Bike Sharing Dataset")
st.write(
    "Data Capital Bikeshare, Washington D.C., 2011–2012. "
    "Dashboard ini menjawab 2 pertanyaan bisnis dari notebook analisis."
)

# Sidebar filter
st.sidebar.header("Filter")
selected_year = st.sidebar.selectbox(
    "Pilih Tahun", options=["Semua", 2011, 2012]
)
if selected_year != "Semua":
    day_filtered = day_df[day_df["year"] == selected_year]
    hour_filtered = hour_df[hour_df["year"] == selected_year]
else:
    day_filtered = day_df
    hour_filtered = hour_df

# KPI
total_rentals = int(day_filtered["cnt"].sum())
avg_daily = float(day_filtered["cnt"].mean())
peak_hour = int(
    hour_filtered.groupby("hr")["cnt"].mean().idxmax()
)
col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", f"{total_rentals:,}".replace(",", "."))
col2.metric("Rata-rata per Hari", f"{avg_daily:,.0f}".replace(",", "."))
col3.metric("Jam Tersibuk (rata-rata)", f"{peak_hour:02d}.00")

# Pertanyaan 1
st.header("Pertanyaan 1: Musim dan Cuaca vs Penyewaan Harian")
st.write(
    "Musim Fall paling ramai (rata-rata 5.644 per hari) dan Spring paling sepi "
    "(2.604 per hari). Cuaca Clear paling ramai (4.877 per hari), "
    "Light Rain/Snow paling sepi (1.803 per hari)."
)

season_order = ["Fall", "Summer", "Winter", "Spring"]
season_cnt = (
    day_filtered.groupby("season_label")["cnt"].mean().reindex(season_order)
)
weather_order = ["Clear", "Mist", "Light Rain/Snow"]
weather_cnt = (
    day_filtered.groupby("weather_label")["cnt"].mean().reindex(weather_order)
)

fig1, axes1 = plt.subplots(1, 2, figsize=(14, 5))
axes1[0].bar(
    season_cnt.index,
    season_cnt.values,
    color=["#2f7ab8", "#5aa9e6", "#8ecae6", "#bde0fe"],
)
axes1[0].set_title("Rata-rata Penyewaan Harian per Musim")
axes1[0].set_xlabel("Musim")
axes1[0].set_ylabel("Rata-rata cnt per hari")
for i, v in enumerate(season_cnt.values):
    axes1[0].text(i, v + 120, f"{v:,.0f}", ha="center")

axes1[1].bar(
    weather_cnt.index,
    weather_cnt.values,
    color=["#2a9d8f", "#8ab17d", "#e76f51"],
)
axes1[1].set_title("Rata-rata Penyewaan Harian per Cuaca")
axes1[1].set_xlabel("Cuaca")
axes1[1].set_ylabel("Rata-rata cnt per hari")
for i, v in enumerate(weather_cnt.values):
    axes1[1].text(i, v + 120, f"{v:,.0f}", ha="center")

plt.tight_layout()
st.pyplot(fig1)

# Pertanyaan 2
st.header("Pertanyaan 2: Pola Penyewaan per Jam")
st.write(
    "Pada hari kerja ada dua puncak tajam di pukul 08.00 dan 17.00 yang "
    "didominasi pengguna registered. Pada hari libur/weekend puncaknya "
    "tunggal di siang hari sekitar pukul 13.00 dan pengguna casual "
    "jauh lebih banyak."
)

hourly = hour_filtered.groupby(["workingday", "hr"])["cnt"].mean().unstack(0)
hourly.columns = ["Hari Libur/Weekend", "Hari Kerja"]
user_hourly = hour_filtered.groupby("hr")[["casual", "registered"]].mean()

fig2, axes2 = plt.subplots(1, 2, figsize=(14, 5))
sns.lineplot(data=hourly, ax=axes2[0], marker="o")
axes2[0].set_title("Rata-rata Penyewaan per Jam: Hari Kerja vs Libur")
axes2[0].set_xlabel("Jam (hr)")
axes2[0].set_ylabel("Rata-rata cnt per jam")
axes2[0].set_xticks(range(0, 24, 2))

sns.lineplot(data=user_hourly, ax=axes2[1], marker="o")
axes2[1].set_title("Rata-rata Penyewaan per Jam: Casual vs Registered")
axes2[1].set_xlabel("Jam (hr)")
axes2[1].set_ylabel("Rata-rata cnt per jam")
axes2[1].set_xticks(range(0, 24, 2))

plt.tight_layout()
st.pyplot(fig2)

# Analisis lanjutan
st.header("Analisis Lanjutan: Tren Bulanan")
monthly_cnt = day_filtered.groupby(["year", "mnth"])["cnt"].mean().unstack(0)
fig3, ax3 = plt.subplots(figsize=(10, 4))
monthly_cnt.plot(ax=ax3, marker="o")
ax3.set_title("Tren Rata-rata Penyewaan Harian per Bulan")
ax3.set_xlabel("Bulan")
ax3.set_ylabel("Rata-rata cnt per hari")
ax3.set_xticks(range(1, 13))
st.pyplot(fig3)
st.write(
    "Penyewaan naik di semua bulan dari 2011 ke 2012. Bulan tersibuk "
    "adalah Juni (rata-rata 5.772 per hari) dan September (5.767), "
    "sedangkan Januari paling sepi (2.176 per hari)."
)

st.header("Conclusion")
st.write(
    "- **Pertanyaan 1:** Musim dan cuaca berpengaruh besar. Fall (5.644/hari) "
    "dan cuaca Clear (4.877/hari) paling ramai; Spring (2.604/hari) dan "
    "Light Rain/Snow (1.803/hari) paling sepi.\n"
    "- **Pertanyaan 2:** Hari kerja berpuncak di 08.00 (477/jam) dan 17.00 "
    "(525/jam), didominasi registered. Hari libur berpuncak di 13.00 "
    "(373/jam) dengan casual jauh lebih banyak."
)
st.header("Rekomendasi Action Item")
st.write(
    "- Tambah stok dan redistribusi sepeda sebelum jam 08.00 dan 17.00 "
    "pada hari kerja, dan kurangi stok pada dini hari.\n"
    "- Siapkan stok lebih banyak menjelang musim Fall dan saat cuaca cerah.\n"
    "- Buat promo siang hari libur/weekend (10.00–15.00) untuk pengguna casual.\n"
    "- Dorong pengguna casual menjadi registered melalui paket langganan bulanan."
)
