# Pegasus Lacak Nomor v3.0 - Real Tracking Edition

Aplikasi Python untuk melacak nomor telepon dan NIK dengan **Real Tracking ONLY** menggunakan API eksternal dan database lokal.

## ⚠️ **IMPORTANT: Simulation Mode Removed**

**Simulation mode has been removed.** Application now operates in **Real Tracking Mode ONLY**.

See [SIMULATION_REMOVED.md](SIMULATION_REMOVED.md) for details.

## ✨ **Real Tracking Features**

Aplikasi mendukung **pelacakan real-time** dengan:
- 🌐 **API Integration** - Koneksi ke API eksternal untuk data real
- 💾 **Local Database** - Query data dari SQLite lokal
- 🔐 **Privacy Compliance** - Built-in disclaimer dan consent
- ⚡ **Rate Limiting** - Proteksi dari API overload
- 💰 **Caching** - Mengurangi API calls dengan smart caching
- ❌ **No Simulation** - Data real saja, tidak ada data dummy/fake

📖 **[Baca Panduan Lengkap Real Tracking](REAL_TRACKING_GUIDE.md)**

## 🚀 Fitur

### Fitur Utama
- 🔒 Password protection untuk keamanan
- 📱 Pencarian nomor telepon (08xxx) dan NIK
- 🌐 **Real Tracking** via API atau Database lokal
- ⏳ Progress bar dengan animasi loading
- 🎨 Interface berwarna dengan feedback visual
- 📊 Tampilan hasil yang informatif dan terstruktur
- ⚡ Performa cepat dan responsif

### Fitur v2.0
1. **📤 Export Hasil Pencarian** - Export hasil ke berbagai format (JSON, CSV, TXT)
2. **📜 History Pencarian** - Lihat history pencarian yang telah dilakukan
3. **📦 Pencarian Batch** - Cari multiple nomor sekaligus dari file
4. **📈 Statistik Dashboard** - Lihat statistik lengkap tentang pencarian
5. **🔄 Menu Interaktif** - Navigasi yang lebih mudah dengan menu pilihan

### 🆕 15 Fitur Baru v3.0
1. **🔍 Pencarian Berdasarkan Nama** - ~~Reverse lookup berdasarkan nama~~ (Disabled - requires API support)
2. **📍 Pencarian Berdasarkan Lokasi** - ~~Cari nomor berdasarkan kota/provinsi~~ (Disabled - requires API support)
3. **🔎 Filter History Advanced** - Filter by tanggal, lokasi, gender
4. **📊 Statistik Visual** - Chart ASCII untuk visualisasi data
5. **📱 Deteksi Operator** - Identifikasi Telkomsel, XL, Indosat, dll
6. **💳 Deteksi Tipe Kartu** - Prabayar atau Pascabayar
7. **📧 Email Generator** - Generate email dari nama
8. **🌐 Social Media Profiles** - Instagram, Facebook, Twitter, TikTok
9. **🎂 Kalkulator Umur** - Hitung umur dari tanggal lahir
10. **🗺️ Kalkulator Jarak** - Hitung jarak antar koordinat
11. **⭐ Kelola Favorit** - Simpan pencarian favorit
12. **🗑️ Hapus History** - Bersihkan history pencarian
13. **📝 Tambah Catatan** - Notes untuk setiap pencarian
14. **⚡ Mode Cepat** - Skip animasi untuk pencarian cepat
15. **📄 Laporan Lengkap** - Generate report profesional

📖 **Lihat dokumentasi lengkap di [NEW_FEATURES.md](NEW_FEATURES.md)**

## 📋 Persyaratan Sistem

- Python 3.7 atau lebih tinggi
- pip (Python package manager)
- Terminal/Command Prompt dengan dukungan ANSI colors

