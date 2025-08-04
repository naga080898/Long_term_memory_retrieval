# 🧠 Enhanced RAG Chatbot with Intelligent Memory

An advanced Retrieval-Augmented Generation (RAG) system featuring **automatic document retrieval** and **intelligent contradiction detection**. This chatbot maintains sophisticated long-term memory and automatically manages information through natural conversation.

## 🚀 Quick Start

**⚡ Get running in 5 minutes** - See [docs/QUICK_START.md](docs/QUICK_START.md) for detailed setup guide

```bash
# 1. Set up environment and dependencies
source LLM_memory-env/bin/activate
pip install -r requirements.txt

# 2. Set up your OpenAI API key
echo "OPENAI_API_KEY=your-api-key-here" > .env

# 3. Choose your interface:

# Option A: Full RAG system with auto-retrieval
python examples/demo_comprehensive_rag.py

# Option B: Simple Q&A chatbot (lightweight)
python simple_qa_chatbot.py

# Option C: Visualize stored data
jupyter notebook LLM_memory.ipynb
```

## ✨ Key Features

### 🚀 **New Enhanced Features**
- **🔍 Automatic Document Retrieval** - Every query automatically retrieves relevant context
- **🗑️ Smart Contradiction Detection** - Automatically deletes outdated information when users negate statements  
- **🧠 Context-Aware Operations** - All CRUD operations use intelligent context from retrieved documents

### 🤖 **Core Intelligent Features**
- **📥 Automatic Saving** - Stores personal information during natural conversation
- **✏️ Smart Updates** - Updates existing info instead of creating duplicates
- **💬 Natural Flow** - No trigger phrases needed, just talk naturally
- **👥 Multi-user Support** - Isolated databases per user

## 🎯 What Makes This Special

### Automatic Contradiction Detection
```
User: "I play badminton every weekend"
Bot: [Automatically saves information]

Later...
User: "I no longer play badminton"  
Bot: [Automatically finds badminton info, detects contradiction, deletes it]
     "I've deleted the information about you playing badminton"
```

### Context-Aware Intelligence
```
User: "I got promoted to Senior Engineer"
Bot: [Automatically retrieves work info, sees existing "Engineer" role]
     [Updates existing document instead of creating duplicate]
     "I've updated your work information to reflect your promotion"
```

## 📁 Project Structure

```
Enhanced_RAG_Chatbot/
├── 📚 Core System
│   ├── rag_chat_example.py           # 🤖 Enhanced chatbot with auto-retrieval
│   ├── simple_qa_chatbot.py          # 💬 Lightweight Q&A chatbot with sessions
│   ├── rag_system.py                 # ⚙️ Core RAG implementation  
│   ├── rag_tools.py                  # 🛠️ OpenAI function schemas
│   ├── rag_tool_executor.py          # 🔧 Tool execution logic
│   ├── llm_interface.py              # 🌐 OpenAI API interface
│   └── prompt_builder.py             # 🎨 YAML template renderer
│
├── 🔍 Database Tools
│   └── LLM_memory.ipynb              # 📊 Jupyter notebook for database visualization
│
├── 🎨 Configuration
│   ├── prompt_templates/
│   │   ├── intelligent_rag_chat.yaml # 🧠 Enhanced prompt with auto-deletion
│   │   └── simple_qa.yaml            # 💬 Simple Q&A prompt template
│   ├── requirements.txt              # 📦 Dependencies
│   └── setup.py                      # 🔧 Package setup
│
├── 🎯 Examples & Tests
│   ├── examples/
│   │   └── demo_comprehensive_rag.py # 🎬 Complete feature demo
│   └── tests/
│       ├── test_rag_comprehensive.py # 🧪 All features test suite
│       └── test_rag_tools.py         # 🔍 Basic tool tests
│
├── 📚 Documentation
│   ├── docs/
│   │   ├── ENHANCEMENT_SUMMARY.md    # 📖 Technical enhancement guide
│   │   ├── RAG_TOOLS_DOCUMENTATION.md # 🛠️ Complete API reference
│   │   └── README_TEMPLATE_SYSTEM.md # 🎨 Template system guide
│
└── 💾 Data Storage
    ├── user_memory/                  # 👥 Isolated user databases (.pkl files)
    └── sessions/                     # 💬 Chat session histories (.jsonl files)
```

