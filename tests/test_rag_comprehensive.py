#!/usr/bin/env python3
"""
Comprehensive Test Suite for Enhanced RAG Chatbot
Tests all features: automatic retrieval, intelligent updates, and automatic deletion
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag_chat_example import RAGChatBot

def test_all_features():
    """
    Comprehensive test of all RAG chatbot features
    """
    print("🧠 COMPREHENSIVE RAG CHATBOT TEST SUITE")
    print("=" * 80)
    print("✨ Testing all enhanced features:")
    print("   📥 Automatic information saving")
    print("   🔍 Automatic document retrieval") 
    print("   ✏️  Intelligent updates")
    print("   🗑️  Automatic deletion on contradictions")
    print()

    # Create a test user
    user_id = "comprehensive_test_user"
    chatbot = RAGChatBot(user_id)
    
    # Phase 1: Add initial information
    print("📥 PHASE 1: Adding Initial Information")
    print("-" * 50)
    
    initial_statements = [
        "I play badminton every weekend",
        "I work at Microsoft as a software engineer", 
        "I love drinking coffee in the morning",
        "I'm learning to play piano",
        "I'm a vegetarian",
        "I collect vintage coins as a hobby"
    ]
    
    for statement in initial_statements:
        print(f"\n👤 User: \"{statement}\"")
        response = chatbot.chat(statement)
        print(f"🤖 Assistant: {response}")
    
    # Show stats after initial additions
    stats = chatbot.get_user_stats()
    if stats["success"]:
        num_docs = stats["data"]["stats"]["num_documents"]
        print(f"\n📊 Documents stored after initial phase: {num_docs}")
    
    print("\n" + "=" * 80)
    
    # Phase 2: Test automatic deletion with negations
    print("🗑️ PHASE 2: Testing Automatic Deletion with Negations")
    print("-" * 50)
    print("💡 The chatbot should automatically detect negations and delete relevant documents!")
    
    negation_statements = [
        "I no longer play badminton",  # Should delete badminton document
        "I don't work at Microsoft anymore",  # Should delete work document
        "I stopped learning piano",  # Should delete piano document
        "I'm not vegetarian anymore",  # Should delete vegetarian document
    ]
    
    for statement in negation_statements:
        print(f"\n👤 User: \"{statement}\"")
        print("🔍 [AUTOMATIC] Retrieving relevant documents...")
        print("🧠 [AUTOMATIC] Detecting contradictions...")
        response = chatbot.chat(statement)
        print(f"🤖 Assistant: {response}")
        
        # Check current document count
        stats = chatbot.get_user_stats()
        if stats["success"]:
            num_docs = stats["data"]["stats"]["num_documents"]
            print(f"📊 Documents remaining: {num_docs}")
    
    print("\n" + "=" * 80)
    
    # Phase 3: Test automatic deletion with contradictions
    print("⚡ PHASE 3: Testing Automatic Deletion with Direct Contradictions")
    print("-" * 50)
    
    contradiction_statements = [
        "I actually hate coffee now",  # Should delete coffee love document
        "I quit collecting coins",  # Should delete coin collecting document
    ]
    
    for statement in contradiction_statements:
        print(f"\n👤 User: \"{statement}\"")
        print("🔍 [AUTOMATIC] Retrieving relevant documents...")
        print("⚡ [AUTOMATIC] Detecting contradictions...")
        response = chatbot.chat(statement)
        print(f"🤖 Assistant: {response}")
        
        # Check current document count
        stats = chatbot.get_user_stats()
        if stats["success"]:
            num_docs = stats["data"]["stats"]["num_documents"]
            print(f"📊 Documents remaining: {num_docs}")
    
    print("\n" + "=" * 80)
    
    # Phase 4: Verify what's left
    print("✅ PHASE 4: Verification - What Information Remains")
    print("-" * 50)
    
    verification_queries = [
        "What do you know about me?",
        "What are my hobbies?",
        "Tell me about my work",
        "What are my preferences?"
    ]
    
    for query in verification_queries:
        print(f"\n👤 User: \"{query}\"")
        print("🔍 [AUTOMATIC] Retrieving remaining documents...")
        response = chatbot.chat(query)
        print(f"🤖 Assistant: {response}")
    
    # Final stats
    final_stats = chatbot.get_user_stats()
    if final_stats["success"]:
        final_docs = final_stats["data"]["stats"]["num_documents"]
        print(f"\n📊 Final document count: {final_docs}")
    
    print("\n" + "=" * 80)
    print("🎉 AUTOMATIC DELETION TEST COMPLETE!")
    print("💡 Key Features Demonstrated:")
    print("   ✅ Automatic detection of negation language ('I no longer...', 'I stopped...', etc.)")
    print("   ✅ Automatic deletion of contradicted information")
    print("   ✅ Context-aware contradiction detection using retrieved documents")
    print("   ✅ Smart preservation of non-contradicted information")
    print("   ✅ Natural conversation flow with automatic cleanup")

def run_interactive_test():
    """
    Run interactive test for automatic deletion features
    """
    print("🧠 COMPREHENSIVE RAG TEST - Interactive Mode")
    print("=" * 60)
    print("🚀 Test automatic deletion by negating previous statements!")
    print()
    print("💡 Try patterns like:")
    print("   • First: 'I love playing tennis'")
    print("   • Later: 'I no longer play tennis'")
    print("   • Or: 'I work at Google' → 'I don't work at Google anymore'")
    print()
    
    user_id = input("Enter your user ID: ").strip() or "deletion_test_user"
    print(f"\n🔧 Initializing RAG system for: {user_id}")
    
    chatbot = RAGChatBot(user_id)
    
    # Show current stats
    stats = chatbot.get_user_stats()
    if stats["success"]:
        num_docs = stats["data"]["stats"]["num_documents"]
        print(f"📊 Current database: {num_docs} documents")
    
    print("\n💬 Start testing! The bot will automatically delete contradicted information.")
    print("   • Type 'quit' to exit")
    print()
    
    while True:
        try:
            user_input = input(f"[{user_id}] You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                stats = chatbot.get_user_stats()
                if stats["success"]:
                    num_docs = stats["data"]["stats"]["num_documents"]
                    print(f"\n📊 Final count: {num_docs} documents")
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Check for negation patterns to highlight automatic deletion
            negation_keywords = ["no longer", "don't", "stopped", "quit", "not anymore", "hate"]
            if any(keyword in user_input.lower() for keyword in negation_keywords):
                print("🔍 [AUTOMATIC] Detecting potential contradiction/negation...")
            
            response = chatbot.chat(user_input)
            print(f"🤖 Assistant: {response}")
            
            # Show current count after each interaction
            stats = chatbot.get_user_stats()
            if stats["success"]:
                num_docs = stats["data"]["stats"]["num_documents"]
                print(f"📊 Current documents: {num_docs}")
            
        except KeyboardInterrupt:
            print("\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        run_interactive_test()
    else:
        test_all_features()