## 🛠️ Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/yourusername/pegasus-lacak-nomor.git
cd pegasus-lacak-nomor
```

2. Install dependencies yang diperlukan:
```bash
pip install -r requirements.txt
```

## 💻 Penggunaan

1. Jalankan program:
```bash
python main.py
```

2. Masukkan password aktivasi (default: Sobri)

3. Pilih menu yang diinginkan (v3.0):
   - **Menu 1**: Pencarian Tunggal - Cari satu nomor dengan opsi export
   - **Menu 2**: Pencarian Batch - Cari banyak nomor dari file batch_search.txt
   - **Menu 3**: Pencarian Berdasarkan Nama - Reverse lookup
   - **Menu 4**: Pencarian Berdasarkan Lokasi - Cari by kota/provinsi
   - **Menu 5**: Lihat History - Tampilkan semua pencarian
   - **Menu 6**: Filter History (Advanced) - Filter by tanggal/lokasi/gender
   - **Menu 7**: Lihat Statistik - Statistik pencarian
   - **Menu 8**: Statistik Visual (Chart) - Visualisasi dengan grafik
   - **Menu 9**: Kalkulator Jarak - Hitung jarak koordinat
   - **Menu 10**: Kelola Favorit - Simpan pencarian favorit
   - **Menu 11**: Hapus History - Bersihkan history
   - **Menu 12**: Tambah Catatan - Notes untuk pencarian
   - **Menu 13**: Mode Cepat (Toggle) - Skip animasi
   - **Menu 14**: Generate Laporan Lengkap - Report profesional
   - **Menu 15**: Info Operator - Lihat database operator
   - **Menu 0**: Keluar dari program

### Pencarian Batch

Untuk menggunakan fitur pencarian batch:

1. Buat file `batch_search.txt` di direktori root
2. Masukkan nomor telepon atau NIK, satu per baris
3. Pilih menu "Pencarian Batch" di program
4. Hasil dapat di-export ke format JSON

Contoh isi `batch_search.txt`:
```
081234567890
082345678901
1234567890123456
2345678901234567
```

### Export Hasil

Setelah melakukan pencarian tunggal, Anda dapat export hasil ke:
- **JSON**: Format terstruktur untuk integrasi dengan aplikasi lain
- **CSV**: Format spreadsheet untuk analisis data
- **TXT**: Format teks sederhana untuk dokumentasi

File hasil export akan tersimpan di folder `exports/`

## 📁 Struktur Proyek

```
pegasus-lacak-nomor/
├── config/
│   ├── settings.py           # Konfigurasi aplikasi
│   ├── api_config.py         # Konfigurasi API (not in git)
│   └── api_config.example.py # Template konfigurasi
├── data/
│   ├── local_database.db     # Database lokal (generated)
│   └── sample_database.json  # Sample data untuk import
├── utils/
│   ├── helpers.py            # Fungsi-fungsi pembantu
│   ├── api_client.py         # API & Database client
│   └── database_manager.py   # Database management
├── exports/                  # Folder untuk hasil export (auto-created)
├── main.py                   # File utama program
├── Pegasus-lacak-nomor.py    # DEPRECATED - shows message only
├── batch_search.txt          # File input untuk batch search
└── requirements.txt          # Daftar dependencies
```

## 🔧 Konfigurasi

File `config/settings.py` berisi pengaturan yang dapat disesuaikan:
- Password aktivasi
- Jumlah percobaan password maksimum
- Pengaturan tampilan
- Parameter pencarian
- Pengaturan warna
- Konfigurasi export dan batch
- Batas maksimal history

## 📝 Fitur Detail

### 1. Export Hasil Pencarian
Setelah pencarian, Anda dapat menyimpan hasil dalam 3 format berbeda. Setiap file memiliki timestamp untuk tracking.

### 2. History Pencarian
Program menyimpan hingga 50 pencarian terakhir. Anda dapat melihat:
- Target yang dicari
- Waktu pencarian
- Hasil pencarian singkat

### 3. Pencarian Batch
Ideal untuk mencari banyak nomor sekaligus:
- Baca dari file batch_search.txt
- Maksimal 100 nomor per batch
- Auto-export hasil ke JSON
- Progress tracking untuk setiap nomor

### 4. Statistik Dashboard
Menampilkan insight tentang penggunaan:
- Total pencarian
- Jumlah nomor telepon vs NIK
- Waktu pencarian pertama dan terakhir

### 5. Menu Interaktif
Interface menu yang user-friendly:
- Navigasi mudah dengan angka
- Validasi input
- Pesan error yang jelas

## 📝 Catatan Penting

- **Program memerlukan API atau Database untuk berfungsi**
- **Simulation mode telah dihapus** - lihat [SIMULATION_REMOVED.md](SIMULATION_REMOVED.md)
- Data yang ditampilkan adalah data real dari API/Database
- Jangan gunakan untuk tujuan ilegal
- Pastikan penggunaan sesuai dengan peraturan yang berlaku
- User bertanggung jawab penuh atas legalitas penggunaan

## 🤝 Kontribusi

Kontribusi selalu diterima! Silakan buat pull request atau laporkan issues.

## 📄 Lisensi

Created by: Letda Kes dr. Sobri

## 🙏 Ucapan Terima Kasih

- Telkomsel untuk inspirasi
- Komunitas Python Indonesia
- Semua kontributor

## ⚠️ Disclaimer

Program ini dibuat untuk tujuan edukasi dan demonstrasi. Penggunaan untuk tujuan ilegal adalah tanggung jawab pengguna.

## 📝 Changelog

### v3.0 - Simulation Removal Update
- ⚠️ **BREAKING:** Simulation mode completely removed
- ⚠️ **BREAKING:** Application requires API or Database to function
- ❌ Removed: `generate_random_data()`, `simulate_search()`, `sample_data.py`
- ❌ Removed: `USE_FALLBACK_DATA` configuration option
- ❌ Disabled: Search by name (requires API support)
- ❌ Disabled: Search by location (requires API support)
- ✨ Pencarian berdasarkan nama ~~(disabled)~~
- ✨ Pencarian berdasarkan lokasi ~~(disabled)~~
- ✨ Filter history advanced (tanggal, lokasi, gender)
- ✨ Statistik visual dengan chart ASCII
- ✨ Deteksi operator telepon otomatis
- ✨ Deteksi tipe kartu (prabayar/pascabayar)
- ✨ Email generator dari nama
- ✨ Social media profiles generator (4 platform)
- ✨ Kalkulator umur otomatis
- ✨ Kalkulator jarak koordinat (Haversine)
- ✨ Sistem favorit/bookmark pencarian
- ✨ Hapus history dengan konfirmasi
- ✨ Tambah catatan ke pencarian
- ✨ Mode cepat untuk skip animasi
- ✨ Generate laporan lengkap profesional
- ✨ Info operator dengan database lengkap
- 🎨 Enhanced data output dengan lebih banyak informasi
- 📚 Dokumentasi lengkap untuk semua fitur

### v2.0
- ✨ Fitur export hasil (JSON, CSV, TXT)
- ✨ History pencarian dengan display interaktif
- ✨ Pencarian batch dari file
- ✨ Statistik dashboard
- ✨ Menu navigasi interaktif
- 🐛 Fixed missing sys import
- 🎨 Improved UI/UX
