"""
Analisis Regresi Logistik: Prediksi Jenis Kerusakan Reader Berdasarkan Total
Lalu Lintas (Tabel 5.3 & Tabel 5.4)

Variabel:
- total_lalu_lintas (X)  : total kendaraan yang melewati gerbang tol pada hari
                           terjadinya laporan kerusakan
- permasalahan (Y)       : 0 = "reader tidak bisa membaca", 1 = "reader error"
- tindakan               : 0 = pengecekan alat, 1 = pergantian suku cadang
                           (tidak dipakai sebagai prediktor pada model akhir)

Model: logit(P(permasalahan=1)) = beta0 + beta1 * total_lalu_lintas
"""
import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("../data/tabel_gabungan_regresi_logistik.csv")

X = df["total_lalu_lintas"]
X = sm.add_constant(X)
y = df["permasalahan"]

model = sm.Logit(y, X).fit()
print(model.summary())

# Odds ratio
print("\nOdds Ratio:")
print(pd.Series(model.params).apply(lambda b: pow(2.718281828, b)).rename("odds_ratio"))
