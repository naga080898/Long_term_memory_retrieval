# OpenAI API Setup Guide

## 🔑 Setting Up Your OpenAI API Key

To use the full chatbot functionality, you need to set up your OpenAI API key:

### 1. Get Your API Key
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (it starts with `sk-`)

### 2. Create .env File
Create a file called `.env` in your project root:

```bash
# In your terminal, run:
touch .env
```

### 3. Add Your API Key
Open `.env` file and add:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**⚠️ Important:** 
- Replace `sk-your-actual-api-key-here` with your real API key
- Never commit `.env` files to git (they're already in .gitignore)
- Keep your API key secure

### 4. Test the Chatbot
Once your API key is set up:

```bash
# Activate your environment
source LLM_memory-env/bin/activate

# Run the interactive chatbot
python rag_chat_example.py

# Or try the demo mode
python rag_chat_example.py demo
```

## 💬 Example Chat Session

```
🤖 RAG-Enabled Chatbot
Enter your user ID: alice

[alice] You: Remember that I love hiking and photography
🤖 Assistant: I've saved that information! You love hiking and photography.

[alice] You: What do I enjoy doing?
🤖 Assistant: Based on what you've told me, you enjoy hiking and photography!

[alice] You: Add this note: I work as a data scientist at Google
🤖 Assistant: I've added that information about your work as a data scientist at Google.

[alice] You: What's my job?
🤖 Assistant: You work as a data scientist at Google.
```

## 🛠️ Available Commands

When chatting, you can:
- **"Remember this..."** → Adds information
- **"Save this note..."** → Stores a document  
- **"What do you know about..."** → Searches your documents
- **"Find information about..."** → Semantic search
- **"How many documents do I have?"** → Gets statistics
- **"Update doc_0 with..."** → Updates specific documents
- **"Delete doc_1"** → Removes documents

## 🚀 System Features

✅ **Multi-user Support** - Each user gets their own database
✅ **Semantic Search** - Find information by meaning, not exact words
✅ **CRUD Operations** - Create, Read, Update, Delete documents
✅ **Persistent Storage** - Your data is saved automatically
✅ **Export/Import** - Backup and restore your data
✅ **Real-time Chat** - Natural conversation with your AI assistant

## 📊 Current System Status

Your RAG system is ready with:
- 🔧 **11 tools** available for LLM function calling
- 📚 **7 users** already in the system
- 🏗️ **Three index types** supported (flat, ivf, hnsw)
- 🤖 **GPT-4o-mini** as default model (fast and cost-effective)

## 🎯 Next Steps

1. **Set up API key** (above)
2. **Try the chatbot**: `python rag_chat_example.py`
3. **Explore tools**: Check `RAG_TOOLS_DOCUMENTATION.md`
4. **Customize**: Modify system prompts in `rag_chat_example.py`
5. **Integrate**: Use the tools in your own applications

Happy chatting! 🚀