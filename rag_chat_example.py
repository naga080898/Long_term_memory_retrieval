"""
Complete example of RAG-enabled chatbot using OpenAI function calling
Demonstrates how to integrate RAG tools with LLM interface
"""

import json
from typing import List, Dict, Any
from llm_interface import call_openai_chat_with_messages
from rag_tool_executor import RAGToolExecutor, process_tool_call, create_rag_enabled_chat
from rag_tools import ALL_RAG_TOOLS
from prompt_builder import render_template


class RAGChatBot:
    """
    RAG-enabled chatbot that can perform CRUD operations on documents
    """
    
    def __init__(self, user_id: str, index_type: str = "flat", template_path: str = "prompt_templates/intelligent_rag_chat.yaml"):
        """
        Initialize RAG chatbot
        
        Args:
            user_id: User ID for the RAG system
            index_type: Type of Faiss index ('flat', 'ivf', 'hnsw')
            template_path: Path to the YAML template file
        """
        self.user_id = user_id
        self.template_path = template_path
        self.rag_executor, self.tools = create_rag_enabled_chat(user_id, index_type)
        
        # Initialize conversation history (will be dynamically built)
        self.conversation_history = []
    
    def _build_template_context(self, user_message: str) -> Dict[str, Any]:
        """
        Build context for template rendering with automatic document retrieval
        """
        # Get current user stats
        user_stats = None
        stats_result = self.rag_executor.execute_tool("get_database_stats", {"user_id": self.user_id})
        if stats_result and "data" in stats_result and "stats" in stats_result["data"]:
            user_stats = stats_result["data"]["stats"]
        
        # Automatically retrieve relevant documents for the user query
        retrieved_documents = []
        if user_message and user_message.strip():
            search_result = self.rag_executor.execute_tool("search_documents", {
                "user_id": self.user_id,
                "query": user_message,
                "top_k": 5  # Retrieve top 5 most relevant documents
            })
            
            # Extract documents from search result
            if search_result and "data" in search_result and "results" in search_result["data"]:
                retrieved_documents = search_result["data"]["results"]
        
        return {
            "user_id": self.user_id,
            "user_input": user_message,
            "chat_history": self.conversation_history,
            "user_stats": user_stats,
            "retrieved_documents": retrieved_documents,  # Add retrieved documents to context
            "recent_operations": []  # Can be extended later for operation tracking
        }
    
    def chat(self, user_message: str) -> str:
        """
        Process a user message and return the assistant's response using dynamic templates
        
        Args:
            user_message: User's input message
            
        Returns:
            Assistant's response
        """
        # Build template context
        context = self._build_template_context(user_message)
        
        # Render the template to get the full conversation
        try:
            messages = render_template(self.template_path, context)
        except Exception as e:
            print(f"Template rendering error: {e}")
            # Fallback to simple message structure
            messages = [
                {"role": "system", "content": f"You are a helpful assistant for user {self.user_id}."},
                {"role": "user", "content": user_message}
            ]
        
        # Call OpenAI with tools
        response = call_openai_chat_with_messages(
            messages=messages,
            tools=self.tools,
            tool_choice="auto",
            model="gpt-4o-mini",
            temperature=0.7
        )
        
        # Process the response
        message = response.choices[0].message
        
        # Handle tool calls if present
        if hasattr(message, 'tool_calls') and message.tool_calls:
            # Add assistant message with tool calls to history
            self.conversation_history.append({
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": tool_call.type,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments if isinstance(tool_call.function.arguments, str) else json.dumps(tool_call.function.arguments)
                        }
                    }
                    for tool_call in message.tool_calls
                ]
            })
            
            # Execute each tool call
            for tool_call in message.tool_calls:
                # Ensure arguments are JSON string for API compatibility
                tool_call_dict = tool_call.dict()
                if 'function' in tool_call_dict and 'arguments' in tool_call_dict['function']:
                    args = tool_call_dict['function']['arguments']
                    if not isinstance(args, str):
                        tool_call_dict['function']['arguments'] = json.dumps(args)
                
                tool_result = process_tool_call(tool_call_dict, self.rag_executor)
                
                # Add tool result to conversation
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result or ""
                })
            
            # For final response, just use the accumulated conversation history
            # Build a system message and add all conversation history
            context = self._build_template_context("")
            try:
                # Render just the system prompt part
                system_context = {k: v for k, v in context.items()}
                system_context["chat_history"] = []  # No chat history for system prompt
                system_context["user_input"] = ""
                system_messages = render_template(self.template_path, system_context)
                system_prompt = system_messages[0]["content"] if system_messages else f"You are a helpful assistant for user {self.user_id}."
                
                # Build final message list with system + history
                final_messages = [{"role": "system", "content": system_prompt}] + self.conversation_history
            except Exception as e:
                print(f"Final template rendering error: {e}")
                # Fallback: use simple system message + conversation history  
                final_messages = [{"role": "system", "content": f"You are a helpful assistant for user {self.user_id}."}] + self.conversation_history
            
            # Get final response from LLM after tool execution
            final_response = call_openai_chat_with_messages(
                messages=final_messages,
                tools=self.tools,
                tool_choice="auto",
                model="gpt-4o-mini",
                temperature=0.7
            )
            
            final_message = final_response.choices[0].message
            self.conversation_history.append({
                "role": "assistant",
                "content": final_message.content or ""
            })
            
            return final_message.content or ""
        
        else:
            # No tool calls, add user message and assistant response to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": message.content or ""
            })
            
            return message.content or ""
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the full conversation history"""
        return self.conversation_history.copy()
    
    def clear_conversation(self):
        """Clear conversation history (system prompt is dynamically generated)"""
        self.conversation_history = []
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get current user's RAG database statistics"""
        result = self.rag_executor.execute_tool("get_database_stats", {"user_id": self.user_id})
        return result


