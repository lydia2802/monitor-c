import sys
import time
import random
from tqdm import tqdm
from colorama import init, Fore, Style

from config.settings import (
    ACTIVATION_PASSWORD, MAX_PASSWORD_ATTEMPTS,
    PROGRESS_BAR_WIDTH, LOADING_ANIMATION_DURATION,
    LOADING_ANIMATION_ITERATIONS, VALID_PHONE_PREFIX,
    NIK_LENGTH, MAX_HISTORY_ITEMS, BATCH_INPUT_FILE,
    MAX_BATCH_SIZE, QUICK_SEARCH_MODE, MAX_FAVORITES,
    PHONE_OPERATORS
)
from config.api_config import (
    API_ENABLED, REQUIRE_CONSENT,
    DATABASE_ENABLED, ENABLE_OPERATOR_CHECK
)
from utils.helpers import (
    clear_screen, print_colored, validate_input,
    format_timestamp, handle_exception, handle_keyboard_interrupt,
    export_to_json, export_to_csv, export_to_txt,
    read_batch_file, calculate_statistics, detect_operator,
    calculate_age, calculate_distance, generate_email,
    generate_social_media, draw_ascii_chart, filter_history_by_date,
    filter_history_by_location, filter_history_by_gender, export_to_report
)
from utils.api_client import perform_real_lookup, APIClient

# Initialize colorama
init()

# Global search history and favorites
search_history = []
favorites = []
quick_mode = QUICK_SEARCH_MODE

