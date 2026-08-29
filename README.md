# Analisis Kerusakan Reader dalam Sistem Gardu Tol Otomatis (GTO)
### Pendekatan Data Mining untuk Pemeliharaan Proaktif — Ruas Tol Jakarta-Cikampek

> Proyek analisis data yang dikerjakan selama Praktik Kerja Lapangan (PKL) di
> **PT. Module Intracs Yasatama (Intracs)**, sebuah perusahaan penyedia sistem
> gardu tol di Indonesia. Proyek ini menggunakan data operasional lalu lintas
> harian serta log pemeliharaan/kerusakan alat untuk mengidentifikasi pola
> kerusakan pada *reader* (perangkat pembaca kartu e-Toll) di Gardu Tol
> Otomatis, dan merumuskan strategi pemeliharaan proaktif berbasis data.

---

## 1. Ringkasan

Gardu Tol Otomatis (GTO) mengandalkan komponen *reader* untuk membaca kartu
e-Toll saat kendaraan masuk/keluar gerbang. Ketika reader rusak, transaksi
tol terganggu dan berpotensi menimbulkan antrean panjang. Proyek ini
menganalisis data kerusakan reader pada tujuh gerbang tol di ruas
Jakarta-Cikampek selama periode **1–7 Februari 2024**, dengan tujuan:

1. Mengidentifikasi pola dan frekuensi kerusakan reader per gerbang tol.
2. Menguji apakah **volume lalu lintas harian** memengaruhi jenis/tingkat
   kerusakan yang terjadi, menggunakan **regresi logistik**.
3. Merangkum penyebab kerusakan yang paling umum menjadi rekomendasi
   **pemeliharaan proaktif** (predictive & preventive maintenance).

Data bersumber dari software internal perusahaan, **Settlement Monitoring
Tool**, yang mencatat lalu lintas kendaraan per gerbang serta laporan
pemeliharaan/kerusakan alat per shift.

---

## 2. Hasil

### 2.1 Frekuensi kerusakan reader per gerbang tol

Gerbang **Cikampek Utama** mencatat jumlah laporan kerusakan reader jauh
lebih tinggi (9 kejadian dalam 7 hari) dibanding gerbang lain, yang
kemungkinan berkaitan dengan volume lalu lintasnya yang tinggi sebagai
titik transisi utama ruas tol.

![Frekuensi Kerusakan per Gerbang Tol](images/regenerated_chart_frekuensi_kerusakan.png)

### 2.2 Volume lalu lintas vs. distribusi bank e-Toll per gerbang

Gerbang dengan volume lalu lintas tertinggi (Cikarang Utara, Cibitung 3)
juga menunjukkan proporsi transaksi Bank Mandiri yang dominan dibanding
BRI/BNI/BCA, konsisten dengan pangsa pasar kartu e-Toll di Indonesia.

![Lalu Lintas per Bank per Gerbang Tol](images/regenerated_chart_lalu_lintas_bank.png)

### 2.3 Regresi logistik: total lalu lintas sebagai prediktor jenis kerusakan

Model regresi logistik dibangun untuk memprediksi kategori permasalahan
(`0 = reader tidak bisa membaca`, `1 = reader error`) menggunakan
**total lalu lintas harian** pada gerbang terkait sebagai prediktor.

| | Koefisien | Odds Ratio |
|---|---|---|
| Intercept | −7,61 (laporan, Excel) / −3,04 (reproduksi, statsmodels) | 0,0005 |
| Total Lalu Lintas | 0,00011 (laporan) / 0,000033 (reproduksi) | ≈1,00 |

Lihat `code/03_regresi_logistik.py` untuk reproduksi lengkap.

---

## 3. Analisis

- **Total lalu lintas adalah prediktor yang relevan secara arah**, meskipun
  tingkat signifikansinya lemah (p-value > 0,1 baik pada perhitungan Excel
  di laporan asli maupun pada reproduksi dengan `statsmodels`). Artinya, ada
  indikasi bahwa gerbang dengan lalu lintas lebih padat cenderung mengalami
  jenis kerusakan "reader error" dibanding "reader tidak bisa membaca",
  namun jumlah observasi yang kecil (18 laporan dalam 7 hari) membuat
  interval kepercayaan sangat lebar sehingga kesimpulan ini **belum bisa
  digeneralisasi**.
- **Catatan reproduksi:** koefisien yang dihasilkan `statsmodels` pada
  proyek ini tidak identik dengan angka regresi berbasis Excel Add-in yang
  dilaporkan pada laporan PKL asli (arah dan kesimpulan tetap konsisten,
  namun magnitudonya berbeda). Ini kemungkinan disebabkan perbedaan metode
  solver/penskalaan antara Excel Regression Add-in dan MLE `statsmodels`.
  Disertakan apa adanya sebagai catatan transparansi, bukan untuk menutupi
  perbedaan tersebut.
