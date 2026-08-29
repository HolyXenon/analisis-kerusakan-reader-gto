"""
Chart: Frekuensi Kerusakan Reader per Gerbang Tol (Gambar 5.1)
Ruas Jakarta-Cikampek, 1-7 Februari 2024

Menghitung jumlah laporan kerusakan reader per gerbang tol dari data
pemeliharaan mentah, lalu memvisualisasikannya sebagai bar chart.
"""
import pandas as pd
import matplotlib.pyplot as plt

# Data mentah pemeliharaan & kerusakan (lihat data/tabel_pemeliharaan_kerusakan_reader.csv)
df_raw = pd.read_csv("../data/tabel_pemeliharaan_kerusakan_reader.csv")

# Hitung frekuensi kerusakan per gerbang tol
freq = df_raw.groupby("gerbang")["permasalahan"].count().reset_index()
freq.columns = ["Gerbang Tol", "Frekuensi Kerusakan"]

df = pd.DataFrame(freq)

plt.figure(figsize=(10, 6))
plt.bar(df["Gerbang Tol"], df["Frekuensi Kerusakan"], color="skyblue")
plt.title("Frekuensi Kerusakan di Gerbang Tol")
plt.xlabel("Gerbang Tol")
plt.ylabel("Frekuensi Kerusakan")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("../images/regenerated_chart_frekuensi_kerusakan.png", dpi=150)
plt.show()
