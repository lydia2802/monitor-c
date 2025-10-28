import sys
import time
import random
from tqdm import tqdm
from colorama import init, Fore, Style

from config.settings import (
    ACTIVATION_PASSWORD, MAX_PASSWORD_ATTEMPTS,
    PROGRESS_BAR_WIDTH, LOADING_ANIMATION_DURATION,
    LOADING_ANIMATION_ITERATIONS, VALID_PHONE_PREFIX,
    NIK_LENGTH, LATITUDE_RANGE, LONGITUDE_RANGE,
    BIRTH_YEAR_RANGE, MAX_HISTORY_ITEMS, BATCH_INPUT_FILE,
    MAX_BATCH_SIZE
)
from data.sample_data import (
    NAMES, STREETS, CITIES, PROVINCES,
    POSTAL_CODES, GENDERS
)
from utils.helpers import (
    clear_screen, print_colored, validate_input,
    format_timestamp, handle_exception, handle_keyboard_interrupt,
    export_to_json, export_to_csv, export_to_txt,
    read_batch_file, calculate_statistics
)

# Initialize colorama
init()

# Global search history
search_history = []

def print_banner():
    """Print the application banner."""
    banner = f"""
    {Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════╗
    ║                         PEGASUS LACAK NOMOR v2.0                          ║
    ║                     Created by: Letda Kes dr. Sobri                       ║
    ╚════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def check_password():
    """Check activation password."""
    attempts = 0
    
    while attempts < MAX_PASSWORD_ATTEMPTS:
        password = input(f"\n{Fore.YELLOW}[!] Masukkan Password Aktivasi: {Style.RESET_ALL}")
        if password == ACTIVATION_PASSWORD:
            print_colored("[✓] Password benar!", "SUCCESS")
            time.sleep(1)
            return True
        attempts += 1
        if attempts < MAX_PASSWORD_ATTEMPTS:
            print_colored(f"\n[!] Password salah! Sisa percobaan: {MAX_PASSWORD_ATTEMPTS - attempts}", "ERROR")
        else:
            print_colored("\n[!] Maksimal percobaan terlampaui. Program berhenti.", "ERROR")
            sys.exit(1)
    return False

def loading_animation():
    """Show loading animation."""
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for _ in range(LOADING_ANIMATION_ITERATIONS):
        for char in chars:
            sys.stdout.write(f"\r{Fore.CYAN}[{char}] Loading...{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(LOADING_ANIMATION_DURATION)
    print("\r" + " " * 50 + "\r", end="")

def simulate_search():
    """Simulate search process with progress bar."""
    print_colored("\n[INFO] Processing Target Data...", "INFO")
    loading_animation()
    for _ in tqdm(range(100), desc="Search Data", 
                 bar_format="{l_bar}█{bar}█{r_bar}",
                 colour="cyan", ncols=PROGRESS_BAR_WIDTH):
        time.sleep(0.03)

def generate_random_data():
    """Generate random data for demonstration."""
    return {
        "Nama": random.choice(NAMES),
        "Jenis Kelamin": random.choice(GENDERS),
        "Birthday": f"{random.randint(*BIRTH_YEAR_RANGE)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
        "Jalan": random.choice(STREETS),
        "Kota/Town": random.choice(CITIES),
        "Provinsi": random.choice(PROVINCES),
        "Kode Pos": random.choice(POSTAL_CODES),
        "Negara": "Indonesia",
        "Latitude": f"{random.uniform(*LATITUDE_RANGE):.6f}",
        "Longitude": f"{random.uniform(*LONGITUDE_RANGE):.6f}",
        "Waktu Pencarian": format_timestamp()
    }

def display_result(data):
    """Display search results."""
    print_colored("\nResult:", "SUCCESS")
    for key, value in data.items():
        if key == "Waktu Pencarian":
            print_colored(f"{key}: {value}", "WARNING")
        else:
            print_colored(f"{key}: {value}", "INFO")
    print_colored("\n[✔] Search Data complete!", "SUCCESS")

def add_to_history(target, result):
    """Add search to history."""
    global search_history
    if len(search_history) >= MAX_HISTORY_ITEMS:
        search_history.pop(0)
    
    history_entry = {
        'target': target,
        'timestamp': format_timestamp(),
        'result': result
    }
    search_history.append(history_entry)

def show_history():
    """Display search history."""
    if not search_history:
        print_colored("\n[!] History kosong. Belum ada pencarian yang dilakukan.", "WARNING")
        return
    
    print_colored(f"\n{'='*70}", "INFO")
    print_colored("HISTORY PENCARIAN", "SUCCESS")
    print_colored(f"{'='*70}", "INFO")
    
    for i, entry in enumerate(search_history, 1):
        print_colored(f"\n[{i}] Target: {entry['target']}", "INFO")
        print_colored(f"    Waktu: {entry['timestamp']}", "WARNING")
        print_colored(f"    Nama: {entry['result']['Nama']}", "INFO")
        print_colored(f"    Kota: {entry['result']['Kota/Town']}", "INFO")
    
    print_colored(f"\n{'='*70}", "INFO")
    print_colored(f"Total: {len(search_history)} pencarian", "SUCCESS")

def show_statistics():
    """Display search statistics."""
    stats = calculate_statistics(search_history)
    
    if not stats:
        print_colored("\n[!] Belum ada data untuk statistik.", "WARNING")
        return
    
    print_colored(f"\n{'='*70}", "INFO")
    print_colored("STATISTIK PENCARIAN", "SUCCESS")
    print_colored(f"{'='*70}", "INFO")
    print_colored(f"Total Pencarian: {stats['total_searches']}", "INFO")
    print_colored(f"Nomor Telepon: {stats['phone_numbers']}", "INFO")
    print_colored(f"NIK: {stats['niks']}", "INFO")
    if stats['first_search']:
        print_colored(f"Pencarian Pertama: {stats['first_search']}", "WARNING")
    if stats['last_search']:
        print_colored(f"Pencarian Terakhir: {stats['last_search']}", "WARNING")
    print_colored(f"{'='*70}", "INFO")

def export_result(data, target):
    """Export search result to file."""
    print_colored("\n[?] Pilih format export:", "INFO")
    print("1. JSON")
    print("2. CSV")
    print("3. TXT")
    print("4. Batal")
    
    choice = input(f"\n{Fore.YELLOW}Pilih (1-4): {Style.RESET_ALL}")
    
    timestamp = format_timestamp().replace(' ', '_').replace(':', '-')
    filename_base = f"result_{target}_{timestamp}"
    
    try:
        if choice == '1':
            filepath = export_to_json(data, f"{filename_base}.json")
            print_colored(f"\n[✓] Data berhasil diexport ke: {filepath}", "SUCCESS")
        elif choice == '2':
            filepath = export_to_csv(data, f"{filename_base}.csv")
            print_colored(f"\n[✓] Data berhasil diexport ke: {filepath}", "SUCCESS")
        elif choice == '3':
            filepath = export_to_txt(data, f"{filename_base}.txt")
            print_colored(f"\n[✓] Data berhasil diexport ke: {filepath}", "SUCCESS")
        elif choice == '4':
            print_colored("\n[!] Export dibatalkan.", "WARNING")
        else:
            print_colored("\n[!] Pilihan tidak valid.", "ERROR")
    except Exception as e:
        print_colored(f"\n[!] Error saat export: {str(e)}", "ERROR")

def batch_search():
    """Search multiple numbers from file."""
    print_colored(f"\n[INFO] Membaca file batch: {BATCH_INPUT_FILE}", "INFO")
    numbers = read_batch_file(BATCH_INPUT_FILE)
    
    if not numbers:
        print_colored("\n[!] Tidak ada nomor untuk dicari. Buat file batch_search.txt dengan nomor per baris.", "WARNING")
        time.sleep(3)
        return
    
    if len(numbers) > MAX_BATCH_SIZE:
        print_colored(f"\n[!] Jumlah nomor melebihi batas maksimal ({MAX_BATCH_SIZE}). Hanya {MAX_BATCH_SIZE} yang akan diproses.", "WARNING")
        numbers = numbers[:MAX_BATCH_SIZE]
    
    print_colored(f"\n[INFO] Ditemukan {len(numbers)} nomor untuk dicari.", "INFO")
    time.sleep(1)
    
    results = []
    for i, target in enumerate(numbers, 1):
        print_colored(f"\n[{i}/{len(numbers)}] Mencari: {target}", "INFO")
        
        if not validate_input(target, VALID_PHONE_PREFIX, NIK_LENGTH):
            print_colored(f"[!] Melewati nomor tidak valid: {target}", "ERROR")
            continue
        
        simulate_search()
        result = generate_random_data()
        result['Target'] = target
        results.append(result)
        add_to_history(target, result)
        display_result(result)
        time.sleep(0.5)
    
    print_colored(f"\n[✓] Batch search selesai! {len(results)}/{len(numbers)} berhasil.", "SUCCESS")
    
    if results:
        choice = input(f"\n{Fore.YELLOW}[?] Export semua hasil? (y/n): {Style.RESET_ALL}")
        if choice.lower() == 'y':
            timestamp = format_timestamp().replace(' ', '_').replace(':', '-')
            filepath = export_to_json(results, f"batch_results_{timestamp}.json")
            print_colored(f"\n[✓] Semua hasil diexport ke: {filepath}", "SUCCESS")

def show_menu():
    """Display main menu."""
    print_colored(f"\n{'='*70}", "INFO")
    print_colored("MENU UTAMA", "SUCCESS")
    print_colored(f"{'='*70}", "INFO")
    print("1. Pencarian Tunggal")
    print("2. Pencarian Batch (dari file)")
    print("3. Lihat History")
    print("4. Lihat Statistik")
    print("5. Keluar")
    print_colored(f"{'='*70}", "INFO")

def single_search():
    """Perform single search."""
    target = input(f"\n{Fore.YELLOW}[?] Masukkan Nomor Telepon (08xxx) atau NIK: {Style.RESET_ALL}")
    
    if not validate_input(target, VALID_PHONE_PREFIX, NIK_LENGTH):
        time.sleep(2)
        return
        
    simulate_search()
    result = generate_random_data()
    add_to_history(target, result)
    display_result(result)
    
    choice = input(f"\n{Fore.YELLOW}[?] Export hasil? (y/n): {Style.RESET_ALL}")
    if choice.lower() == 'y':
        export_result(result, target)

def main():
    """Main program loop."""
    clear_screen()
    print_banner()
    
    if not check_password():
        return
    
    while True:
        clear_screen()
        print_banner()
        show_menu()
        
        choice = input(f"\n{Fore.YELLOW}[?] Pilih menu (1-5): {Style.RESET_ALL}")
        
        if choice == '1':
            single_search()
        elif choice == '2':
            batch_search()
        elif choice == '3':
            show_history()
        elif choice == '4':
            show_statistics()
        elif choice == '5':
            break
        else:
            print_colored("\n[!] Pilihan tidak valid!", "ERROR")
            time.sleep(1)
            continue
        
        if choice in ['1', '2', '3', '4']:
            input(f"\n{Fore.YELLOW}[Enter untuk kembali ke menu]{Style.RESET_ALL}")
    
    print_colored("\n[!] Terima kasih telah menggunakan Pegasus Lacak Nomor!", "SUCCESS")
    time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        handle_keyboard_interrupt()
    except Exception as e:
        handle_exception(e)
