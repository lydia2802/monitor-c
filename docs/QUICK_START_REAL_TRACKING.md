# Quick Start - Real Tracking

Panduan cepat untuk memulai menggunakan fitur Real Tracking di Pegasus Lacak Nomor v3.0.

## 📋 Pilihan Mode

Aplikasi ini memiliki 3 mode operasi:

### 1. 🎮 **Mode Simulasi** (Default - Tanpa Setup)
Data acak untuk testing dan demo. Tidak perlu setup apapun.

### 2. 🌐 **Mode Real Tracking dengan API**
Koneksi ke API eksternal untuk data real-time. Perlu API key.

### 3. 💾 **Mode Database Lokal**
Query data dari database SQLite lokal. Untuk data yang Anda miliki sendiri.

---

## 🚀 Option 1: Mode Simulasi (Paling Mudah)

### Install & Run

```bash
# 1. Clone atau download repository
cd /path/to/pegasus-lacak-nomor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Jalankan aplikasi
python main.py

# 4. Masukkan password: Sobri

# 5. Pilih menu: 1 (Pencarian Tunggal)

# 6. Masukkan nomor test: 081234567890
```

**Selesai!** Aplikasi akan menampilkan data simulasi.

### Konfigurasi (Optional)

Tidak perlu konfigurasi. Aplikasi sudah siap pakai dengan mode simulasi.

---

## 🌐 Option 2: Mode Real Tracking dengan API

### Prerequisites

- ✅ Akun API provider (Truecaller, Numverify, atau custom)
- ✅ API Key valid
- ✅ Internet connection

### Setup (5 Menit)

#### Step 1: Copy Configuration

```bash
cd config
cp api_config.example.py api_config.py
```

#### Step 2: Edit Konfigurasi

Edit `pegasus/config/api_config.py`:

```python
# Aktifkan Real Tracking
API_ENABLED = True

# Masukkan API Key Anda
API_KEYS = {
    "primary": "YOUR_API_KEY_HERE",  # ← Ganti dengan API key Anda
}

# Set API Endpoints
API_ENDPOINTS = {
    "phone_lookup": "https://your-api.com/v1/phone",
    "nik_lookup": "https://your-api.com/v1/nik",
}
```

#### Step 3: Test Connection

```bash
# Test import
python -c "from pegasus.utils.api_client import APIClient; print('OK')"

# Run test suite
python test_real_tracking.py
```

#### Step 4: Run Aplikasi

```bash
python main.py
```

Aplikasi akan menampilkan:
```
╔════════════════════════════════════════════════════════════════════╗
║                   PEGASUS LACAK NOMOR v3.0                        ║
║                 [REAL TRACKING MODE]                              ║
╚════════════════════════════════════════════════════════════════════╝

[!] DISCLAIMER & PRIVACY
...
Lanjutkan? (yes/no): yes
```

### Contoh API Providers

#### Numverify (Recommended untuk Pemula)

```python
# FREE tier: 250 requests/month
API_ENDPOINTS = {
    "phone_lookup": "http://apilayer.net/api/validate",
}
API_KEYS = {
    "primary": "YOUR_NUMVERIFY_KEY"
}
```

Daftar di: https://numverify.com/

#### Custom API (Self-hosted)

```python
API_ENDPOINTS = {
    "phone_lookup": "http://localhost:5000/api/phone",
}
API_KEYS = {
    "primary": "your_secret_key"
}
```

---

## 💾 Option 3: Mode Database Lokal

Untuk menggunakan data yang Anda miliki sendiri.

### Setup (10 Menit)

#### Step 1: Enable Database

Edit `pegasus/config/api_config.py`:

```python
DATABASE_ENABLED = True
DATABASE_PATH = "data/local_database.db"
```

#### Step 2: Initialize Database

```bash
python utils/database_manager.py

# Pilih: 1. Initialize Database
```

#### Step 3: Import Data

##### Option A: Import dari JSON

Buat file JSON (contoh: `my_data.json`):

```json
[
  {
    "phone_number": "081234567890",
    "name": "John Doe",
    "address": "Jl. Sudirman No. 123",
    "city": "Jakarta",
    "province": "DKI Jakarta",
    "operator": "Telkomsel"
  }
]
```

Import:

```bash
python utils/database_manager.py

# Pilih: 2. Import from JSON
# Enter: my_data.json
```

##### Option B: Import dari CSV

Buat file CSV dengan header:
```
phone_number,name,address,city,province,operator
081234567890,John Doe,Jl. Sudirman No. 123,Jakarta,DKI Jakarta,Telkomsel
```

Import:

```bash
python utils/database_manager.py

# Pilih: 3. Import from CSV
# Enter: my_data.csv
```

#### Step 4: Verify Data

```bash
python utils/database_manager.py

# Pilih: 6. List All Records
```

#### Step 5: Run Aplikasi

```bash
python main.py

# Sekarang aplikasi akan query database lokal Anda
```

