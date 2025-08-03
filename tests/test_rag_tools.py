"""
Test script for RAG tools - demonstrates individual tool usage
"""

import json
from rag_tool_executor import RAGToolExecutor
from rag_system import RAGSystem


def test_crud_operations():
    """Test all CRUD operations step by step"""
    print("🧪 Testing RAG CRUD Operations")
    print("=" * 50)
    
    # Initialize RAG system and executor
    rag_system = RAGSystem(index_type="flat")
    executor = RAGToolExecutor(rag_system)
    
    user_id = "test_user"
    
    # Test 1: Add documents
    print("\n1. 📝 Adding Documents")
    documents = [
        {
            "document": "I love programming in Python. It's my favorite language for data science and web development.",
            "metadata": {"category": "preferences", "topic": "programming"}
        },
        {
            "document": "I work at TechCorp as a Senior Software Engineer. I joined the company in 2022.",
            "metadata": {"category": "work", "topic": "employment"}
        },
        {
            "document": "My favorite foods are pizza, sushi, and chocolate. I'm also a coffee enthusiast.",
            "metadata": {"category": "preferences", "topic": "food"}
        },
        {
            "document": "I have a meeting with the product team every Monday at 10 AM to discuss roadmap.",
            "metadata": {"category": "schedule", "topic": "meetings"}
        }
    ]
    
    doc_ids = []
    for i, doc_data in enumerate(documents):
        result = executor.execute_tool("add_document", {
            "user_id": user_id,
            "document": doc_data["document"],
            "metadata": doc_data["metadata"]
        })
        print(f"   Added document {i+1}: {result['data']['doc_id']}")
        doc_ids.append(result['data']['doc_id'])
    
    # Test 2: Search documents
    print("\n2. 🔍 Searching Documents")
    search_queries = [
        "What programming languages do I like?",
        "Where do I work?",
        "What are my favorite foods?",
        "When do I have meetings?"
    ]
    
    for query in search_queries:
        result = executor.execute_tool("search_documents", {
            "user_id": user_id,
            "query": query,
            "top_k": 2
        })
        print(f"\n   Query: '{query}'")
        if result['success'] and result['data']['results']:
            for res in result['data']['results'][:1]:  # Show top result
                print(f"   → {res['doc_id']}: {res['document'][:60]}... (score: {res['similarity_score']:.3f})")
        else:
            print("   → No results found")
    
    # Test 3: Update document
    print("\n3. ✏️  Updating Document")
    update_result = executor.execute_tool("update_document", {
        "user_id": user_id,
        "doc_id": doc_ids[1],  # Update work document
        "new_document": "I work at TechCorp as a Senior Software Engineer. I joined in 2022 and recently got promoted to Tech Lead.",
        "new_metadata": {"category": "work", "topic": "employment", "status": "updated"}
    })
    print(f"   Update result: {update_result['data']['message']}")
    
    # Test 4: Search again to see updated content
    print("\n4. 🔍 Searching After Update")
    result = executor.execute_tool("search_documents", {
        "user_id": user_id,
        "query": "What is my role at work?",
        "top_k": 1
    })
    if result['success'] and result['data']['results']:
        res = result['data']['results'][0]
        print(f"   → Updated document: {res['document']}")
    
    # Test 5: Get statistics
    print("\n5. 📊 Database Statistics")
    stats_result = executor.execute_tool("get_database_stats", {"user_id": user_id})
    if stats_result['success']:
        stats = stats_result['data']['stats']
        print(f"   User: {stats['user_id']}")
        print(f"   Documents: {stats['num_documents']}")
        print(f"   Index type: {stats['index_type']}")
        print(f"   Dimension: {stats['dimension']}")
    
    # Test 6: Delete document
    print("\n6. 🗑️  Deleting Document")
    delete_result = executor.execute_tool("delete_document", {
        "user_id": user_id,
        "doc_id": doc_ids[-1]  # Delete last document
    })
    print(f"   Delete result: {delete_result['data']['message']}")
    
    # Test 7: Final statistics
    print("\n7. 📊 Final Statistics")
    final_stats = executor.execute_tool("get_database_stats", {"user_id": user_id})
    if final_stats['success']:
        stats = final_stats['data']['stats']
        print(f"   Documents remaining: {stats['num_documents']}")
    
    print("\n✅ CRUD operations test completed!")
    return executor


