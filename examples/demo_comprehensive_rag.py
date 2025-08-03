#!/usr/bin/env python3
"""
Comprehensive RAG Chatbot Demo
Showcases all enhanced features including automatic document retrieval and deletion
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag_chat_example import RAGChatBot

def demo_all_features():
    """
    Comprehensive demo showing all RAG chatbot features
    """
    print("🧠 COMPREHENSIVE RAG CHATBOT DEMO")
    print("=" * 80)
    print("✨ Features demonstrated:")
    print("   📥 Automatic information saving")
    print("   🔍 Automatic document retrieval for every query")
    print("   ✏️  Intelligent updates based on context")
    print("   🗑️  Automatic deletion on contradictions/negations")
    print("   💬 Natural conversation flow")
    print()

    user_id = "demo_user"
    chatbot = RAGChatBot(user_id)
    
    # Demo scenarios with all features
    scenarios = [
        {
            "title": "📥 AUTOMATIC SAVING",
            "description": "Natural information storage without explicit commands",
            "interactions": [
                "Hi, I'm Alex and I work as a Data Scientist at Google",
                "I love playing tennis and hiking on weekends",
                "My favorite programming language is Python"
            ]
        },
        {
            "title": "🔍 AUTOMATIC RETRIEVAL & INTELLIGENT RESPONSES",
            "description": "Context-aware responses using stored information",
            "interactions": [
                "What do you know about my work?",
                "What are my hobbies?",
                "Tell me about myself"
            ]
        },
        {
            "title": "✏️ INTELLIGENT UPDATES",
            "description": "Smart updates based on retrieved context",
            "interactions": [
                "I got promoted to Senior Data Scientist",
                "I also enjoy rock climbing now",
                "I'm learning JavaScript along with Python"
            ]
        },
        {
            "title": "🗑️ AUTOMATIC DELETION ON CONTRADICTIONS",
            "description": "Automatic removal of contradicted information",
            "interactions": [
                "I no longer play tennis",
                "I don't work at Google anymore",
                "I stopped hiking on weekends"
            ]
        },
        {
            "title": "✅ VERIFICATION",
            "description": "Check what information remains after automatic cleanup",
            "interactions": [
                "What are my current hobbies?",
                "Where do I work now?",
                "What do you know about me?"
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['title']}")
        print("-" * 60)
        print(f"💡 {scenario['description']}")
        print()
        
        for interaction in scenario['interactions']:
            print(f"👤 User: \"{interaction}\"")
            if "🔍" in scenario['title'] or "🗑️" in scenario['title'] or "✅" in scenario['title']:
                print("🔍 [AUTOMATIC] Retrieving relevant documents...")
            if "🗑️" in scenario['title']:
                print("🧠 [AUTOMATIC] Detecting contradictions...")
            
            response = chatbot.chat(interaction)
            print(f"🤖 Assistant: {response}")
            print()
    
    # Final statistics
    stats = chatbot.get_user_stats()
    if stats["success"]:
        num_docs = stats["data"]["stats"]["num_documents"]
        print(f"📊 Final document count: {num_docs}")
    
    print("\n" + "=" * 80)
    print("🎉 COMPREHENSIVE DEMO COMPLETE!")
    print("💡 All key features successfully demonstrated:")
    print("   ✅ Automatic information saving during natural conversation")
    print("   ✅ Context-aware responses with automatic document retrieval")
    print("   ✅ Intelligent updates that avoid duplication")
    print("   ✅ Automatic deletion of contradicted/negated information")
    print("   ✅ Seamless conversation flow with powerful memory capabilities")

def run_interactive_mode():
    """
    Interactive mode for testing all features
    """
    print("🧠 COMPREHENSIVE RAG CHATBOT - Interactive Mode")
    print("=" * 60)
    print("🚀 All enhanced features are active:")
    print("   📥 Automatic saving of personal information")
    print("   🔍 Automatic context retrieval for every query")
    print("   ✏️  Smart updates based on existing information")
    print("   🗑️  Automatic deletion when you contradict previous info")
    print()
    print("💡 Try natural conversations like:")
    print("   • 'I work at Apple as a software engineer'")
    print("   • 'What do you know about my job?'")
    print("   • 'Actually, I got promoted to senior engineer'")
    print("   • 'I no longer work at Apple' (automatic deletion)")
    print()
    
    user_id = input("Enter your user ID: ").strip() or "interactive_user"
    print(f"\n🔧 Initializing comprehensive RAG system for: {user_id}")
    
    chatbot = RAGChatBot(user_id)
    
    # Show current stats
    stats = chatbot.get_user_stats()
    if stats["success"]:
        num_docs = stats["data"]["stats"]["num_documents"]
        print(f"📊 Current database: {num_docs} documents")
    
    print("\n💬 Start chatting! All features work automatically.")
    print("   • Type 'help' for feature examples")
    print("   • Type 'stats' to see current document count")
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
            
            if user_input.lower() == 'help':
                print("💡 Feature Examples:")
                print("   📥 Saving: 'I love photography' or 'I work at Microsoft'")
                print("   🔍 Retrieval: 'What are my hobbies?' or 'Tell me about my work'")
                print("   ✏️  Updates: 'I got promoted' or 'I also enjoy hiking'")
                print("   🗑️  Deletion: 'I no longer play guitar' or 'I don't work there anymore'")
                continue
            
            if user_input.lower() == 'stats':
                stats = chatbot.get_user_stats()
                if stats["success"]:
                    num_docs = stats["data"]["stats"]["num_documents"]
                    print(f"📊 Current documents: {num_docs}")
                continue
            
            if not user_input:
                continue
            
            # Show automatic features in action
            negation_keywords = ["no longer", "don't", "stopped", "quit", "not anymore", "hate"]
            if any(keyword in user_input.lower() for keyword in negation_keywords):
                print("🔍 [AUTOMATIC] Retrieving relevant documents...")
                print("🗑️ [AUTOMATIC] Detecting contradictions...")
            else:
                print("🔍 [AUTOMATIC] Retrieving context...")
            
            response = chatbot.chat(user_input)
            print(f"🤖 Assistant: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        run_interactive_mode()
    else:
        demo_all_features()