---

## 🔧 Troubleshooting

### API Key Error

```
[!] API authentication failed. Check your API key.
```

**Solusi:**
1. Verifikasi API key valid
2. Cek API_KEYS di `pegasus/config/api_config.py`
3. Pastikan tidak ada spasi extra

### Connection Timeout

```
[!] Request timeout
```

**Solusi:**
1. Cek internet connection
2. Verifikasi endpoint URL benar
3. Increase timeout: `API_TIMEOUT = 20` di config

### No Results from API

```
[!] No results from API or database
[i] Using fallback simulation data
```

**Ini normal jika:**
- Nomor tidak ada di database API
- API limit reached
- Fallback otomatis ke simulasi

**Solusi:**
- Cek API quota/limit
- Verifikasi nomor valid di provider

### Module Not Found

```
ModuleNotFoundError: No module named 'requests'
```

**Solusi:**
```bash
pip install -r requirements.txt
```

---

## 💡 Tips & Tricks

### 1. Quick Mode untuk Testing

```bash
# Dalam aplikasi
Menu → 13. Mode Cepat (Toggle)

# Skip animasi, lebih cepat
```

### 2. Batch Processing

```bash
# Buat file: batch_search.txt
081234567890
082198765432
085612345678

# Dalam aplikasi
Menu → 2. Pencarian Batch

# Process semua nomor sekaligus
```

### 3. Kombinasi Mode

Gunakan database + API + fallback:

```python
DATABASE_ENABLED = True     # Cek database dulu
API_ENABLED = True          # Kalau tidak ada, cek API
USE_FALLBACK_DATA = True    # Kalau semua gagal, simulasi
```

Priority: **Cache → Database → API → Simulation**

### 4. Cost Optimization

Untuk mengurangi biaya API:

```python
CACHE_RESULTS = True         # Enable caching
CACHE_DURATION = 7200        # Cache 2 jam
DATABASE_ENABLED = True      # Store frequently used data
RATE_LIMIT_ENABLED = True    # Prevent overuse
MAX_REQUESTS_PER_MINUTE = 5  # Lower limit
```

### 5. Export Results

```bash
# Setelah search
[?] Export hasil? (y/n): y

# Pilih format
1. JSON  → For APIs & data processing
2. CSV   → For Excel/spreadsheet
3. TXT   → For reports

# File akan disimpan di folder: exports/
```

---

## 📊 Next Steps

### Setelah Basic Setup

1. **Explore Features**
   ```bash
   # Try all 15 features
   Menu → Explore each option
   ```

2. **Customize Settings**
   ```bash
   # Edit: pegasus/config/api_config.py
   # Edit: pegasus/config/settings.py
   ```

3. **Read Full Documentation**
   - [REAL_TRACKING_GUIDE.md](REAL_TRACKING_GUIDE.md) - Panduan lengkap
   - [API_INTEGRATION.md](API_INTEGRATION.md) - API details
   - [NEW_FEATURES.md](NEW_FEATURES.md) - Semua fitur

4. **Build Your Database**
   ```bash
   # Collect your data
   # Import ke database
   # Query super cepat!
   ```

---

## ⚖️ Legal Notice

**PENTING:**

✅ **DO:**
- Gunakan untuk data yang Anda miliki
- Verifikasi identitas dengan consent
- Testing & development
- Legal investigation dengan warrant
- Research dengan approval

❌ **DON'T:**
- Stalking atau harassment
- Tracking tanpa izin
- Pelanggaran privasi
- Commercial reselling tanpa license
- Bypass security/authentication

**Anda bertanggung jawab penuh** atas penggunaan aplikasi ini.  
Patuhi UU No. 27 Tahun 2022 tentang Perlindungan Data Pribadi.

---

## 🆘 Need Help?

### Documentation
- 📖 [README.md](README.md) - Overview
- 🔐 [REAL_TRACKING_GUIDE.md](REAL_TRACKING_GUIDE.md) - Detailed guide
- 🔌 [API_INTEGRATION.md](API_INTEGRATION.md) - API integration
- ✨ [NEW_FEATURES.md](NEW_FEATURES.md) - Feature list

### Testing
```bash
# Run test suite
python test_real_tracking.py

# Test specific component
python -c "from pegasus.utils.api_client import APIClient; c = APIClient(); print('OK')"
```

### Support
- GitHub Issues: [Report bugs]
- Email: support@example.com

---

## 🎉 Ready to Go!

Pilih mode yang sesuai kebutuhan Anda:

1. **Baru mulai?** → Gunakan Mode Simulasi
2. **Punya API?** → Setup Real Tracking dengan API
3. **Punya data sendiri?** → Setup Database Lokal

Semua mode bisa dikombinasikan untuk hasil terbaik!

---

**Happy Tracking! 🚀**

*Created by: Letda Kes dr. Sobri*  
*Version: 3.0 - Real Tracking Edition*
