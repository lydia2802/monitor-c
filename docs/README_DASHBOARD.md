# 🛡️ Lacak Nomor — Unified Monitoring Dashboard

Dokumen ini menjelaskan **dashboard monitoring terpadu** untuk Lacak Nomor: satu server yang menggabungkan REST API dan web UI, bisa diakses **online** lewat browser/link, sementara seluruh data pencarian, history, dan statistik tetap **tersimpan offline** di SQLite lokal (folder `data/`).

> Catatan: project ini adalah tool pelacak nomor telepon/NIK (CLI Python), bukan tool MITRE ATT&CK/spyware-scanner. Dokumen ini mendeskripsikan struktur repo yang sebenarnya.

## 📋 Komponen

| Komponen | Lokasi | Fungsi |
|---|---|---|
| CLI App | `main.py` (-> `pegasus/main.py`) | Menu interaktif terminal (pencarian, history, export, dll) |
| REST API + Web Dashboard | `pegasus/api/server.py`, `run_dashboard.py` | Server Flask: REST API (`/api/v1/...`) + halaman web (`/dashboard`) |
| Analytics Engine | `pegasus/analytics/dashboard.py` | Statistik real-time, trend, distribusi operator/gender dari SQLite |
| Anomaly Detection | `pegasus/ml/anomaly_detector.py` | Deteksi pola pencarian anomali |
| User & RBAC | `pegasus/managers/user_manager.py`, `pegasus/models/user.py` | Login multi-user dengan role (admin/operator/viewer/auditor) |
| Penyimpanan Offline | `data/*.db` (SQLite, di-generate otomatis) | History pencarian, user, cache — semua lokal, tidak perlu internet untuk dibaca ulang |

Seluruh kode aplikasi ada di package `pegasus/`; `main.py` dan `run_dashboard.py` di root hanyalah entry point tipis. Lihat bagian "Struktur Proyek" di [README utama](../README.md) untuk detail lengkap.

Hasil pencarian yang dilakukan lewat web dashboard otomatis tersimpan ke `data/app_data.db`, sama seperti pencarian lewat CLI — jadi tab History dan Analytics di dashboard akan menampilkan data yang sama.

## 🚀 Step-by-Step: Menjalankan Dashboard (Website/Server)

### 1. Persyaratan

- Python 3.9+
- pip

### 2. Clone & masuk ke folder project

```bash
git clone https://github.com/lydia2802/monitor-c.git
cd monitor-c
```

