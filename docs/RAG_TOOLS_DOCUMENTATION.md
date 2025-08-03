# RAG System Tools Documentation

This documentation covers the complete RAG (Retrieval-Augmented Generation) tools system with CRUD operations, designed for OpenAI function calling integration.

## 📁 File Overview

| File | Purpose |
|------|---------|
| `rag_tools.py` | Tool schemas in OpenAI function calling format |
| `rag_tool_executor.py` | Tool execution functions and utilities |
| `rag_chat_example.py` | Complete chatbot example with RAG tools |
| `test_rag_tools.py` | Individual tool testing and validation |
| `rag_system.py` | Core RAG system implementation (existing) |
| `llm_interface.py` | OpenAI API interface (existing) |

## 🛠️ Available Tools

### CRUD Operations

#### 1. Add Document
```python
tool_name: "add_document"
parameters:
  - user_id (required): User identifier
  - document (required): Text content to store
  - metadata (optional): Additional document metadata
```

#### 2. Search Documents
```python
tool_name: "search_documents"
parameters:
  - user_id (required): User identifier
  - query (required): Search query
  - top_k (optional): Number of results (default: 5)
```

#### 3. Update Document
```python
tool_name: "update_document"
parameters:
  - user_id (required): User identifier
  - doc_id (required): Document ID to update
  - new_document (required): New document content
  - new_metadata (optional): New metadata
```

#### 4. Delete Document
```python
tool_name: "delete_document"
parameters:
  - user_id (required): User identifier
  - doc_id (required): Document ID to delete
```

### Database Management

#### 5. Save Database
```python
tool_name: "save_database"
parameters: (none)
```

#### 6. Load Database
```python
tool_name: "load_database"
parameters:
  - user_id (required): User database to load
```

#### 7. Get Database Stats
```python
tool_name: "get_database_stats"
parameters:
  - user_id (required): User to get stats for
```

#### 8. List Users
```python
tool_name: "list_users"
parameters: (none)
```

#### 9. Get User Directory Info
```python
tool_name: "get_user_directory_info"
parameters:
  - user_id (required): User to inspect
```

### Import/Export

#### 10. Save Documents Only
```python
tool_name: "save_documents_only"
parameters:
  - user_id (required): User whose documents to save
  - file_path (optional): Custom file path
```

#### 11. Load Documents Only
```python
tool_name: "load_documents_only"
parameters:
  - file_path (required): Path to documents file
```

## 🚀 Quick Start

### 1. Basic Tool Usage

```python
from rag_tool_executor import RAGToolExecutor

# Initialize executor
executor = RAGToolExecutor()

# Add a document
result = executor.execute_tool("add_document", {
    "user_id": "john_doe",
    "document": "I love programming in Python",
    "metadata": {"category": "preferences"}
})

# Search documents
result = executor.execute_tool("search_documents", {
    "user_id": "john_doe",
    "query": "programming languages",
    "top_k": 3
})
```

### 2. OpenAI Function Calling Integration

```python
from llm_interface import call_openai_chat_with_messages
from rag_tools import ALL_RAG_TOOLS

messages = [
    {"role": "user", "content": "Remember that I like pizza"}
]

response = call_openai_chat_with_messages(
    messages=messages,
    tools=ALL_RAG_TOOLS,
    tool_choice="auto"
)
```

### 3. Complete Chatbot Setup

```python
from rag_chat_example import RAGChatBot

# Initialize chatbot for a user
chatbot = RAGChatBot(user_id="alice")

# Chat with RAG capabilities
response = chatbot.chat("Remember that I work at Google")
print(response)  # Assistant will use add_document tool

response = chatbot.chat("Where do I work?")
print(response)  # Assistant will use search_documents tool
```

## 📊 Tool Response Format

All tools return a standardized response format:

```python
{
    "success": bool,        # Whether the operation succeeded
    "error": str|None,      # Error message if failed
    "data": dict|None       # Tool-specific response data
}
```

### Example Responses

#### Add Document Success
```json
{
    "success": true,
    "error": null,
    "data": {
        "doc_id": "doc_0",
        "message": "Document added successfully for user alice",
        "user_id": "alice",
        "document_preview": "I love programming in Python. It's my favorite..."
    }
}
```

#### Search Results
```json
{
    "success": true,
    "error": null,
    "data": {
        "query": "programming languages",
        "user_id": "alice",
        "num_results": 2,
        "results": [
            {
                "doc_id": "doc_0",
                "document": "I love programming in Python",
                "similarity_score": 0.85,
                "metadata": {"category": "preferences"}
            }
        ]
    }
}
```