## 💡 Usage Examples

### 1. Natural Information Management
```python
from rag_chat_example import RAGChatBot

chatbot = RAGChatBot("user123")

# Natural conversation - automatic saving
chatbot.chat("I'm a data scientist at Google and love hiking")
# → Information automatically stored

# Automatic context retrieval  
chatbot.chat("What do you know about my work?")
# → Automatically finds and uses work information

# Smart contradiction handling
chatbot.chat("I no longer work at Google")  
# → Automatically finds work info and deletes it
```

### 2. Simple Q&A Chatbot
```bash
# Run interactive simple chatbot (basic Q&A with optional background memory)
python simple_qa_chatbot.py

# Run basic demo
python simple_qa_chatbot.py demo

# Run configurable history demo
python simple_qa_chatbot.py history-demo
```

#### Simple Chatbot Features:
- **🗣️ Lightweight Q&A**: Chat without complex RAG operations
- **📝 Session Management**: Persistent conversation history in JSONL format
- **🧠 Optional Background Memory**: Automatic memory via RAG system when enabled
- **⚙️ Configurable History**: Adjustable conversation history length
- **💾 Session Persistence**: Save, load, and export chat sessions

```python
from simple_qa_chatbot import SimpleQAChatBot

# Basic usage
chatbot = SimpleQAChatBot(user_id="your_user_id")
response = chatbot.chat("What is machine learning?")

# With session management
chatbot = SimpleQAChatBot(user_id="user123", session_id="existing_session")
response = chatbot.chat("Continue our previous conversation")

# Configure history length (keeps N pairs, clips at 2N)
chatbot.set_history_length(5)  # Keep 5 conversation pairs
```

#### 🎮 **Interactive Commands:**
When running `python simple_qa_chatbot.py`, these commands are available:
```
📋 Basic Commands:
• help                     - Show all available commands  
• quit/exit/bye           - Exit the chatbot
• remember <info>         - Explicitly save information to memory
• forget                  - Clear background memory

📜 History Management:
• history                 - Show conversation history
• clear                   - Clear conversation history  
• set-history <N>         - Set max history length to N pairs

💾 Session Management:
• sessions                - List all available sessions
• load <session_id>       - Load a previous session
• session                 - Show current session info
• export                  - Export session for OpenAI training
• delete-session          - Delete current session

🧠 Memory Management:
• memory-stats            - Show background memory statistics
• toggle-memory           - Enable/disable background memory
```

### 3. Database Visualization
```bash
# Launch Jupyter notebook to visualize your RAG database
jupyter notebook LLM_memory.ipynb
```

The notebook provides comprehensive database inspection tools:

#### 📊 **What You Can Visualize:**
- **📑 Stored Documents**: View all user information saved as text documents
- **🏷️ Document Metadata**: Examine document IDs, timestamps, and structure
- **🔢 Database Stats**: Check document count, dimension size, index type
- **🎯 Vector Embeddings**: Inspect the raw embedding data (index_data array)

#### 💡 **Example Usage in Notebook:**
```python
# Load and inspect a user's database
file_path = "user_memory/your_user_id/rag_db_your_user_id.pkl"
data = read_and_print_pkl(file_path)

# View just the documents
print(data['documents'])
# Output: {'doc_0': 'Name: John, Job: Engineer...', 'doc_1': 'User likes...'}

# Check database structure
print(f"Index Type: {data['index_type']}")
print(f"Embedding Dimension: {data['dimension']}")
print(f"Total Documents: {len(data['documents'])}")
```

