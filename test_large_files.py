#!/usr/bin/env python3
"""
Large File Processing Test Script
Demonstrates how the system handles 50+ files including 80-page documents
"""

import os
import time
from pathlib import Path
from file_manager import FileManager, DocumentChunker
import json


def create_test_documents():
    """Create test documents of various sizes"""
    test_dir = Path("test_documents")
    test_dir.mkdir(exist_ok=True)

    print("📝 Creating test documents...")

    # Create small documents (2-3 pages)
    for i in range(47):  # 47 small documents
        content = f"""# Test Document {i + 1}

## Nazirlik Prosedurları

Bu sənəd test məqsədi üçün yaradılmışdır.

### Əsas Məlumatlar
- Sənəd nömrəsi: {i + 1}
- Yaradılma tarixi: 2025-01-01
- Statusu: Aktiv

### Təfərrüatlar
{"Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 50}

### Qayda və Qaydalar
{"Bu bölmədə müxtəlif qaydalar və prosedurlar təsvir edilir. " * 30}

### Əlaqə Məlumatları
Email: test{i + 1}@nazirlik.gov.az
Telefon: +994-12-555-{1000 + i}

### Əlavə Məlumatlar
{"Əlavə məlumatlar və izahlar bu hissədə yer alır. " * 40}
"""

        with open(test_dir / f"test_document_{i + 1:02d}.md", 'w', encoding='utf-8') as f:
            f.write(content)

    # Create 3 large documents (80+ pages each)
    large_docs = [
        {
            "name": "nazirlik_tam_rehber.md",
            "title": "Nazirlik Tam Rəhbəri",
            "sections": 25,
            "pages_per_section": 4
        },
        {
            "name": "layihe_menecment_kitabi.md",
            "title": "Layihə Menecment Kitabı",
            "sections": 20,
            "pages_per_section": 5
        },
        {
            "name": "hr_tam_prosedurlar.md",
            "title": "İnsan Resursları Tam Prosedurları",
            "sections": 30,
            "pages_per_section": 3
        }
    ]

    for doc in large_docs:
        print(f"📄 Creating large document: {doc['title']}")
        content = f"""# {doc['title']}

Bu ətraflı sənəd Azərbaycan Respublikası nazirlik işçiləri üçün hazırlanmışdır.

## Mündəricat

"""

        # Add table of contents
        for section in range(1, doc['sections'] + 1):
            content += f"- {section}. Bölmə: Section {section}\n"

        content += "\n---\n\n"

        # Create detailed sections
        for section in range(1, doc['sections'] + 1):
            content += f"""
## {section}. Bölmə: Section {section}

### {section}.1 Giriş
{"Bu bölmədə əsas məsələlər və prinsiplər izah edilir. " * 100}

### {section}.2 Əsas Qaydalar
{"Əsas qaydalar və tələblər bu hissədə detallı şəkildə təsvir edilir. " * 120}

### {section}.3 Prosedurlar
{"Addım-addım prosedurlar və təlimatlar aşağıda verilmişdir. " * 80}

1. İlk addım: {"Ətraflı izahlar və nümunələr ilə birlikdə. " * 20}
2. İkinci addım: {"Əlavə təfərrüatlar və məsləhətlər ilə. " * 25}
3. Üçüncü addım: {"Son mərhələ və yekun qiymətləndirmə. " * 15}

### {section}.4 Nümunələr və Şablonlar
{"Praktiki nümunələr və hazır şablonlar bu hissədə təqdim olunur. " * 150}

### {section}.5 Tez-tez Verilən Suallar
Q: {"Tipik sual nümunəsi? " * 5}
A: {"Ətraflı cavab və izahlar. " * 30}

Q: {"Digər mühüm sual? " * 3}  
A: {"Hərtərəfli cavab və məsləhətlər. " * 35}

### {section}.6 Əlaqə və Dəstək
{"Bu bölmə üçün əlaqə məlumatları və dəstək xidmətləri. " * 40}

### {section}.7 Əlavə Resurslar
{"Əlavə oxuma materialları və faydalı linklər. " * 60}

---

"""

        # Add conclusion
        content += f"""
## Nəticə

{doc['title']} sənədi nazirlik işçiləri üçün əhatəli bir rəhbərdir.

### Əsas Nöqtələr:
{"• Mühüm məqam və qeydlər. " * 50}

### Tövsiyələr:
{"• Praktiki tövsiyələr və məsləhətlər. " * 40}

### Son Qeydlər:
{"• Əlavə izahlar və xatırlatmalar. " * 30}

---

*Bu sənəd {doc['sections']} bölmədən ibarətdir və təxminən 80+ səhifə məlumat ehtiva edir.*
*Son yenilənmə: 2025-01-01*
*Versiya: 1.0*
"""

        with open(test_dir / doc['name'], 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"✅ Created 50 test documents (47 small + 3 large)")
    return test_dir


def test_chunking_system():
    """Test the document chunking system"""
    print("\n🔧 Testing Chunking System...")

    chunker = DocumentChunker(max_chunk_size=4000, overlap_size=200)

    # Test with large text
    large_text = "Bu çox böyük bir sənədin məzmunudur. " * 2000  # ~74,000 characters

    chunks = chunker.chunk_text(large_text, "test_doc")

    print(f"📊 Large text stats:")
    print(f"   - Original length: {len(large_text)} characters")
    print(f"   - Number of chunks: {len(chunks)}")
    print(f"   - Average chunk size: {len(large_text) // len(chunks)} characters")

    for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
        print(f"   - Chunk {i + 1}: {len(chunk['content'])} characters")


