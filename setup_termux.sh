#!/data/data/com.termux/files/usr/bin/bash
# =============================================================================
# Pegasus Lacak Nomor — Setup Script untuk Termux (Android)
# =============================================================================

set -e

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
# 1. Update paket Termux
# ---------------------------------------------------------------------------
echo -e "${YELLOW}[1/5] Update paket Termux...${NC}"
pkg update -y && pkg upgrade -y

# ---------------------------------------------------------------------------
# 2. Pasang dependensi sistem
# ---------------------------------------------------------------------------
echo -e "${YELLOW}[2/5] Pasang Python & git...${NC}"
pkg install -y python git

# ---------------------------------------------------------------------------
# 3. Clone atau update repo
# ---------------------------------------------------------------------------
REPO_URL="https://github.com/sobri3195/Pegasus-Lacak-Nomor.git"
TARGET_DIR="$HOME/Pegasus-Lacak-Nomor"

if [ -d "$TARGET_DIR/.git" ]; then
    echo -e "${YELLOW}[3/5] Repo sudah ada — update...${NC}"
    cd "$TARGET_DIR"
    git pull origin main
else
    echo -e "${YELLOW}[3/5] Clone repo...${NC}"
    git clone "$REPO_URL" "$TARGET_DIR"
    cd "$TARGET_DIR"
fi

# ---------------------------------------------------------------------------
# 4. Pasang dependensi Python
# ---------------------------------------------------------------------------
echo -e "${YELLOW}[4/5] Pasang library Python...${NC}"
pip install --upgrade pip
pip install -r requirements-termux.txt

# ---------------------------------------------------------------------------
# 5. Buat api_config.py jika belum ada
# ---------------------------------------------------------------------------
echo -e "${YELLOW}[5/5] Konfigurasi awal...${NC}"

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