def test_database_management():
    """Test database save/load operations"""
    print("\n🗄️  Testing Database Management")
    print("=" * 30)
    
    # Use the executor from CRUD test
    executor = test_crud_operations()
    user_id = "test_user"
    
    # Save database
    print("\n1. 💾 Saving Database")
    save_result = executor.execute_tool("save_database", {})
    print(f"   Save result: {save_result['data']['message']}")
    
    # List users
    print("\n2. 👥 Listing Users")
    list_result = executor.execute_tool("list_users", {})
    if list_result['success']:
        users = list_result['data']['users']
        print(f"   Found users: {users}")
    
    # Get user directory info
    print("\n3. 📁 User Directory Info")
    info_result = executor.execute_tool("get_user_directory_info", {"user_id": user_id})
    if info_result['success']:
        info = info_result['data']['info']
        print(f"   Directory: {info['directory']}")
        print(f"   Files: {[f['name'] for f in info['files']]}")
    
    # Test save documents only
    print("\n4. 📄 Saving Documents Only")
    docs_result = executor.execute_tool("save_documents_only", {"user_id": user_id})
    if docs_result['success']:
        print(f"   Saved to: {docs_result['data']['file_path']}")
    
    # Test load documents only
    print("\n5. 📖 Loading Documents Only")
    if docs_result['success']:
        load_result = executor.execute_tool("load_documents_only", {
            "file_path": docs_result['data']['file_path']
        })
        if load_result['success']:
            print(f"   Loaded {load_result['data']['num_documents']} documents")
            print(f"   Document IDs: {load_result['data']['document_ids']}")
    
    print("\n✅ Database management test completed!")


def test_tool_call_format():
    """Test tool call in OpenAI function calling format"""
    print("\n🔧 Testing OpenAI Tool Call Format")
    print("=" * 40)
    
    from rag_tool_executor import process_tool_call
    
    # Initialize executor
    rag_system = RAGSystem()
    executor = RAGToolExecutor(rag_system)
    
    # Simulate OpenAI tool call format
    tool_call = {
        "id": "call_123",
        "type": "function",
        "function": {
            "name": "add_document",
            "arguments": json.dumps({
                "user_id": "format_test_user",
                "document": "This is a test document for format testing.",
                "metadata": {"test": True, "format": "openai"}
            })
        }
    }
    
    print("Tool call:")
    print(json.dumps(tool_call, indent=2))
    
    # Process tool call
    result = process_tool_call(tool_call, executor)
    print("\nResult:")
    print(result)
    
    print("\n✅ Tool call format test completed!")


def test_error_handling():
    """Test error handling for various scenarios"""
    print("\n❌ Testing Error Handling")
    print("=" * 30)
    
    executor = RAGToolExecutor()
    
    # Test 1: Invalid tool name
    result = executor.execute_tool("invalid_tool", {})
    print(f"1. Invalid tool: {result['success']} - {result['error']}")
    
    # Test 2: Missing required arguments
    result = executor.execute_tool("add_document", {"user_id": "test"})  # Missing document
    print(f"2. Missing args: {result['success']} - {result['error']}")
    
    # Test 3: Invalid document ID for update
    result = executor.execute_tool("update_document", {
        "user_id": "test_user",
        "doc_id": "nonexistent_doc",
        "new_document": "test"
    })
    print(f"3. Invalid doc ID: {result['success']} - Updated: {result['data']['updated']}")
    
    # Test 4: Delete non-existent document
    result = executor.execute_tool("delete_document", {
        "user_id": "test_user",
        "doc_id": "nonexistent_doc"
    })
    print(f"4. Delete non-existent: {result['success']} - Deleted: {result['data']['deleted']}")
    
    print("\n✅ Error handling test completed!")


if __name__ == "__main__":
    print("🚀 RAG Tools Test Suite")
    print("=" * 60)
    
    # Run all tests
    test_crud_operations()
    test_database_management()
    test_tool_call_format()
    test_error_handling()
    
    print("\n🎉 All tests completed!")
    print("=" * 60)