- **Penyebab kerusakan paling umum**: kegagalan membaca kartu (SAM reader
  tidak terbaca, antena reader bermasalah) dan kegagalan daya (PSU/power
  supply), yang tersebar di hampir seluruh gerbang — bukan hanya di gerbang
  ber-volume tinggi.
- **Rekomendasi pemeliharaan proaktif** yang diusulkan: inspeksi rutin slot
  SAM dan antena, kalibrasi berkala, monitoring kondisi power supply secara
  real-time, serta penjadwalan penggantian suku cadang sebelum melewati
  estimasi masa pakainya — dijabarkan lengkap di laporan (Bab V.B).

**Keterbatasan utama** (diakui pada laporan asli): jumlah observasi kecil
(1 minggu data, 18 laporan) dan sebagian kesimpulan pemeliharaan proaktif
masih bersifat deskriptif/kualitatif, belum didukung data kuantitatif
penuh. Riset lanjutan dengan periode data yang lebih panjang akan
memperkuat validitas model.

---

## 4. Struktur Repository

```
.
├── README.md
├── code/
├── data/
├── images/
└── docs/
```

Penjelasan tiap folder dan file ada di bawah ini, diurutkan sesuai alur
kerja proyek: **data mentah → kode pengolahan → hasil visual → laporan
lengkap.**

### 4.1 `data/` — Dataset

| No | File | Isi |
|---|---|---|
| 1 | `tabel_pemeliharaan_kerusakan_reader.csv` | Log mentah laporan kerusakan reader per gerbang (tanggal, gerbang, nomor gardu, jenis permasalahan, tindakan perbaikan). Sumber untuk chart frekuensi kerusakan. Setara Tabel 5.1 pada laporan. |
| 2 | `tabel_lalu_lintas_per_bank.csv` | Rekap total lalu lintas kendaraan per gerbang, dipecah berdasarkan bank penerbit e-Toll (Mandiri, BRI, BNI, BCA). Setara Tabel 5.2. |
| 3 | `tabel_gabungan_regresi_logistik.csv` | Dataset gabungan (18 observasi) hasil konversi biner dari kategori "Permasalahan" dan "Tindakan", menjadi input model regresi logistik. Setara Tabel 5.3. |

### 4.2 `code/` — Skrip Python

| No | File | Fungsi | Input | Output |
|---|---|---|---|---|
| 1 | `01_chart_frekuensi_kerusakan.py` | Menghitung jumlah laporan kerusakan per gerbang dan menampilkannya sebagai bar chart. | `data/tabel_pemeliharaan_kerusakan_reader.csv` | `images/regenerated_chart_frekuensi_kerusakan.png` |
| 2 | `02_chart_lalu_lintas_bank.py` | Menggabungkan bar chart (total lalu lintas) dan line chart (lalu lintas per bank) dalam satu figur sumbu-ganda. | `data/tabel_lalu_lintas_per_bank.csv` | `images/regenerated_chart_lalu_lintas_bank.png` |
| 3 | `03_regresi_logistik.py` | Membangun model regresi logistik (`statsmodels`) untuk memprediksi kategori kerusakan dari total lalu lintas, lalu mencetak ringkasan koefisien & odds ratio. | `data/tabel_gabungan_regresi_logistik.csv` | Ringkasan model di terminal (lihat Bagian 2.3) |

Jalankan dari dalam folder `code/` (path relatif ke `../data` dan
`../images` sudah diatur di masing-masing skrip):
```bash
pip install pandas matplotlib statsmodels
python 01_chart_frekuensi_kerusakan.py
python 02_chart_lalu_lintas_bank.py
python 03_regresi_logistik.py
```

### 4.3 `images/` — Visualisasi & Dokumentasi

**Hasil reproduksi kode di atas** (untuk dibandingkan dengan versi asli):

| File | Keterangan |
|---|---|
| `regenerated_chart_frekuensi_kerusakan.png` | Output `01_chart_frekuensi_kerusakan.py` |
| `regenerated_chart_lalu_lintas_bank.png` | Output `02_chart_lalu_lintas_bank.py` |

**Hasil asli dari laporan** (dibuat dengan Google Colab & Excel saat PKL berlangsung):

| File | Keterangan |
|---|---|
| `original_chart_frekuensi_kerusakan.png` | Gambar 5.1 pada laporan — versi asli dari Google Colab |
| `original_chart_lalu_lintas_bank.png` | Gambar 5.2 pada laporan — versi asli dari Google Colab |
| `original_chart_trendline_regresi.png` | Gambar 5.3 — trendline hubungan "Permasalahan" & "Tindakan" (Microsoft Excel) |
| `original_tabel_regresi_excel.png` | Tabel 5.4 — output regresi logistik dari Excel Regression Add-in |
| `original_output_logit_python.png` | Output tambahan regresi logistik dari `statsmodels` yang dijalankan penulis di Google Colab pada laporan asli |

