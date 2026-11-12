# Proyek Analisis Data: Bike Sharing Dataset

Analisis penyewaan sepeda Capital Bikeshare, Washington D.C., 2011–2012.

## Pertanyaan Bisnis

1. Bagaimana pengaruh musim (season) dan kondisi cuaca (weathersit) terhadap total penyewaan sepeda harian di Washington D.C. selama periode 2011–2012?
2. Bagaimana pola penyewaan sepeda per jam pada hari kerja dibandingkan hari libur selama 2011–2012, dan bagaimana perbedaan kontribusi pengguna casual dan registered pada jam-jam sibuk tersebut?

## Struktur Folder

```
submission
├── dashboard
│   ├── main_data.csv    # data harian bersih (day_df hasil cleaning)
│   ├── hour_data.csv    # data per jam bersih (hour_df hasil cleaning, untuk Pertanyaan 2)
│   └── dashboard.py     # aplikasi Streamlit
├── data
│   ├── day.csv          # dataset asli, agregasi harian
│   └── hour.csv         # dataset asli, agregasi per jam
├── notebook.ipynb       # notebook analisis (template Dicoding, sudah dijalankan)
├── README.md
└── requirements.txt
```

## Cara Menjalankan Dashboard

1. Buat dan aktifkan virtual environment (disarankan), lalu install dependensi:

```
pip install -r requirements.txt
```

2. Dari dalam folder `dashboard`, jalankan:

```
streamlit run dashboard.py
```

3. Buka alamat yang ditampilkan di terminal, biasanya `http://localhost:8501`.

Catatan: `dashboard.py` membaca `main_data.csv` dan `hour_data.csv` dari folder yang sama dengan file tersebut, jadi jalankan dari dalam folder `dashboard`.
