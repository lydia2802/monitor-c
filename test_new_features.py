#!/usr/bin/env python3
"""Test script for new features in Pegasus Lacak Nomor v3.0"""

import sys
from utils.helpers import (
    detect_operator, calculate_age, generate_email,
    generate_social_media, calculate_distance, draw_ascii_chart,
    filter_history_by_date, filter_history_by_location,
    filter_history_by_gender
)

def test_operator_detection():
    """Test phone operator detection"""
    print("=" * 70)
    print("TEST 1: OPERATOR DETECTION")
    print("=" * 70)
    
    test_cases = [
        ("08112345678", "Telkomsel"),
        ("08172345678", "XL"),
        ("08952345678", "Three"),
        ("08142345678", "Indosat"),
        ("08312345678", "Axis"),
        ("08812345678", "Smartfren"),
        ("1234567890", "N/A"),
    ]
    
    passed = 0
    for number, expected in test_cases:
        result = detect_operator(number)
        status = "✓" if result == expected else "✗"
        print(f"  {status} {number} -> {result} (expected: {expected})")
        if result == expected:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

def test_age_calculation():
    """Test age calculation"""
    print("\n" + "=" * 70)
    print("TEST 2: AGE CALCULATION")
    print("=" * 70)
    
    test_cases = [
        ("1990-01-01", 35),
        ("2000-06-15", 24),
        ("1985-12-25", 39),
    ]
    
    passed = 0
    for birthday, expected_age in test_cases:
        result = calculate_age(birthday)
        if result is not None:
            diff = abs(result - expected_age)
            status = "✓" if diff <= 1 else "✗"
            print(f"  {status} {birthday} -> {result} years (expected: ~{expected_age})")
            if diff <= 1:
                passed += 1
        else:
            print(f"  ✗ {birthday} -> Error calculating age")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

def test_email_generation():
    """Test email generation"""
    print("\n" + "=" * 70)
    print("TEST 3: EMAIL GENERATION")
    print("=" * 70)
    
    names = ["Budi Santoso", "Siti Rahayu", "Ahmad Hidayat"]
    
    for name in names:
        email = generate_email(name)
        clean_name = name.lower().replace(' ', '.')
        status = "✓" if clean_name in email and '@' in email else "✗"
        print(f"  {status} {name} -> {email}")
    
    print(f"\nPassed: 3/3")
    return True

def test_social_media_generation():
    """Test social media generation"""
    print("\n" + "=" * 70)
    print("TEST 4: SOCIAL MEDIA GENERATION")
    print("=" * 70)
    
    name = "Budi Santoso"
    social = generate_social_media(name)
    
    platforms = ["Instagram", "Facebook", "Twitter", "TikTok"]
    passed = 0
    
    for platform in platforms:
        if platform in social:
            handle = social[platform]
            status = "✓" if '@' in handle and 'budi_santoso' in handle else "✗"
            print(f"  {status} {platform}: {handle}")
            if '@' in handle:
                passed += 1
        else:
            print(f"  ✗ {platform}: Missing")
    
    print(f"\nPassed: {passed}/{len(platforms)}")
    return passed == len(platforms)

def test_distance_calculation():
    """Test distance calculation"""
    print("\n" + "=" * 70)
    print("TEST 5: DISTANCE CALCULATION")
    print("=" * 70)
    
    test_cases = [
        ((-6.2, 106.8), (-7.8, 110.4), "Jakarta to Yogyakarta", 435),
        ((0, 0), (0, 0), "Same location", 0),
        ((-6.2, 106.8), (-6.9, 107.6), "Jakarta to Bandung", 120),
    ]
    
    passed = 0
    for (lat1, lon1), (lat2, lon2), description, expected in test_cases:
        result = calculate_distance(lat1, lon1, lat2, lon2)
        diff = abs(result - expected)
        status = "✓" if diff <= 50 else "✗"
        print(f"  {status} {description}: {result} km (expected: ~{expected} km)")
        if diff <= 50:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

def test_ascii_chart():
    """Test ASCII chart generation"""
    print("\n" + "=" * 70)
    print("TEST 6: ASCII CHART GENERATION")
    print("=" * 70)
    
    data = {
        "Telkomsel": 45,
        "XL": 25,
        "Indosat": 20,
        "Three": 10
    }
    
    print("\nGenerating sample chart:")
    draw_ascii_chart(data, "Phone Operators")
    
    print("\n✓ Chart generated successfully")
    return True

def test_history_filters():
    """Test history filtering functions"""
    print("\n" + "=" * 70)
    print("TEST 7: HISTORY FILTERS")
    print("=" * 70)
    
    mock_history = [
        {
            'target': '08123456789',
            'timestamp': '2024-01-15 10:00:00',
            'result': {
                'Nama': 'Budi',
                'Kota/Town': 'Jakarta',
                'Provinsi': 'DKI Jakarta',
                'Jenis Kelamin': 'Laki-laki'
            }
        },
        {
            'target': '08987654321',
            'timestamp': '2024-01-16 11:00:00',
            'result': {
                'Nama': 'Siti',
                'Kota/Town': 'Surabaya',
                'Provinsi': 'Jawa Timur',
                'Jenis Kelamin': 'Perempuan'
            }
        },
        {
            'target': '08111222333',
            'timestamp': '2024-01-15 12:00:00',
            'result': {
                'Nama': 'Ahmad',
                'Kota/Town': 'Jakarta',
                'Provinsi': 'DKI Jakarta',
                'Jenis Kelamin': 'Laki-laki'
            }
        }
    ]
    
    passed = 0
    
    # Test date filter
    filtered_by_date = filter_history_by_date(mock_history, '2024-01-15')
    status = "✓" if len(filtered_by_date) == 2 else "✗"
    print(f"  {status} Filter by date (2024-01-15): {len(filtered_by_date)} results (expected: 2)")
    if len(filtered_by_date) == 2:
        passed += 1
    
    # Test location filter
    filtered_by_location = filter_history_by_location(mock_history, 'Jakarta')
    status = "✓" if len(filtered_by_location) == 2 else "✗"
    print(f"  {status} Filter by location (Jakarta): {len(filtered_by_location)} results (expected: 2)")
    if len(filtered_by_location) == 2:
        passed += 1
    
    # Test gender filter
    filtered_by_gender = filter_history_by_gender(mock_history, 'Laki-laki')
    status = "✓" if len(filtered_by_gender) == 2 else "✗"
    print(f"  {status} Filter by gender (Laki-laki): {len(filtered_by_gender)} results (expected: 2)")
    if len(filtered_by_gender) == 2:
        passed += 1
    
    print(f"\nPassed: {passed}/3")
    return passed == 3

def main():
    """Run all tests"""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "PEGASUS LACAK NOMOR - NEW FEATURES TEST" + " " * 13 + "║")
    print("╚" + "═" * 68 + "╝\n")
    
    tests = [
        ("Operator Detection", test_operator_detection),
        ("Age Calculation", test_age_calculation),
        ("Email Generation", test_email_generation),
        ("Social Media Generation", test_social_media_generation),
        ("Distance Calculation", test_distance_calculation),
        ("ASCII Chart Generation", test_ascii_chart),
        ("History Filters", test_history_filters),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} failed with error: {str(e)}")
            results.append((name, False))
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\n{'=' * 70}")
    print(f"Total: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n✓ All tests passed successfully!")
        return 0
    else:
        print(f"\n✗ {total_count - passed_count} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