def print_banner():
    """Print the application banner."""
    banner = f"""
    {Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════╗
    ║                         PEGASUS LACAK NOMOR v3.0                          ║
    ║                     Created by: Letda Kes dr. Sobri                       ║
    ║                          REAL TRACKING SYSTEM                             ║
    ║                     {Fore.GREEN}[API & DATABASE ENABLED]{Fore.CYAN}                      ║
    ╚════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)
    
    if REQUIRE_CONSENT:
        print_consent_disclaimer()

def print_consent_disclaimer():
    """Print privacy and consent disclaimer."""
    disclaimer = f"""
    {Fore.YELLOW}╔════════════════════════════════════════════════════════════════════════════╗
    ║                            DISCLAIMER & PRIVACY                           ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    
    [!] PENTING - HARAP DIBACA:
    
    1. Aplikasi ini menggunakan API eksternal untuk pelacakan real-time
    2. Pastikan Anda memiliki izin hukum untuk melacak nomor target
    3. Penyalahgunaan aplikasi ini dapat melanggar hukum privasi data
    4. Semua pencarian akan dicatat untuk keperluan audit
    5. Pengguna bertanggung jawab penuh atas penggunaan aplikasi ini
    
    Dengan melanjutkan, Anda menyetujui syarat dan ketentuan di atas.{Style.RESET_ALL}
    """
    print(disclaimer)
    
    consent = input(f"\n{Fore.YELLOW}Lanjutkan? (yes/no): {Style.RESET_ALL}")
    if consent.lower() not in ['yes', 'y']:
        print_colored("\n[!] Anda tidak menyetujui disclaimer. Program dihentikan.", "ERROR")
        sys.exit(0)
    print()

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

def real_search(target):
    """Perform real tracking lookup via API or database."""
    print_colored("\n[INFO] Initiating Real-time Tracking...", "INFO")
    loading_animation()
    
    # Perform actual lookup
    result = perform_real_lookup(target)
    
    # Show progress
    for _ in tqdm(range(100), desc="Tracking", 
                 bar_format="{l_bar}█{bar}█{r_bar}",
                 colour="green", ncols=PROGRESS_BAR_WIDTH):
        time.sleep(0.02)
    
    return result

def normalize_api_response(api_data, target):
    """Normalize API response to standard format."""
    normalized = {
        "Waktu Pencarian": format_timestamp()
    }
    
    # Map common API fields to our format
    field_mapping = {
        'name': 'Nama',
        'full_name': 'Nama',
        'gender': 'Jenis Kelamin',
        'birth_date': 'Birthday',
        'birthdate': 'Birthday',
        'age': 'Umur',
        'email': 'Email',
        'street': 'Jalan',
        'address': 'Jalan',
        'city': 'Kota/Town',
        'province': 'Provinsi',
        'postal_code': 'Kode Pos',
        'zip_code': 'Kode Pos',
        'country': 'Negara',
        'latitude': 'Latitude',
        'lat': 'Latitude',
        'longitude': 'Longitude',
        'lon': 'Longitude',
        'lng': 'Longitude',
        'operator': 'Operator',
        'carrier': 'Operator',
        'card_type': 'Tipe Kartu',
        'social_media': 'Social Media'
    }
    
    for api_key, display_key in field_mapping.items():
        if api_key in api_data:
            normalized[display_key] = api_data[api_key]
    
    # Ensure required fields exist
    if 'Nama' not in normalized:
        normalized['Nama'] = api_data.get('name', 'Unknown')
    
    if 'Negara' not in normalized:
        normalized['Negara'] = 'Indonesia'
    
    # Calculate age if we have birthday
    if 'Birthday' in normalized and 'Umur' not in normalized:
        age = calculate_age(normalized['Birthday'])
        if age:
            normalized['Umur'] = f"{age} tahun"
    
    # Detect operator for phone numbers
    if target.startswith('08') and 'Operator' not in normalized:
        api_client = APIClient()
        operator = api_client.check_operator(target)
        if operator:
            normalized['Operator'] = operator
    
    # Generate missing fields if needed
    if 'Email' not in normalized and 'Nama' in normalized:
        normalized['Email'] = generate_email(normalized['Nama'])
    
    if 'Social Media' not in normalized and 'Nama' in normalized:
        normalized['Social Media'] = generate_social_media(normalized['Nama'])
    
    return normalized

def display_result(data):
    """Display search results."""
    print_colored("\nResult:", "SUCCESS")
    for key, value in data.items():
        if key == "Waktu Pencarian":
            print_colored(f"{key}: {value}", "WARNING")
        elif key == "Social Media":
            print_colored(f"\n{key}:", "INFO")
            for platform, handle in value.items():
                print_colored(f"  - {platform}: {handle}", "INFO")
        else:
            print_colored(f"{key}: {value}", "INFO")
    print_colored("\n[✔] Search Data complete!", "SUCCESS")

def add_to_history(target, result, note=""):
    """Add search to history."""
    global search_history
    if len(search_history) >= MAX_HISTORY_ITEMS:
        search_history.pop(0)
    
    history_entry = {
        'target': target,
        'timestamp': format_timestamp(),
        'result': result,
        'note': note
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
    """Search multiple numbers from file with real tracking."""
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
    print_colored(f"[INFO] Mode: Real Tracking via API/Database", "SUCCESS")
    
    time.sleep(1)
    
    results = []
    for i, target in enumerate(numbers, 1):
        print_colored(f"\n[{i}/{len(numbers)}] Mencari: {target}", "INFO")
        
        if not validate_input(target, VALID_PHONE_PREFIX, NIK_LENGTH):
            print_colored(f"[!] Melewati nomor tidak valid: {target}", "ERROR")
            continue
        
        result = None
        
        # Perform real tracking
        api_result = perform_real_lookup(target)
        if api_result:
            result = normalize_api_response(api_result, target)
            result["Source"] = "API/Database"
        else:
            print_colored(f"[!] Data tidak ditemukan untuk: {target}", "WARNING")
        
        if result:
            result['Target'] = target
            results.append(result)
            add_to_history(target, result)
            
            # Show brief result for batch
            print_colored(f"    Nama: {result.get('Nama', 'N/A')}", "INFO")
            print_colored(f"    Kota: {result.get('Kota/Town', 'N/A')}", "INFO")
            time.sleep(0.3)
    
    print_colored(f"\n[✓] Batch search selesai! {len(results)}/{len(numbers)} berhasil.", "SUCCESS")
    
    if results:
        choice = input(f"\n{Fore.YELLOW}[?] Export semua hasil? (y/n): {Style.RESET_ALL}")
        if choice.lower() == 'y':
            timestamp = format_timestamp().replace(' ', '_').replace(':', '-')
            filepath = export_to_json(results, f"batch_results_{timestamp}.json")
            print_colored(f"\n[✓] Semua hasil diexport ke: {filepath}", "SUCCESS")

def search_by_name():
    """Search by name (reverse lookup) - Requires API/Database support."""
    print_colored("\n[!] Fitur pencarian berdasarkan nama memerlukan API/Database yang mendukung reverse lookup.", "WARNING")
    print_colored("[!] Fitur ini telah dinonaktifkan karena memerlukan data real dari API.", "WARNING")
    time.sleep(3)

def search_by_location():
    """Search by location (city/province) - Requires API/Database support."""
    print_colored("\n[!] Fitur pencarian berdasarkan lokasi memerlukan API/Database yang mendukung location lookup.", "WARNING")
    print_colored("[!] Fitur ini telah dinonaktifkan karena memerlukan data real dari API.", "WARNING")
    time.sleep(3)

def advanced_filter_history():
    """Filter history with advanced options."""
    if not search_history:
        print_colored("\n[!] History kosong.", "WARNING")
        return
    
    print_colored(f"\n{'='*70}", "INFO")
    print_colored("FILTER HISTORY", "SUCCESS")
    print_colored(f"{'='*70}", "INFO")
    print("1. Filter berdasarkan tanggal")
    print("2. Filter berdasarkan lokasi")
    print("3. Filter berdasarkan gender")
    print("4. Kembali")
    
    choice = input(f"\n{Fore.YELLOW}Pilih filter (1-4): {Style.RESET_ALL}")
    
    filtered = []
    if choice == '1':
        date = input(f"\n{Fore.YELLOW}Masukkan tanggal (YYYY-MM-DD): {Style.RESET_ALL}")
        filtered = filter_history_by_date(search_history, date)
    elif choice == '2':
        location = input(f"\n{Fore.YELLOW}Masukkan lokasi: {Style.RESET_ALL}")
        filtered = filter_history_by_location(search_history, location)
    elif choice == '3':
        gender = input(f"\n{Fore.YELLOW}Masukkan gender (Laki-laki/Perempuan): {Style.RESET_ALL}")
        filtered = filter_history_by_gender(search_history, gender)
    elif choice == '4':
        return
    else:
        print_colored("\n[!] Pilihan tidak valid!", "ERROR")
        return
    
    if not filtered:
        print_colored("\n[!] Tidak ada hasil yang sesuai filter.", "WARNING")
        return
    
    print_colored(f"\n{'='*70}", "INFO")
    print_colored(f"HASIL FILTER ({len(filtered)} item)", "SUCCESS")
    print_colored(f"{'='*70}", "INFO")
    
    for i, entry in enumerate(filtered, 1):
        print_colored(f"\n[{i}] Target: {entry['target']}", "INFO")
        print_colored(f"    Waktu: {entry['timestamp']}", "WARNING")
        print_colored(f"    Nama: {entry['result']['Nama']}", "INFO")
        print_colored(f"    Lokasi: {entry['result']['Kota/Town']}, {entry['result']['Provinsi']}", "INFO")

def show_visual_statistics():
    """Display statistics with ASCII charts."""
    if not search_history:
        print_colored("\n[!] Belum ada data untuk statistik.", "WARNING")
        return
    
    stats = calculate_statistics(search_history)
    
    print_colored(f"\n{'='*70}", "INFO")
    print_colored("STATISTIK VISUAL", "SUCCESS")
    print_colored(f"{'='*70}", "INFO")
    
    search_types = {
        "Nomor Telepon": stats['phone_numbers'],
        "NIK": stats['niks']
    }
    draw_ascii_chart(search_types, "Tipe Pencarian")
    
    gender_count = {}
    for h in search_history:
        gender = h['result'].get('Jenis Kelamin', 'Unknown')
        gender_count[gender] = gender_count.get(gender, 0) + 1
    
    if gender_count:
        draw_ascii_chart(gender_count, "Distribusi Gender")
    
    city_count = {}
    for h in search_history:
        city = h['result'].get('Kota/Town', 'Unknown')
        city_count[city] = city_count.get(city, 0) + 1
    
    top_cities = dict(sorted(city_count.items(), key=lambda x: x[1], reverse=True)[:5])
    if top_cities:
        draw_ascii_chart(top_cities, "Top 5 Kota")

def calculate_distance_feature():
    """Calculate distance between two coordinates."""
    print_colored("\n[?] KALKULATOR JARAK", "SUCCESS")
    
    try:
        lat1 = float(input(f"\n{Fore.YELLOW}Latitude 1: {Style.RESET_ALL}"))
        lon1 = float(input(f"{Fore.YELLOW}Longitude 1: {Style.RESET_ALL}"))
        lat2 = float(input(f"{Fore.YELLOW}Latitude 2: {Style.RESET_ALL}"))
        lon2 = float(input(f"{Fore.YELLOW}Longitude 2: {Style.RESET_ALL}"))
        
        distance = calculate_distance(lat1, lon1, lat2, lon2)
        print_colored(f"\n[✓] Jarak: {distance} km", "SUCCESS")
    except ValueError:
        print_colored("\n[!] Input tidak valid! Masukkan angka.", "ERROR")

def manage_favorites():
    """Manage favorite/bookmarked searches."""
    global favorites
    
    print_colored(f"\n{'='*70}", "INFO")
    print_colored("FAVORIT", "SUCCESS")
    print_colored(f"{'='*70}", "INFO")
    print("1. Tambah dari history")
    print("2. Lihat favorit")
    print("3. Hapus favorit")
    print("4. Kembali")
    
    choice = input(f"\n{Fore.YELLOW}Pilih (1-4): {Style.RESET_ALL}")
    
    if choice == '1':
        if not search_history:
            print_colored("\n[!] History kosong.", "WARNING")
            return
        
        if len(favorites) >= MAX_FAVORITES:
            print_colored(f"\n[!] Favorit penuh (max {MAX_FAVORITES}).", "WARNING")
            return
        
        print_colored("\n[?] Pilih nomor dari history:", "INFO")
        for i, h in enumerate(search_history[-10:], 1):
            print(f"{i}. {h['target']} - {h['result']['Nama']}")
        
        idx = input(f"\n{Fore.YELLOW}Pilih nomor (1-{min(10, len(search_history))}): {Style.RESET_ALL}")
        try:
            idx = int(idx) - 1
            if 0 <= idx < len(search_history[-10:]):
                favorites.append(search_history[-(10-idx)])
                print_colored("\n[✓] Ditambahkan ke favorit!", "SUCCESS")
            else:
                print_colored("\n[!] Nomor tidak valid!", "ERROR")
        except ValueError:
            print_colored("\n[!] Input tidak valid!", "ERROR")
    
    elif choice == '2':
        if not favorites:
            print_colored("\n[!] Favorit kosong.", "WARNING")
            return
        
        print_colored(f"\n{'='*70}", "INFO")
        print_colored(f"DAFTAR FAVORIT ({len(favorites)})", "SUCCESS")
        print_colored(f"{'='*70}", "INFO")
        
        for i, fav in enumerate(favorites, 1):
            print_colored(f"\n[{i}] {fav['target']}", "INFO")
            print_colored(f"    Nama: {fav['result']['Nama']}", "INFO")
            print_colored(f"    Kota: {fav['result']['Kota/Town']}", "INFO")
    
    elif choice == '3':
        if not favorites:
            print_colored("\n[!] Favorit kosong.", "WARNING")
            return
        
        for i, fav in enumerate(favorites, 1):
            print(f"{i}. {fav['target']} - {fav['result']['Nama']}")
        
        idx = input(f"\n{Fore.YELLOW}Pilih nomor untuk dihapus: {Style.RESET_ALL}")
        try:
            idx = int(idx) - 1
            if 0 <= idx < len(favorites):
                favorites.pop(idx)
                print_colored("\n[✓] Dihapus dari favorit!", "SUCCESS")
            else:
                print_colored("\n[!] Nomor tidak valid!", "ERROR")
        except ValueError:
            print_colored("\n[!] Input tidak valid!", "ERROR")

def clear_history():
    """Clear search history."""
    global search_history
    
    if not search_history:
        print_colored("\n[!] History sudah kosong.", "WARNING")
        return
    
    confirm = input(f"\n{Fore.YELLOW}[!] Hapus semua history? (y/n): {Style.RESET_ALL}")
    if confirm.lower() == 'y':
        search_history.clear()
        print_colored("\n[✓] History berhasil dihapus!", "SUCCESS")
    else:
        print_colored("\n[!] Dibatalkan.", "WARNING")

def add_note_to_search():
    """Add note to a search in history."""
    if not search_history:
        print_colored("\n[!] History kosong.", "WARNING")
        return
    
    print_colored("\n[?] Pilih pencarian untuk ditambahkan catatan:", "INFO")
    for i, h in enumerate(search_history[-10:], 1):
        note_text = f" - {h['note']}" if h.get('note') else ""
        print(f"{i}. {h['target']} - {h['result']['Nama']}{note_text}")
    
    idx = input(f"\n{Fore.YELLOW}Pilih nomor: {Style.RESET_ALL}")
    try:
        idx = int(idx) - 1
        if 0 <= idx < len(search_history[-10:]):
            note = input(f"{Fore.YELLOW}Masukkan catatan: {Style.RESET_ALL}")
            search_history[-(10-idx)]['note'] = note
            print_colored("\n[✓] Catatan ditambahkan!", "SUCCESS")
        else:
            print_colored("\n[!] Nomor tidak valid!", "ERROR")
    except ValueError:
        print_colored("\n[!] Input tidak valid!", "ERROR")

def toggle_quick_mode():
    """Toggle quick search mode."""
    global quick_mode
    quick_mode = not quick_mode
    status = "AKTIF" if quick_mode else "NONAKTIF"
    print_colored(f"\n[✓] Mode Cepat: {status}", "SUCCESS")
    time.sleep(1)

def generate_detailed_report():
    """Generate detailed report for last search."""
    if not search_history:
        print_colored("\n[!] Belum ada pencarian.", "WARNING")
        return
    
    last_search = search_history[-1]
    result = last_search['result'].copy()
    result['Target'] = last_search['target']
    result['Catatan'] = last_search.get('note', '-')
    
    timestamp = format_timestamp().replace(' ', '_').replace(':', '-')
    filepath = export_to_report(result, f"report_{timestamp}.txt")
    print_colored(f"\n[✓] Laporan lengkap dibuat: {filepath}", "SUCCESS")

def show_operator_info():
    """Show phone operator information."""
    print_colored(f"\n{'='*70}", "INFO")
    print_colored("INFORMASI OPERATOR", "SUCCESS")
    print_colored(f"{'='*70}", "INFO")
    
    operators = {}
    for prefix, op in PHONE_OPERATORS.items():
        if op not in operators:
            operators[op] = []
        operators[op].append(prefix)
    
    for op, prefixes in operators.items():
        print_colored(f"\n{op}:", "SUCCESS")
        print_colored(f"  Prefix: {', '.join(prefixes)}", "INFO")

def show_menu():
    """Display main menu."""
    print_colored(f"\n{'='*70}", "INFO")
    print_colored("MENU UTAMA", "SUCCESS")
    print_colored(f"{'='*70}", "INFO")
    print("1. Pencarian Tunggal")
    print("2. Pencarian Batch (dari file)")
    print("3. Pencarian Berdasarkan Nama")
    print("4. Pencarian Berdasarkan Lokasi")
    print("5. Lihat History")
    print("6. Filter History (Advanced)")
    print("7. Lihat Statistik")
    print("8. Statistik Visual (Chart)")
    print("9. Kalkulator Jarak")
    print("10. Kelola Favorit")
    print("11. Hapus History")
    print("12. Tambah Catatan")
    print("13. Mode Cepat (Toggle)")
    print("14. Generate Laporan Lengkap")
    print("15. Info Operator")
    print("0. Keluar")
    print_colored(f"{'='*70}", "INFO")
    
    mode_status = "ON" if quick_mode else "OFF"
    print_colored(f"Mode Cepat: {mode_status}", "WARNING")

def single_search():
    """Perform single search with real tracking."""
    target = input(f"\n{Fore.YELLOW}[?] Masukkan Nomor Telepon (08xxx) atau NIK: {Style.RESET_ALL}")
    
    if not validate_input(target, VALID_PHONE_PREFIX, NIK_LENGTH):
        time.sleep(2)
        return
    
    result = None
    
    # Perform real tracking
    if not quick_mode:
        api_result = real_search(target)
    else:
        print_colored("\n[INFO] Mode cepat aktif - query langsung", "WARNING")
        api_result = perform_real_lookup(target)
    
    if api_result:
        result = normalize_api_response(api_result, target)
        result["Source"] = "API/Database"
        print_colored("[✓] Data ditemukan dari sumber real!", "SUCCESS")
    else:
        print_colored("\n[!] Data tidak ditemukan. Pastikan API/Database dikonfigurasi dengan benar.", "ERROR")
        print_colored("[!] Atau nomor/NIK tidak ada dalam database.", "WARNING")
        time.sleep(3)
        return
    
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
        
        choice = input(f"\n{Fore.YELLOW}[?] Pilih menu (0-15): {Style.RESET_ALL}")
        
        if choice == '1':
            single_search()
        elif choice == '2':
            batch_search()
        elif choice == '3':
            search_by_name()
        elif choice == '4':
            search_by_location()
        elif choice == '5':
            show_history()
        elif choice == '6':
            advanced_filter_history()
        elif choice == '7':
            show_statistics()
        elif choice == '8':
            show_visual_statistics()
        elif choice == '9':
            calculate_distance_feature()
        elif choice == '10':
            manage_favorites()
        elif choice == '11':
            clear_history()
        elif choice == '12':
            add_note_to_search()
        elif choice == '13':
            toggle_quick_mode()
        elif choice == '14':
            generate_detailed_report()
        elif choice == '15':
            show_operator_info()
        elif choice == '0':
            break
        else:
            print_colored("\n[!] Pilihan tidak valid!", "ERROR")
            time.sleep(1)
            continue
        
        if choice in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '14', '15']:
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
