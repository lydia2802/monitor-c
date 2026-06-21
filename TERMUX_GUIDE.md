# Panduan Instalasi di Android via Termux

## Prasyarat

- Aplikasi **Termux** — download dari [F-Droid](https://f-droid.org/packages/com.termux/) (BUKAN dari Play Store, versi Play Store sudah tidak diupdate)
- Koneksi internet aktif
- Storage minimal 500 MB

---

## Instalasi Otomatis (Direkomendasikan)

> **Jika muncul error SSL / "Unable to locate package"**, jalankan langkah 1 dulu sebelum yang lain.

Jalankan perintah ini **satu per satu** di Termux:

```bash
# 1. WAJIB: Ganti mirror Termux ke Cloudflare (atasi SSL error mirror lama)
echo "deb https://packages-cf.termux.dev/apt/termux-main stable main" > $PREFIX/etc/apt/sources.list
pkg update -y

# 2. Pasang git dan python
pkg install -y git python

# 3. Clone repo
git clone https://github.com/sobri3195/Pegasus-Lacak-Nomor.git
cd Pegasus-Lacak-Nomor

# 4. Jalankan setup otomatis (mirror sudah otomatis diperbaiki di dalam script)
bash setup_termux.sh
```

---

## Instalasi Manual (Langkah per Langkah)

```bash
# WAJIB: Ganti mirror dulu (atasi SSL error)
echo "deb https://packages-cf.termux.dev/apt/termux-main stable main" > $PREFIX/etc/apt/sources.list
pkg update -y

# Pasang dependensi sistem
pkg install -y python git

# Clone repo
git clone https://github.com/sobri3195/Pegasus-Lacak-Nomor.git
cd Pegasus-Lacak-Nomor

# Pasang library Python
pip install -r requirements-termux.txt

# Buat konfigurasi
cp config/api_config.example.py config/api_config.py

# Buat folder yang dibutuhkan
mkdir -p exports data
```

---

## Menjalankan Aplikasi

```bash
cd ~/Pegasus-Lacak-Nomor
python main.py
```

**Password default:** `Sobri`

---

## Konfigurasi API (Opsional)

Untuk mengaktifkan real tracking, edit file konfigurasi:

```bash
nano config/api_config.py
```

Ubah baris berikut:

```python
API_ENABLED = True           # Aktifkan API
API_KEYS = {
    "primary": "API_KEY_ANDA_DI_SINI"
}
API_ENDPOINTS = {
    "phone_lookup": "https://url-api-anda.com/phone",
    "nik_lookup": "https://url-api-anda.com/nik"
}
```

Simpan dengan `Ctrl+O`, keluar dengan `Ctrl+X`.

---

## Fitur Opsional (Memerlukan Kompilasi)

Beberapa fitur advanced memerlukan library tambahan:

```bash
# Untuk grafik/chart (matplotlib)
pkg install -y python-numpy
pip install matplotlib

# Untuk machine learning (scikit-learn)
pip install scikit-learn

# Untuk peta geospasial (folium)
pip install folium

# Untuk API server (Flask)
pip install flask flask-cors

# Untuk laporan Excel
pip install openpyxl

# Untuk penjadwalan otomatis
pip install schedule
```

---

## Troubleshooting

### SSL Error / "Unable to locate package git/python" ⬅ ERROR PALING UMUM
```
SSL connection failed: error:0A000086:SSL routines::certificate verify failed
Error: Unable to locate package git
Error: Unable to locate package python
```
**Penyebab:** Mirror Termux lama (`termux.net`) sudah tidak valid.  
**Solusi:**
```bash
# Ganti ke mirror Cloudflare (mirror resmi & paling stabil)
echo "deb https://packages-cf.termux.dev/apt/termux-main stable main" > $PREFIX/etc/apt/sources.list
pkg update -y
pkg install -y git python
```

Jika masih gagal, coba mirror alternatif:
```bash
echo "deb https://dl.kcubeterm.com stable main" > $PREFIX/etc/apt/sources.list
pkg update -y
```

### `ModuleNotFoundError: No module named 'config.api_config'`
```bash
cp config/api_config.example.py config/api_config.py
```

### `pip: command not found`
```bash
pkg install python
```

### Karakter/warna tidak tampil dengan benar
```bash
export TERM=xterm-256color
python main.py
```

### `Permission denied` saat menjalankan setup_termux.sh
```bash
bash setup_termux.sh
```

### Update ke versi terbaru
```bash
cd ~/Pegasus-Lacak-Nomor
git pull origin main
pip install -r requirements-termux.txt
```

---

## Struktur Folder

```
Pegasus-Lacak-Nomor/
├── main.py                  # File utama — jalankan ini
├── setup_termux.sh          # Script instalasi Termux
├── requirements-termux.txt  # Library Python minimal
├── config/
│   ├── api_config.py        # Konfigurasi API (buat dari .example.py)
│   └── settings.py          # Pengaturan aplikasi
├── exports/                 # Hasil export disimpan di sini
└── data/                    # Database lokal
```

---

## Tips Penggunaan di Android

- Gunakan **gesture swipe dari kiri** di Termux untuk membuka panel session baru
- Tekan **Volume Down + C** untuk interrupt (sama dengan Ctrl+C)
- Tekan **Volume Down + D** untuk exit session (sama dengan Ctrl+D)
- Anda bisa buka **beberapa session** sekaligus dengan swipe dari kiri → New Session
- Untuk memperbesar teks: **pinch zoom** di layar Termux
