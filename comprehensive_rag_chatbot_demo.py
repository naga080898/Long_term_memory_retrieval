#!/usr/bin/env python3
"""
Comprehensive demonstration of creating a RAG chatbot instance with user_id
and showcasing the powerful jinja dynamic injection capabilities.
"""

from rag_chat_example import RAGChatBot
from prompt_builder import render_template
from rag_system import RAGSystem
from rag_tool_executor import RAGToolExecutor
import json

def create_rag_chatbot_with_user():
    """
    Create a RAG chatbot instance with user_id and demonstrate initialization
    """
    print("🚀 Creating RAG Chatbot Instance")
    print("=" * 50)
    
    # Step 1: Define user ID
    user_id = "alice_demo"
    
    # Step 2: Create RAG chatbot with intelligent template
    print(f"👤 Creating chatbot for user: {user_id}")
    
    rag_chatbot = RAGChatBot(
        user_id=user_id,
        index_type="flat",  # Options: "flat", "ivf", "hnsw"
        template_path="prompt_templates/intelligent_rag_chat.yaml"
    )
    
    print("✅ RAG Chatbot successfully created!")
    print(f"   📁 User database: user_memory/{user_id}/")
    print(f"   🔧 Index type: flat")
    print(f"   📄 Template: intelligent_rag_chat.yaml with jinja injection")
    
    return rag_chatbot

def demonstrate_template_context():
    """
    Demonstrate how jinja dynamic injection works with different context variables
    """
    print("\n🎯 Jinja Dynamic Injection Demo")
    print("=" * 50)
    
    # Example 1: Basic context with user input and history
    basic_context = {
        "user_id": "alice_demo",
        "user_input": "What do I like to do for fun?",
        "chat_history": [
            {"role": "user", "content": "Hi there!"},
            {"role": "assistant", "content": "Hello Alice! How can I help you today?"}
        ]
    }
    
    print("📝 Basic Template Context:")
    print(json.dumps(basic_context, indent=2))
    
    # Example 2: Advanced context with retrieved documents
    advanced_context = {
        "user_id": "alice_demo",
        "user_input": "Tell me about my hobbies",
        "user_stats": {
            "num_documents": 5,
            "index_type": "flat",
            "database_path": "user_memory/alice_demo/"
        },
        "retrieved_documents": [
            {
                "doc_id": "doc_1",
                "similarity_score": 0.95,
                "document": "Alice loves hiking, photography, and reading science fiction novels.",
                "metadata": {"type": "hobbies", "added": "2024-01-15"}
            },
            {
                "doc_id": "doc_2", 
                "similarity_score": 0.87,
                "document": "Alice enjoys cooking Italian food and trying new restaurants.",
                "metadata": {"type": "interests", "added": "2024-01-16"}
            }
        ],
        "recent_operations": [
            {
                "timestamp": "2024-01-16 10:30",
                "operation": "ADD_DOCUMENT",
                "description": "Added cooking preferences"
            }
        ],
        "chat_history": []
    }
    
    print("\n📝 Advanced Template Context (with retrieved docs):")
    print(json.dumps(advanced_context, indent=2, default=str))
    
    # Render the template with advanced context
    try:
        print("\n🔄 Rendering template with jinja injection...")
        rendered_messages = render_template("prompt_templates/intelligent_rag_chat.yaml", advanced_context)
        
        print("✅ Template rendered successfully!")
        print(f"📊 Generated {len(rendered_messages)} message(s)")
        
        # Show the rendered system message (with injected data)
        if rendered_messages:
            system_msg = rendered_messages[0]
            print("\n📄 Rendered System Message (first 500 chars):")
            print("-" * 50)
            print(system_msg['content'][:500] + "...")
            print("-" * 50)
            
    except Exception as e:
        print(f"❌ Template rendering error: {e}")

def simulate_chatbot_workflow():
    """
    Simulate a complete chatbot workflow showing how jinja injection works in practice
    """
    print("\n💬 Chatbot Workflow Simulation")
    print("=" * 50)
    
    # Create chatbot
    chatbot = create_rag_chatbot_with_user()
    
    # Simulate conversation with automatic document management
    conversations = [
        "Hi! My name is Alice and I work as a software engineer at TechCorp.",
        "I love hiking and photography in my free time.",
        "What hobbies do I have?",
        "I also enjoy cooking, especially Italian cuisine.",
        "What do you know about my work and interests?"
    ]
    
    print("\n🎭 Simulating conversation...")
    for i, user_input in enumerate(conversations, 1):
        print(f"\n--- Conversation Turn {i} ---")
        print(f"👤 User: {user_input}")
        
        # Show how template context would be built (simplified)
        print("🔧 Building template context...")
        context = chatbot._build_template_context(user_input)
        
        print(f"   📊 Context includes:")
        print(f"   - user_id: {context.get('user_id', 'None')}")
        print(f"   - chat_history: {len(context.get('chat_history', []))} messages")
        print(f"   - user_input: '{user_input[:50]}...'")
        
        # Simulate the actual chat (comment out to avoid API calls)
        # response = chatbot.chat(user_input)
        # print(f"🤖 Assistant: {response}")
        
        print("✅ Template would be rendered with jinja injection")

def show_template_features():
    """
    Highlight the key jinja template features
    """
    print("\n🌟 Jinja Template Features")
    print("=" * 50)
    
    features = [
        {
            "feature": "User ID Injection",
            "syntax": "{{ user_id }}",
            "purpose": "Personalizes messages with specific user context"
        },
        {
            "feature": "Conditional Blocks", 
            "syntax": "{% if user_stats %}...{% endif %}",
            "purpose": "Shows content only when data is available"
        },
        {
            "feature": "Loop Constructs",
            "syntax": "{% for doc in retrieved_documents %}...{% endfor %}",
            "purpose": "Iterates over retrieved documents or chat history"
        },
        {
            "feature": "Filters",
            "syntax": "{{ doc.similarity_score | format('%.3f') }}",
            "purpose": "Formats data (e.g., numbers, JSON, escaping)"
        },
        {
            "feature": "Nested Data Access",
            "syntax": "{{ doc.metadata.type }}",
            "purpose": "Accesses nested dictionary/object properties"
        },
        {
            "feature": "Safe Output",
            "syntax": "{{ content | tojson }}",
            "purpose": "Safely outputs content with proper escaping"
        }
    ]
    
    for feature in features:
        print(f"🔹 {feature['feature']}")
        print(f"   Syntax: {feature['syntax']}")
        print(f"   Purpose: {feature['purpose']}")
        print()

def main():
    """
    Main demonstration function
    """
    print("🎨 RAG Chatbot with Jinja Dynamic Injection")
    print("=" * 60)
    
    # Create chatbot instance
    chatbot = create_rag_chatbot_with_user()
    
    # Show template context demonstration
    demonstrate_template_context()
    
    # Show template features
    show_template_features()
    
    # Simulate workflow
    simulate_chatbot_workflow()
    
    print("\n🎯 Key Takeaways:")
    print("=" * 50)
    print("✅ RAGChatBot(user_id) creates a personalized chatbot instance")
    print("✅ Jinja templating enables dynamic content injection")
    print("✅ Templates support conditionals, loops, and data formatting")
    print("✅ Context includes user_id, chat history, retrieved docs, and stats")
    print("✅ prompt_builder.render_template() handles the jinja processing")
    print("✅ Templates are stored in prompt_templates/ directory")
    
    print(f"\n📁 User database created at: user_memory/{chatbot.user_id}/")
    print("🚀 Ready for production use!")

if __name__ == "__main__":
    main()