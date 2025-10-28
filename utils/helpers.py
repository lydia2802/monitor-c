import os
import sys
import json
import csv
from datetime import datetime
from colorama import Fore, Style
from config.settings import COLORS, EXPORT_DIR

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored(message, color_type="INFO"):
    """Print a colored message to the console."""
    color = getattr(Fore, COLORS.get(color_type, "WHITE").upper())
    print(f"{color}{message}{Style.RESET_ALL}")

def validate_input(target, valid_prefix, nik_length):
    """Validate phone number or NIK input."""
    if not target:
        print_colored("\n[!] Input tidak boleh kosong!", "ERROR")
        return False
        
    if not (target.startswith(valid_prefix) or len(target) == nik_length):
        print_colored("\n[!] Format nomor telepon atau NIK tidak valid!", "ERROR")
        return False
        
    return True

def format_timestamp():
    """Get current timestamp in formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def handle_exception(e):
    """Handle exceptions and print error message."""
    print_colored(f"\n[!] Terjadi kesalahan: {str(e)}", "ERROR")
    sys.exit(1)

def handle_keyboard_interrupt():
    """Handle keyboard interrupt (Ctrl+C)."""
    print_colored("\n\n[!] Program dihentikan oleh pengguna.", "WARNING")
    sys.exit(0)

def export_to_json(data, filename):
    """Export search result to JSON file."""
    ensure_export_dir()
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return filepath

def export_to_csv(data, filename):
    """Export search result to CSV file."""
    ensure_export_dir()
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Field', 'Value'])
        for key, value in data.items():
            writer.writerow([key, value])
    return filepath

def export_to_txt(data, filename):
    """Export search result to TXT file."""
    ensure_export_dir()
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("PEGASUS LACAK NOMOR - HASIL PENCARIAN\n")
        f.write("=" * 50 + "\n\n")
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
        f.write("\n" + "=" * 50 + "\n")
    return filepath

def ensure_export_dir():
    """Ensure export directory exists."""
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

def read_batch_file(filepath):
    """Read numbers from batch file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        return lines
    except FileNotFoundError:
        print_colored(f"\n[!] File {filepath} tidak ditemukan!", "ERROR")
        return []
    except Exception as e:
        print_colored(f"\n[!] Error membaca file: {str(e)}", "ERROR")
        return []

def calculate_statistics(history):
    """Calculate statistics from search history."""
    if not history:
        return {}
    
    total_searches = len(history)
    targets = [h['target'] for h in history]
    phone_numbers = sum(1 for t in targets if t.startswith('08'))
    niks = total_searches - phone_numbers
    
    return {
        'total_searches': total_searches,
        'phone_numbers': phone_numbers,
        'niks': niks,
        'first_search': history[0]['timestamp'] if history else None,
        'last_search': history[-1]['timestamp'] if history else None
    }
