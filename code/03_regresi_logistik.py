"""
Regresi Logistik: Memprediksi Jenis Tindakan Perbaikan Reader GTO
Berdasarkan Total Lalu Lintas Gerbang & Kategori Permasalahan

Variabel:
- total_lalu_lintas (X1) : total lalu lintas mingguan pada gerbang tempat
                           insiden kerusakan tercatat (lihat catatan
                           keterbatasan di README)
- permasalahan (X2)      : 0 = "reader tidak bisa membaca", 1 = "reader error"
- tindakan (Y, target)   : 0 = pengecekan alat, 1 = pergantian suku cadang

Model: logit(P(tindakan=1)) = beta0 + beta1*total_lalu_lintas + beta2*permasalahan
"""
import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("../data/tabel_gabungan_regresi_logistik.csv")

X = df[["total_lalu_lintas", "permasalahan"]]
X = sm.add_constant(X)
y = df["tindakan"]

model = sm.Logit(y, X).fit()
print(model.summary())

print("\nOdds Ratio:")
print(model.params.apply(lambda b: pow(2.718281828, b)).rename("odds_ratio"))

# --- Diagnostik tambahan: cek granularitas variabel total_lalu_lintas ---
print("\nJumlah nilai unik total_lalu_lintas:", df["total_lalu_lintas"].nunique(),
      "dari", len(df), "observasi (lihat README bagian Keterbatasan Data)")
