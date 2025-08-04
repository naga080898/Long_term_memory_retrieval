#!/usr/bin/env python3
"""
Example script demonstrating how to create a RAG chatbot instance 
with user_id and jinja dynamic injection using the prompt_builder.
"""

from rag_chat_example import RAGChatBot
from prompt_builder import render_template

def create_rag_chatbot_instance():
    """
    Create a RAG chatbot instance by passing user_id with jinja dynamic injection
    """
    
    # Define a user ID
    user_id = "example_user_123"
    
    # Option 1: Create RAG chatbot with default template (intelligent_rag_chat.yaml)
    print("Creating RAG chatbot with default template...")
    rag_chatbot = RAGChatBot(
        user_id=user_id,
        index_type="flat",  # Options: "flat", "ivf", "hnsw"
        template_path="prompt_templates/intelligent_rag_chat.yaml"  # Uses jinja templating
    )
    
    print(f"✅ RAG chatbot created for user: {user_id}")
    print(f"📁 Database path: user_memory/{user_id}/")
    print(f"🔧 Index type: flat")
    print(f"📄 Template: prompt_templates/intelligent_rag_chat.yaml")
    
    # Option 2: Create with simple Q&A template
    print("\nCreating RAG chatbot with simple Q&A template...")
    simple_rag_chatbot = RAGChatBot(
        user_id=user_id,
        index_type="flat",
        template_path="prompt_templates/simple_qa.yaml"  # Alternative template
    )
    
    print(f"✅ Simple RAG chatbot created for user: {user_id}")
    
    return rag_chatbot, simple_rag_chatbot

def demonstrate_jinja_templating():
    """
    Demonstrate how the prompt_builder uses jinja dynamic injection
    """
    print("\n=== Jinja Dynamic Injection Demo ===")
    
    # Example context data that gets injected into templates
    context = {
        "user_input": "What documents do I have?",
        "chat_history": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi! How can I help you today?"}
        ],
        "user_id": "example_user_123",
        "available_tools": ["search_documents", "add_document", "delete_document"]
    }
    
    # Render template with jinja injection
    try:
        rendered_messages = render_template("prompt_templates/simple_qa.yaml", context)
        print("🎯 Template rendering successful!")
        print("📝 Rendered messages structure:")
        for i, msg in enumerate(rendered_messages):
            print(f"  Message {i+1}: {msg['role']} - {msg['content'][:50]}...")
    except Exception as e:
        print(f"❌ Template rendering error: {e}")

def example_usage():
    """
    Example of using the RAG chatbot with dynamic templating
    """
    print("\n=== RAG Chatbot Usage Example ===")
    
    # Create chatbot instance
    user_id = "demo_user"
    chatbot = RAGChatBot(user_id=user_id)
    
    # Add some sample documents
    print("📚 Adding sample documents...")
    sample_docs = [
        "Python is a high-level programming language known for its simplicity and readability.",
        "Machine learning is a subset of artificial intelligence that enables computers to learn.",
        "RAG (Retrieval-Augmented Generation) combines information retrieval with text generation."
    ]
    
    # The chatbot automatically handles document addition through its tool system
    for i, doc in enumerate(sample_docs):
        response = chatbot.chat(f"Please save this information: {doc}")
        print(f"  Document {i+1} processed")
    
    # Now query the chatbot - it will use jinja templating and RAG
    print("\n💬 Chatting with RAG-enabled bot...")
    questions = [
        "What is Python?",
        "Tell me about machine learning",
        "What documents do I have about programming?"
    ]
    
    for question in questions:
        print(f"\n👤 User: {question}")
        response = chatbot.chat(question)
        print(f"🤖 Assistant: {response}")
        print("-" * 50)

if __name__ == "__main__":
    print("🚀 RAG Chatbot Creation Example")
    print("=" * 50)
    
    # Create RAG chatbot instances
    chatbot1, chatbot2 = create_rag_chatbot_instance()
    
    # Demonstrate jinja templating
    demonstrate_jinja_templating()
    
    # Show example usage
    example_usage()
    
    print("\n✨ Example completed!")
    print("\nKey points:")
    print("- RAGChatBot automatically creates user databases")
    print("- Uses prompt_builder.render_template() for jinja injection")
    print("- Templates are in prompt_templates/ directory")
    print("- Supports multiple index types (flat, ivf, hnsw)")
    print("- Integrates with OpenAI function calling")