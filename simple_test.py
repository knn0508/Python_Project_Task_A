#!/usr/bin/env python3
"""
Simple test to create a few test documents
"""

import os
from pathlib import Path


def create_simple_test_files():
    """Create just a few test files for quick testing"""
    test_dir = Path("simple_test_docs")
    test_dir.mkdir(exist_ok=True)

    print("📝 Creating simple test documents...")

    # Create 3 small test documents
    test_docs = [
        {
            "filename": "hr_qaydalari.md",
            "content": """# İnsan Resursları Qaydaları

## Məzuniyyət Qaydaları
İllik məzuniyyət hüququ 21 iş günüdür.

## İş Saatları
- Başlama: 09:00
- Bitmə: 18:00
- Nahar: 13:00-14:00

## Əlaqə
HR Şöbəsi: gunel.mammadova@nazirlik.gov.az
Telefon: +994-12-555-0102
"""
        },
        {
            "filename": "layihe_statusu.md",
            "content": """# Layihə Statusu Hesabatı

## Rəqəmsal Həkimlik
- Status: Development fazasında (75% hazır)
- Rəhbər: Dr. Zaur Əhmədov
- Email: zaur.ahmadov@nazirlik.gov.az
- Deadline: 2025-ci il mart ayı

## Smart City  
- Status: Pilot test fazasında (60% hazır)
- Rəhbər: Nigar Həsənova
- Email: nigar.hasanova@nazirlik.gov.az
- Test sahəsi: Yasamal rayonu

## E-Governance
- Status: İnisial fazada (25% hazır)
- Rəhbər: Tural Əliyev
- Email: tural.aliyev@nazirlik.gov.az
- Başlama: 2025-ci il yanvar
"""
        },
        {
            "filename": "ezamiyye_qaydalari.txt",
            "content": """Ezamiyyə Qaydaları

1. Ezamiyyə ərizəsi minimum 3 gün əvvəl təqdim edilməlidir
2. Günlük yemək pulu: 25 AZN  
3. Yaşayış xərci: 50 AZN
4. Nəqliyyat xərci faktiki hesablanır

Ezamiyyə ərizəsi nümunəsi:

TARİX: [Tarix]
KÖMÜNƏ: [Şöbə rəhbəri] 
KİMDƏN: [Ad Soyad, Vəzifə]

Ezamiyyə ərizəsi

Hörmətli [Rəhbər adı],

[Başlama tarixi] - [Bitmə tarixi] tarixləri arasında [şəhər] şəhərinə iş ezamiyyətinə göndərilməyimi xahiş edirəm.

Ezamiyyənin məqsədi: [Məqsəd]
Təxmini xərc: [Məbləğ] AZN

Hörmətlə,
[Ad Soyad]

Əlaqə: Maliyyə Şöbəsi - samad.aliyev@nazirlik.gov.az
"""
        }
    ]

    for doc in test_docs:
        file_path = test_dir / doc["filename"]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(doc["content"])
        print(f"✅ Created: {doc['filename']}")

    print(f"\n📁 Test files created in: {test_dir.absolute()}")
    print("🔥 You can now upload these files via the web interface!")
    print("💡 Go to: http://localhost:5000/files-manager")


if __name__ == "__main__":
    create_simple_test_files()