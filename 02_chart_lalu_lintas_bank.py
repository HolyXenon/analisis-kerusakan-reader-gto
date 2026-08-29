"""
Chart: Total Lalu Lintas dan Lalu Lintas Per Bank di Setiap Gerbang Tol (Gambar 5.2)
Ruas Jakarta-Cikampek, Februari 2024

Menggabungkan bar chart (total lalu lintas) dengan line chart (lalu lintas
per bank e-toll: Mandiri, BRI, BNI, BCA) pada sumbu ganda.
"""
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../data/tabel_lalu_lintas_per_bank.csv")

fig, ax1 = plt.subplots(figsize=(14, 7))

color = "skyblue"
ax1.set_xlabel("Gerbang Tol")
ax1.set_ylabel("Total Lalu Lintas", color=color)
ax1.bar(df["gerbang_tol"], df["total_lalu_lintas"], color=color, label="Total Lalu Lintas")
ax1.tick_params(axis="y", labelcolor=color)

ax2 = ax1.twinx()
ax2.set_ylabel("Lalu Lintas Per Bank")
colors = ["red", "green", "blue", "purple"]
for bank, c in zip(["mandiri", "bri", "bni", "bca"], colors):
    ax2.plot(df["gerbang_tol"], df[bank], marker="o", label=bank.upper(), color=c)
ax2.tick_params(axis="y")

fig.tight_layout()
fig.suptitle("Total Lalu Lintas dan Lalu Lintas Per Bank di Setiap Gerbang Tol", y=1.02)
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))

plt.xticks(rotation=45)
plt.savefig("../images/regenerated_chart_lalu_lintas_bank.png", dpi=150, bbox_inches="tight")
plt.show()