#### Error Response
```json
{
    "success": false,
    "error": "Document doc_999 not found for user alice",
    "data": {
        "message": "Document doc_999 not found for user alice",
        "doc_id": "doc_999",
        "user_id": "alice",
        "updated": false
    }
}
```

## 🧪 Testing

### Run Individual Tool Tests
```bash
python test_rag_tools.py
```

### Run Interactive Chatbot
```bash
python rag_chat_example.py
```

### Run Demo Mode
```bash
python rag_chat_example.py demo
```

## 🔧 Advanced Configuration

### Custom RAG System Setup

```python
from rag_system import RAGSystem
from rag_tool_executor import RAGToolExecutor

# Initialize with specific configuration
rag_system = RAGSystem(
    model_name="all-MiniLM-L6-v2",  # Embedding model
    index_type="hnsw"               # Index type: flat, ivf, hnsw
)

executor = RAGToolExecutor(rag_system)
```

### Custom System Prompt

```python
from rag_chat_example import RAGChatBot

custom_prompt = """
You are a personal knowledge assistant. You help users store and retrieve information.
Always be concise and helpful.
"""

chatbot = RAGChatBot(
    user_id="custom_user",
    system_prompt=custom_prompt
)
```

### Tool Subset Usage

```python
from rag_tools import CRUD_TOOLS, MANAGEMENT_TOOLS

# Use only CRUD tools
response = call_openai_chat_with_messages(
    messages=messages,
    tools=CRUD_TOOLS,  # Only add, search, update, delete
    tool_choice="auto"
)
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input    │───▶│   LLM Interface  │───▶│  OpenAI API     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Tool Schema   │◀───│  Tool Executor   │───▶│   RAG System    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Tool Response  │◀───│  Result Format   │───▶│   User Storage  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔒 Security Considerations

1. **User Isolation**: Each user has their own database directory
2. **Input Validation**: All tool parameters are validated
3. **Error Handling**: Comprehensive error handling prevents crashes
4. **File Access**: Limited to user-specific directories in `user_memory/`

## 🚨 Common Issues

### Issue: Tool not found
```python
# Problem: Invalid tool name
result = executor.execute_tool("invalid_tool", {})

# Solution: Use valid tool names from rag_tools.py
result = executor.execute_tool("add_document", {...})
```

### Issue: Missing required parameters
```python
# Problem: Missing required 'document' parameter
result = executor.execute_tool("add_document", {"user_id": "test"})

# Solution: Include all required parameters
result = executor.execute_tool("add_document", {
    "user_id": "test",
    "document": "Content here"
})
```

### Issue: Database not found
```python
# Problem: User database doesn't exist
result = executor.execute_tool("search_documents", {
    "user_id": "nonexistent_user",
    "query": "test"
})

# Solution: Add a document first (auto-creates database)
executor.execute_tool("add_document", {
    "user_id": "nonexistent_user",
    "document": "First document"
})
```

## 📈 Performance Tips

1. **Index Selection**:
   - `flat`: Best for <1000 documents
   - `ivf`: Good for 1000-100k documents
   - `hnsw`: Best for >100k documents

2. **Batch Operations**: Add multiple documents before searching for better performance

3. **Memory Management**: Use `save_database()` to persist data and free memory

## 🔄 Integration Examples

### With FastAPI
```python
from fastapi import FastAPI
from rag_tool_executor import RAGToolExecutor

app = FastAPI()
executor = RAGToolExecutor()

@app.post("/add_document")
async def add_document(user_id: str, document: str):
    result = executor.execute_tool("add_document", {
        "user_id": user_id,
        "document": document
    })
    return result
```

### With Streamlit
```python
import streamlit as st
from rag_chat_example import RAGChatBot

st.title("Personal RAG Assistant")
user_id = st.text_input("User ID")
chatbot = RAGChatBot(user_id)

if prompt := st.chat_input("What can I help you remember?"):
    response = chatbot.chat(prompt)
    st.write(response)
```

## 📚 Next Steps

1. **Extend Tools**: Add more specialized tools for your use case
2. **Custom Embeddings**: Integrate domain-specific embedding models
3. **Monitoring**: Add logging and metrics collection
4. **Scaling**: Implement distributed storage for multi-user systems

For more examples and advanced usage, see the test files and example implementations.