**Diagram metodologi:**

| File | Keterangan |
|---|---|
| `diagram_alir_metode_penelitian.png` | Alur kerja penelitian dari studi literatur hingga kesimpulan pemeliharaan (Gambar 3.10) |

**Foto alat & sistem GTO:**

| File | Keterangan |
|---|---|
| `alat_lts_gto.jpg` | Lighting and Traffic System (LTS), salah satu komponen GTO yang dirakit penulis |
| `reader_pada_gto.jpg` | Reader (perangkat pembaca kartu e-Toll) terpasang pada GTO |
| `nfc_tag_dan_reader.jpg` | Tag NFC dan modul reader — komponen inti teknologi pembacaan kartu e-Toll |
| `gardu_tol_otomatis.jpg` | Foto fisik Gardu Tol Otomatis (GTO) |
| `toll_fare_information.jpg` | Perangkat Toll Fare Information (TFI) — layar informasi tarif tol |
| `etoll_card.jpg` | Contoh kartu e-Toll dari berbagai bank penerbit |
| `peta_ruas_tol_jakarta_cikampek.jpg` | Peta ruas Tol Jakarta-Cikampek beserta titik gerbang tol |
| `settlement_monitoring_tool.jpg` | Tampilan software Settlement Monitoring Tool — sumber data proyek ini |

**Dokumentasi kegiatan PKL:**

| File | Keterangan |
|---|---|
| `penyolderan_keyboard.jpg` | Proses penyolderan komponen keyboard GTO |
| `dokumentasi_solder.jpg` | Dokumentasi tambahan proses perakitan/penyolderan alat |
| `dokumentasi_pengujian_layar.jpg` | Pengujian tampilan layar perangkat |
| `dokumentasi_pcb_akhir.jpg` | Hasil akhir papan PCB yang telah dirakit dan diuji |

> Catatan: foto pribadi penulis (wajah) dan gambar yang memuat data pribadi
> pihak ketiga (nilai kinerja karyawan, hasil tes psikologi kandidat) sengaja
> **tidak disertakan** di folder ini maupun di laporan PDF — lihat Bagian 6.

### 4.4 `docs/` — Laporan Lengkap

| File | Keterangan |
|---|---|
| `Laporan_PKL_Analisis_Kerusakan_Reader_GTO_clean.pdf` | Laporan akhir PKL lengkap (52 halaman): latar belakang, profil perusahaan, tinjauan pustaka, metodologi, hasil & pembahasan penuh, kesimpulan, daftar pustaka, serta lampiran data pendukung & dokumentasi. Halaman identitas pribadi dan data pihak ketiga telah dihilangkan (lihat Bagian 6). |

---

## 5. Skill yang Diterapkan

- **Data mining & statistik terapan**: regresi logistik untuk data biner,
  interpretasi odds ratio, evaluasi signifikansi (p-value, confidence
  interval).
- **Pengolahan data**: pembersihan & konversi data operasional mentah
  (format tool internal perusahaan) menjadi tabel terstruktur siap-analisis
  menggunakan Microsoft Excel.
- **Pemrograman Python untuk analisis data**: `pandas` (manipulasi data),
  `matplotlib` (visualisasi dual-axis & bar chart), `statsmodels`
  (pemodelan regresi logistik), dijalankan di Google Colab.
- **Fisika instrumentasi diterapkan pada industri**: pemahaman prinsip kerja
  sensor NFC/RFID pada reader, sistem kelistrikan (PSU, relay, MCB) pada
  perangkat GTO, dari pengalaman langsung merakit & menguji alat.
- **Komunikasi hasil analisis**: menyusun temuan teknis menjadi rekomendasi
  pemeliharaan proaktif yang dapat ditindaklanjuti oleh tim operasional.

---

## 6. Tentang Proyek Asli

- **Instansi**: PT. Module Intracs Yasatama (Intracs), Cikarang, Bekasi
- **Program Studi**: Fisika (Fisika Instrumentasi) — FMIPA, Universitas
  Negeri Jakarta
- **Periode PKL**: 12 Februari 2024 – 31 Juli 2024
- **Laporan lengkap**: lihat `docs/` — versi yang dipublikasikan di sini
  sudah dibersihkan dari halaman identitas pribadi (sampul, lembar
  pengesahan, biodata, tanda tangan) serta data pribadi pihak ketiga
  (data penilaian kinerja karyawan & hasil tes psikologi kandidat) yang
  awalnya ikut terlampir di laporan.

---

## Lisensi & Atribusi

Repository ini dibagikan untuk keperluan portofolio pembelajaran. Data
lalu lintas dan pemeliharaan berasal dari operasional PT. Module Intracs
Yasatama dan digunakan di sini hanya sebagai studi kasus akademik.
