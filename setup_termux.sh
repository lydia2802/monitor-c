#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Pegasus Lacak Nomor — Setup Script untuk Termux (Android)
# =============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║       PEGASUS LACAK NOMOR — Setup Termux Android        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# ---------------------------------------------------------------------------
# 0. Perbaiki mirror Termux (atasi SSL error dari mirror lama termux.net)
# ---------------------------------------------------------------------------
echo -e "${YELLOW}[0/6] Mengganti mirror ke Cloudflare (atasi SSL error)...${NC}"

SOURCES="$PREFIX/etc/apt/sources.list"
# Ganti ke mirror resmi Cloudflare Termux yang paling stabil
echo "deb https://packages-cf.termux.dev/apt/termux-main stable main" > "$SOURCES"
echo -e "${GREEN}[✓] Mirror diperbarui: packages-cf.termux.dev${NC}"

# Bersihkan cache apt yang mungkin korup
rm -f "$PREFIX/var/lib/apt/lists/"* 2>/dev/null || true

# ---------------------------------------------------------------------------
# 1. Update paket Termux
# ---------------------------------------------------------------------------
echo -e "${YELLOW}[1/6] Update daftar paket...${NC}"
if ! pkg update -y; then
    echo -e "${RED}[!] Update gagal. Coba ganti mirror lain:${NC}"
    echo "deb https://dl.kcubeterm.com stable main" > "$SOURCES"
    pkg update -y || {
        echo -e "${RED}[!] Semua mirror gagal. Periksa koneksi internet Anda.${NC}"
        exit 1
    }
fi

# ---------------------------------------------------------------------------
# 2. Pasang dependensi sistem
# ---------------------------------------------------------------------------
echo -e "${YELLOW}[2/6] Pasang Python & git...${NC}"
pkg install -y python git

# ---------------------------------------------------------------------------
# 3. Clone atau update repo
# ---------------------------------------------------------------------------
REPO_URL="https://github.com/sobri3195/Pegasus-Lacak-Nomor.git"
TARGET_DIR="$HOME/Pegasus-Lacak-Nomor"

if [ -d "$TARGET_DIR/.git" ]; then
    echo -e "${YELLOW}[3/6] Repo sudah ada — update...${NC}"
    cd "$TARGET_DIR"
    git pull origin main
else
    echo -e "${YELLOW}[3/6] Clone repo...${NC}"
    git clone "$REPO_URL" "$TARGET_DIR"
    cd "$TARGET_DIR"
fi

# ---------------------------------------------------------------------------
# 4. Pasang dependensi Python
# ---------------------------------------------------------------------------
echo -e "${YELLOW}[4/6] Pasang library Python...${NC}"
pip install --upgrade pip --quiet
pip install -r requirements-termux.txt

# ---------------------------------------------------------------------------
# 5. Buat api_config.py jika belum ada
# ---------------------------------------------------------------------------
echo -e "${YELLOW}[5/6] Konfigurasi awal...${NC}"

CONFIG_FILE="config/api_config.py"
if [ ! -f "$CONFIG_FILE" ]; then
    cp config/api_config.example.py "$CONFIG_FILE"
    echo -e "${GREEN}[✓] File konfigurasi dibuat: $CONFIG_FILE${NC}"
else
    echo -e "${GREEN}[✓] File konfigurasi sudah ada${NC}"
fi

# Buat folder exports dan data jika belum ada
mkdir -p exports data

# ---------------------------------------------------------------------------
# 6. Tes bisa jalan
# ---------------------------------------------------------------------------
echo -e "${YELLOW}[6/6] Verifikasi instalasi...${NC}"
if python -c "import requests, tqdm, colorama; print('OK')" 2>/dev/null | grep -q OK; then
    echo -e "${GREEN}[✓] Semua library berhasil terinstal${NC}"
else
    echo -e "${RED}[!] Ada library yang gagal. Coba: pip install requests tqdm colorama${NC}"
fi

# ---------------------------------------------------------------------------
# Selesai
# ---------------------------------------------------------------------------
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗"
echo "║              INSTALASI SELESAI!                         ║"
echo "╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Cara menjalankan:${NC}"
echo "  cd ~/Pegasus-Lacak-Nomor"
echo "  python main.py"
echo ""
echo -e "${YELLOW}Password default: Sobri${NC}"
echo ""
echo -e "${CYAN}Untuk mengaktifkan API tracking:${NC}"
echo "  nano config/api_config.py"
echo "  → set API_ENABLED = True"
echo "  → isi API_KEYS dan API_ENDPOINTS"
echo ""