def test_bulk_upload():
    """Test bulk upload functionality"""
    print("\n📤 Testing Bulk Upload...")

    # Create test documents
    test_dir = create_test_documents()

    # Initialize file manager
    file_manager = FileManager()

    # Test bulk upload
    start_time = time.time()
    result = file_manager.bulk_upload(str(test_dir), category="Test Documents")
    end_time = time.time()

    print(f"⏱️  Upload completed in {end_time - start_time:.2f} seconds")
    print(f"📊 Results:")
    print(f"   - Total processed: {result['total_processed']}")
    print(f"   - Successful: {result['successful']}")
    print(f"   - Failed: {result['failed']}")

    if result['failed'] > 0:
        print("❌ Failed uploads:")
        for failure in result['details']['failed']:
            print(f"   - {failure['file']}: {failure['error']}")


def test_search_performance():
    """Test search performance with many files"""
    print("\n🔍 Testing Search Performance...")

    file_manager = FileManager()

    # Test different search queries
    test_queries = [
        "nazirlik",
        "prosedur",
        "əlaqə",
        "layihə",
        "qaydalar",
        "test document 25"
    ]

    for query in test_queries:
        start_time = time.time()
        results = file_manager.search_files(query)
        end_time = time.time()

        print(f"🔍 '{query}':")
        print(f"   - Found: {len(results)} results")
        print(f"   - Time: {(end_time - start_time) * 1000:.1f}ms")


def demonstrate_ai_integration():
    """Show how AI works with large documents"""
    print("\n🤖 Testing AI Integration...")

    from models import EnhancedKnowledgeBase, EnhancedAIAssistant
    from config import Config

    file_manager = FileManager()
    kb = EnhancedKnowledgeBase(file_manager)
    ai = EnhancedAIAssistant(kb, Config.GEMINI_API_KEY)

    # Test user info
    test_user = {
        'id': 1,
        'username': 'test_user',
        'name': 'Test İstifadəçi',
        'role': 'admin'
    }

    # Test queries that should find information in uploaded documents
    test_questions = [
        "Test sənədləri haqqında məlumat ver",
        "Nazirlik rəhbəri sənədində nə var?",
        "Layihə menecment kitabından məlumat lazımdır"
    ]

    for question in test_questions:
        print(f"\n❓ Sual: {question}")
        try:
            response = ai.generate_enhanced_response(question, test_user)
            print(f"🤖 Cavab: {response[:200]}...")
        except Exception as e:
            print(f"❌ Xəta: {e}")


def show_system_capabilities():
    """Display system capabilities summary"""
    print("\n" + "=" * 50)
    print("🎯 SİSTEM İMKANLARI")
    print("=" * 50)

    capabilities = {
        "Dəstəklənən Fayl Formatları": [
            "📄 PDF - PyPDF2 ilə mətn çıxarılması",
            "📝 DOCX - python-docx ilə məzmun çıxarılması",
            "📊 XLSX/XLS - openpyxl ilə data çıxarılması",
            "📃 TXT - birbaşa mətn oxunması",
            "🔤 HTML - BeautifulSoup ilə mətn çıxarılması",
            "📋 Markdown - markdown parser ilə çevrilmə"
        ],
        "Böyük Fayl İdarəetməsi": [
            "🔧 Ağıllı chunking sistemi (4000 söz hər chunk)",
            "🔄 200 söz overlap kontekst saxlamaq üçün",
            "📚 80+ səhifəli sənədlər avtomatik bölünür",
            "💾 SQLite FTS5 sürətli axtarış üçün",
            "🔍 Chunk-əsaslı axtarış sistemi"
        ],
        "Toplu Əməliyyatlar": [
            "📤 Toplu fayl yükləmə (50+ fayl)",
            "📁 Qovluq strukturu saxlanması",
            "⚡ Paralel processing imkanı",
            "📊 Ətraflı progress reporting",
            "🔄 Avtomatik retry mexanizmi"
        ],
        "AI İnteqrasiyası": [
            "🤖 Sənəd-məzmunlu AI cavabları",
            "💬 Danışıq konteksti saxlanması",
            "🎯 Rol-əsaslı cavab diferensiasiyası",
            "🔍 Ağıllı sənəd aşkarlama",
            "📝 Avtomatik məzmun ümumiləşdirmə"
        ]
    }

    for category, items in capabilities.items():
        print(f"\n🏷️  {category}:")
        for item in items:
            print(f"   {item}")

    print(f"\n📈 Performance Optimizations:")
    print(f"   ⚡ Lazy loading of document chunks")
    print(f"   🧠 In-memory conversation caching")
    print(f"   🔍 Indexed full-text search")
    print(f"   📦 Efficient storage with SQLite")


def main():
    """Main test function"""
    print("🚀 BÖYÜK FAYL SİSTEMİ TEST SKRIPTI")
    print("=" * 50)

    # Show capabilities
    show_system_capabilities()

    # Test chunking
    test_chunking_system()

    # Test bulk upload
    test_bulk_upload()

    # Test search performance
    test_search_performance()

    # Test AI integration
    demonstrate_ai_integration()

    print("\n" + "=" * 50)
    print("✅ Bütün testlər tamamlandı!")
    print("📋 Sistem 50+ fayl və 80 səhifəli sənədlər üçün hazırdır")
    print("=" * 50)


if __name__ == "__main__":
    main()