def run_interactive_chat():
    """
    Run an interactive chat session with the RAG-enabled bot
    """
    print("🤖 RAG-Enabled Chatbot")
    print("=" * 50)
    
    # Get user ID
    user_id = input("Enter your user ID (e.g., 'john_doe'): ").strip()
    if not user_id:
        user_id = "default_user"
    
    # Initialize chatbot
    print(f"\n🔧 Initializing RAG system for user: {user_id}")
    chatbot = RAGChatBot(user_id)
    
    # Show current stats
    stats = chatbot.get_user_stats()
    if stats["success"]:
        num_docs = stats["data"]["stats"]["num_documents"]
        print(f"📊 Current database: {num_docs} documents")
    
    print("\n💡 You can:")
    print("- Add documents: 'Remember that I like pizza'")
    print("- Search: 'What do I like to eat?'")
    print("- Update: 'Update doc_0 with new information'")
    print("- Delete: 'Delete doc_1'")
    print("- Stats: 'How many documents do I have?'")
    print("- Type 'quit' to exit")
    print("\n" + "=" * 50)
    
    # Chat loop
    while True:
        try:
            user_input = input(f"\n[{user_id}] You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print(f"🤖 Assistant: ", end="", flush=True)
            response = chatbot.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


def demo_rag_operations():
    """
    Demonstrate RAG CRUD operations programmatically
    """
    print("🚀 RAG System CRUD Operations Demo")
    print("=" * 50)
    
    # Initialize for demo user
    user_id = "demo_user"
    chatbot = RAGChatBot(user_id)
    
    # Demo operations
    demo_operations = [
        "Remember that I am a software engineer who loves Python programming",
        "Save this information: I work at TechCorp and my favorite IDE is VS Code",
        "Store this note: I have a meeting with the product team every Monday at 10 AM",
        "What do you know about my work?",
        "Tell me about my programming preferences",
        "What meetings do I have?",
        "How many documents do I have stored?"
    ]
    
    for i, operation in enumerate(demo_operations, 1):
        print(f"\n{i}. User: {operation}")
        response = chatbot.chat(operation)
        print(f"   Assistant: {response}")
        print("-" * 50)
    
    # Show final stats
    stats = chatbot.get_user_stats()
    if stats["success"]:
        print(f"\n📊 Final stats: {stats['data']['stats']}")


if __name__ == "__main__":
    # You can run either interactive chat or demo
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_rag_operations()
    else:
        run_interactive_chat()