### 3. Buat virtual environment (opsional tapi disarankan)

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` sudah memasukkan `flask` dan `flask-cors` sebagai dependency wajib karena dashboard berjalan di atas Flask.

### 5. Konfigurasi API tracking (wajib)

Aplikasi memerlukan API eksternal atau database lokal aktif untuk menghasilkan data (mode simulasi sudah dihapus di v3.0).

```bash
cp pegasus/config/api_config.example.py pegasus/config/api_config.py
```

Edit `pegasus/config/api_config.py`:

- **Online (real API)**: set `API_ENABLED = True`, isi `API_KEYS` dan `API_ENDPOINTS` sesuai provider Anda.
- **Offline (database lokal)**: set `DATABASE_ENABLED = True`, lalu isi `data/local_database.db` dari sample data:

  ```bash
  python -c "from pegasus.utils.database_manager import init_database, import_from_json; init_database(); import_from_json('data/sample_database.json')"
  ```

  Anda bisa kombinasikan keduanya: API untuk data real-time, database lokal sebagai fallback offline.

### 6. Jalankan server dashboard

```bash
python run_dashboard.py
```

Opsi:

```bash
python run_dashboard.py --host 0.0.0.0 --port 5000   # default
python run_dashboard.py --host 127.0.0.1 --port 8080  # custom
```

Server akan menampilkan:

```
[*] Starting Unified Dashboard Server...
[*] Web Dashboard: http://127.0.0.1:5000/dashboard
[*] REST API Base: http://127.0.0.1:5000/api/v1
[*] Health Check: http://127.0.0.1:5000/api/v1/health
```

Alternatif: jalankan dari menu CLI (`python main.py` → menu **24. Start API Server**), atau langsung `python -m pegasus.api.server`.

### 7. Buka dashboard di browser

Buka link: **http://localhost:5000/dashboard**

Login dengan akun default:

```
Username: admin
Password: admin123
```

⚠️ Segera ganti password default setelah login pertama (lewat tab Users atau `UserManager.change_password`).

### 8. Pakai dashboard

- **Overview** — kartu statistik (total pencarian, success rate, phone vs NIK), trend 24 jam, distribusi operator, top lokasi.
- **Pencarian** — cari nomor telepon/NIK langsung dari browser; hasil otomatis tersimpan ke history.
- **History** — daftar seluruh pencarian (dari web maupun CLI).
- **Anomali** — laporan deteksi pola pencarian tidak wajar (ML).
- **Users** (khusus admin) — kelola user & role.

## 🌐 Mode Online vs 💾 Offline

- **Online**: server Flask listen di `0.0.0.0:5000` sehingga bisa diakses dari perangkat lain di jaringan yang sama (`http://<ip-server>:5000/dashboard`), atau di-deploy ke VPS/cloud agar bisa diakses lewat internet (gunakan reverse proxy + HTTPS, misalnya Nginx + Let's Encrypt, untuk deployment publik).
- **Offline**: semua data (history pencarian, user, cache) disimpan di file SQLite lokal di folder `data/` (`app_data.db`, `users.db`, `local_database.db`). File-file ini tidak ter-commit ke git (lihat `.gitignore`) karena berisi data sensitif — dashboard tetap bisa menampilkan data lama walau koneksi internet/API eksternal terputus, selama database lokal sudah pernah terisi.

## 🔌 Daftar REST API

Semua endpoint (kecuali `/api/v1/health` dan `/api/v1/auth/login`) butuh header `Authorization: Bearer <token>` yang didapat dari login.

| Method | Endpoint | Keterangan |
|---|---|---|
| GET | `/api/v1/health` | Cek status server (online/offline) |
| POST | `/api/v1/auth/login` | Login, mengembalikan token |
| POST | `/api/v1/search/phone` | Cari nomor telepon |
| POST | `/api/v1/search/nik` | Cari NIK |
| GET | `/api/v1/history` | Daftar history pencarian |
| GET | `/api/v1/analytics/stats` | Statistik real-time |
| GET | `/api/v1/analytics/trends` | Trend pencarian per jam |
| GET | `/api/v1/analytics/operators` | Distribusi operator |
| GET | `/api/v1/analytics/genders` | Distribusi gender |
| GET | `/api/v1/analytics/anomalies` | Laporan anomaly detection |
| GET/POST | `/api/v1/users` | List / buat user (admin only) |

## 🔧 Troubleshooting

- **`Flask not installed`** → jalankan `pip install flask flask-cors`.
- **Login gagal / "Default admin user created"** muncul tiap start → pastikan `data/users.db` tidak terhapus antar restart; admin default `admin/admin123` hanya dibuat sekali jika tabel users kosong.
- **Hasil pencarian kosong** → pastikan `pegasus/config/api_config.py` sudah ada dan `API_ENABLED` atau `DATABASE_ENABLED` bernilai `True`.
- **Dashboard kosong / statistik 0** → wajar untuk instalasi baru; lakukan minimal satu pencarian dari tab "Pencarian" agar `data/app_data.db` terisi.
- **Akses dari device lain di jaringan gagal** → pastikan firewall mengizinkan port 5000, dan jalankan dengan `--host 0.0.0.0`.

## ⚠️ Disclaimer

Tool ini dibuat untuk tujuan edukasi. Penggunaan untuk melacak nomor/NIK pihak lain tanpa izin yang sah dapat melanggar hukum privasi data. Pengguna bertanggung jawab penuh atas legalitas penggunaan.