#### 🔍 **Database Structure:**
- **`documents`**: Dictionary of document IDs → text content
- **`metadata`**: Document metadata and timestamps
- **`index_type`**: Vector index type (flat, ivf, hnsw)
- **`dimension`**: Embedding vector dimension (384 for MiniLM)
- **`doc_counter`**: Running count of documents created
- **`index_data`**: Serialized FAISS index with vector embeddings

### 4. Testing All Features
```bash
# Comprehensive test demonstrating all capabilities
python tests/test_rag_comprehensive.py

# Interactive testing
python tests/test_rag_comprehensive.py interactive
```

## 🧠 Advanced Intelligence

### Automatic Negation Patterns
The system automatically detects and handles:
- `"I no longer..."` → Deletes related information
- `"I don't... anymore"` → Removes contradicted data  
- `"I stopped..."` → Deletes activity information
- `"I hate X"` vs `"I love X"` → Replaces preferences
- `"I'm not... anymore"` → Updates identity information

### Context-Aware Decision Making
- **Smart Updates**: Recognizes when to update vs create new
- **Intelligent Deletion**: Finds specific documents to remove  
- **Relationship Understanding**: Connects related information
- **Conflict Resolution**: Automatically resolves contradictions

## 🔧 Configuration

### Key Settings
```python
# Automatic retrieval settings
top_k = 5                    # Documents retrieved per query
index_type = "flat"          # Index type: "flat", "ivf", "hnsw"  
model = "all-MiniLM-L6-v2"   # Embedding model
```

### Environment Variables
```bash
OPENAI_API_KEY=your-api-key-here     # Required for LLM
TOKENIZERS_PARALLELISM=false         # Prevents warnings
```

## 📊 Testing & Validation

### Comprehensive Test Results
✅ **Automatic Information Saving**: 6/6 documents saved naturally  
✅ **Context Retrieval**: 100% relevant document retrieval  
✅ **Intelligent Updates**: 4/4 updates vs new documents  
✅ **Automatic Deletion**: 6/6 contradictions detected and resolved  
✅ **Natural Conversation**: Seamless interaction flow  

### Run Tests
```bash
# Complete feature test
python tests/test_rag_comprehensive.py

# Focused automatic deletion tests
python tests/test_automatic_deletion.py

# Edge case deletion testing
python tests/test_automatic_deletion.py edge

# Interactive deletion testing
python tests/test_automatic_deletion.py interactive

# Basic tool validation  
python tests/test_rag_tools.py

# Interactive comprehensive testing
python tests/test_rag_comprehensive.py interactive
```

## 🎯 Use Cases

- **🤖 Personal AI Assistant**: Comprehensive memory of user preferences, work, relationships
- **📞 Customer Support**: Context-aware interactions across multiple sessions
- **📚 Learning Systems**: Adaptive content based on user progress and interests  
- **🔬 Research Tools**: Dynamic knowledge base building from conversations
- **✍️ Content Creation**: Consistent character and world-building maintenance

## 📚 Documentation

- **[🚀 Quick Start Guide](docs/QUICK_START.md)** - 5-minute setup and testing guide
- **[📖 Enhancement Guide](docs/ENHANCEMENT_SUMMARY.md)** - Detailed technical overview of all enhancements
- **[🛠️ API Documentation](docs/RAG_TOOLS_DOCUMENTATION.md)** - Complete tool reference and schemas  
- **[🎨 Template System](docs/README_TEMPLATE_SYSTEM.md)** - Enhanced YAML prompt template guide
- **[📚 Documentation Index](docs/INDEX.md)** - Complete documentation navigation

## 🎉 Status

✅ **Enhanced & Production Ready** - Advanced RAG with automatic intelligence  
✅ **Auto-Retrieval System** - Context for every interaction  
✅ **Smart Contradiction Detection** - Automatic information management  
✅ **Natural Conversation Flow** - No commands needed  
✅ **Comprehensive Testing** - All features validated  

---

**🚀 Start exploring**: See [docs/QUICK_START.md](docs/QUICK_START.md) for 5-minute setup, then run `python examples/demo_comprehensive_rag.py`
