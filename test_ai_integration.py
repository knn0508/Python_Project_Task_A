#!/usr/bin/env python3
"""
Test script to demonstrate AI integration with uploaded files
Run this after uploading files to see how AI responds
"""

from models import EnhancedKnowledgeBase, EnhancedAIAssistant
from file_manager import FileManager
from config import Config




def test_ai_with_uploaded_files():
    """Test how AI responds to questions about uploaded files"""

    print("🤖 Testing AI Integration with Uploaded Files")
    print("=" * 50)

    # Initialize components
    file_manager = FileManager()
    knowledge_base = EnhancedKnowledgeBase(file_manager)
    ai_assistant = EnhancedAIAssistant(knowledge_base, Config.GEMINI_API_KEY)

    # Sample user (you can change this)
    test_user = {
        'id': 1,
        'username': 'admin',
        'name': 'Test İstifadəçi',
        'role': 'admin'
    }

    # Test questions that should find content in uploaded files
    test_questions = [
        "Məzuniyyət qaydaları haqqında məlumat ver",
        "Layihə statusu nədir?",
        "Ezamiyyə ərizəsi necə yazılır?",
        "HR şöbəsi ilə necə əlaqə saxlayım?",
        "İş saatları nədir?",
        "Hansı sənədlər mövcuddur?",
        "Test sənədlərində nə var?",
        "Nazirlik struktur necədir?"
    ]

    print("🔍 Testing Knowledge Base Search...")

    # First, check what files are available
    files = file_manager.list_files()
    print(f"📁 Available files: {len(files)}")
    for file_info in files[:5]:  # Show first 5 files
        print(f"   - {file_info['filename']} ({file_info['file_type']})")

    if len(files) > 5:
        print(f"   ... and {len(files) - 5} more files")

    print("\n" + "─" * 50)

    # Test knowledge base search directly
    for i, question in enumerate(test_questions[:3], 1):
        print(f"\n🔍 Test {i}: Direct Knowledge Search")
        print(f"❓ Query: '{question}'")

        search_results = knowledge_base.search(question)
        if search_results and "Heç bir məlumat tapılmadı" not in search_results:
            print(f"✅ Found relevant content:")
            print(f"📄 {search_results[:300]}...")
        else:
            print("❌ No relevant content found")

    print("\n" + "─" * 50)

    # Test AI responses
    for i, question in enumerate(test_questions, 1):
        print(f"\n🤖 Test {i}: AI Response")
        print(f"❓ Sual: {question}")

        try:
            response = ai_assistant.generate_enhanced_response(question, test_user)
            print(f"🗣️  Cavab: {response[:400]}...")

            # Check if response mentions specific documents
            if any(word in response.lower() for word in ['sənəd', 'fayl', 'test', 'nazirlik']):
                print("✅ AI referenced uploaded documents")
            else:
                print("⚠️  AI used static knowledge base")

        except Exception as e:
            print(f"❌ Error: {e}")

        print("─" * 30)


def demonstrate_file_specific_queries():
    """Test AI with specific file queries"""

    print("\n📄 Testing File-Specific Queries")
    print("=" * 50)

    file_manager = FileManager()
    knowledge_base = EnhancedKnowledgeBase(file_manager)
    ai_assistant = EnhancedAIAssistant(knowledge_base, Config.GEMINI_API_KEY)

    test_user = {
        'id': 1,
        'username': 'admin',
        'name': 'Test İstifadəçi',
        'role': 'admin'
    }

    # Get list of uploaded files
    files = file_manager.list_files()

    if not files:
        print("❌ No files uploaded yet. Please upload some files first.")
        return

    # Test queries about specific files
    for file_info in files[:3]:  # Test first 3 files
        filename = file_info['filename']

        # Create specific questions about this file
        specific_questions = [
            f"'{filename}' sənədində nə var?",
            f"'{filename}' haqqında məlumat ver",
            f"'{filename}' faylının məzmununu izah et"
        ]

        print(f"\n📋 Testing queries about: {filename}")

        for question in specific_questions[:1]:  # Test 1 question per file
            print(f"❓ Sual: {question}")

            try:
                response = ai_assistant.generate_enhanced_response(question, test_user)
                print(f"🤖 Cavab: {response[:300]}...")

                if filename.lower().replace('.md', '').replace('.txt', '') in response.lower():
                    print("✅ AI found and referenced the specific file")
                else:
                    print("⚠️  AI didn't specifically reference this file")

            except Exception as e:
                print(f"❌ Error: {e}")


def show_uploaded_files_summary():
    """Show summary of uploaded files and their content"""

    print("\n📊 Uploaded Files Summary")
    print("=" * 50)

    file_manager = FileManager()
    files = file_manager.list_files()

    if not files:
        print("📁 No files uploaded yet.")
        print("💡 Upload files via: http://localhost:5000/files-manager")
        return

    print(f"📁 Total files: {len(files)}")

    # Group by category
    categories = {}
    for file_info in files:
        category = file_info.get('category', 'Uncategorized')
        if category not in categories:
            categories[category] = []
        categories[category].append(file_info)

    for category, category_files in categories.items():
        print(f"\n📂 {category}: {len(category_files)} files")
        for file_info in category_files:
            print(f"   📄 {file_info['filename']} ({file_info['file_type']})")
            if file_info.get('chunk_count', 0) > 1:
                print(f"      🔧 {file_info['chunk_count']} chunks (large file)")

    # Show some content examples
    print(f"\n📄 Sample Content from Files:")
    for file_info in files[:2]:  # Show content from first 2 files
        try:
            content = file_manager.get_file_content(file_info['file_id'])
            if not content.get('error'):
                print(f"\n📋 {file_info['filename']}:")
                print(f"   {content['content'][:200]}...")
        except Exception as e:
            print(f"   ❌ Error reading {file_info['filename']}: {e}")


def main():
    """Main test function"""

    print("🚀 AI INTEGRATION TEST")
    print("Make sure you have uploaded some files first!")
    print("=" * 50)

    # Show uploaded files
    show_uploaded_files_summary()

    # Test AI integration
    test_ai_with_uploaded_files()

    # Test file-specific queries
    demonstrate_file_specific_queries()

    print("\n" + "=" * 50)
    print("✅ AI Integration Test Completed!")
    print("💡 Your AI model should now respond using uploaded file content")
    print("🌐 Test it live at: http://localhost:5000")
    print("=" * 50)


if __name__ == "__main__":
    main()
