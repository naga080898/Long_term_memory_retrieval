"""
Simple Q&A Chatbot using OpenAI Chat Completions
A lightweight chatbot that maintains conversation history without RAG functionality
Includes session management with JSONL storage for persistent chat histories
"""

import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from llm_interface import call_openai_chat_with_messages
from prompt_builder import render_template


class SessionManager:
    """
    Manages chat session persistence using JSONL format
    """
    
    def __init__(self, sessions_dir: str = "sessions"):
        """
        Initialize session manager
        
        Args:
            sessions_dir: Directory to store session files
        """
        self.sessions_dir = sessions_dir
        os.makedirs(sessions_dir, exist_ok=True)
    
    def generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return str(uuid.uuid4())
    
    def get_session_file_path(self, session_id: str, user_id: Optional[str] = None) -> str:
        """Get the file path for a session, optionally organized by user"""
        if user_id:
            user_dir = os.path.join(self.sessions_dir, user_id)
            os.makedirs(user_dir, exist_ok=True)
            return os.path.join(user_dir, f"{session_id}.jsonl")
        return os.path.join(self.sessions_dir, f"{session_id}.jsonl")
    
    def save_message(self, session_id: str, role: str, content: str, timestamp: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None, user_id: Optional[str] = None):
        """
        Save a single message (user, assistant, or tool) as a separate line in JSONL format
        
        Args:
            session_id: Unique session identifier
            role: Message role ('user', 'assistant', 'tool', 'system')
            content: Message content
            timestamp: Optional timestamp (current time if not provided)
            metadata: Optional additional metadata
            user_id: Optional user ID for organizing sessions
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        message = {
            "role": role,
            "content": content,
            "timestamp": timestamp,
            "session_id": session_id,
            "message_id": str(uuid.uuid4())
        }
        
        # Add user_id if provided
        if user_id:
            message["user_id"] = user_id
        
        # Add any additional metadata
        if metadata:
            message.update(metadata)
        
        session_file = self.get_session_file_path(session_id, user_id)
        
        # Append to JSONL file - each message on its own line
        with open(session_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(message, ensure_ascii=False) + '\n')
    
    def save_exchange(self, session_id: str, user_query: str, api_response: str, timestamp: Optional[str] = None, user_memory: Optional[str] = None):
        """
        Save an exchange as separate messages (user and assistant) on separate lines
        
        Args:
            session_id: Unique session identifier
            user_query: User's input message
            api_response: Assistant's response
            timestamp: Optional timestamp (current time if not provided)
            user_memory: Optional user memory/context
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        exchange_id = str(uuid.uuid4())
        
        # Save user message
        self.save_message(
            session_id=session_id,
            role="user", 
            content=user_query,
            timestamp=timestamp,
            metadata={"exchange_id": exchange_id}
        )
        
        # Save assistant message
        self.save_message(
            session_id=session_id,
            role="assistant",
            content=api_response,
            timestamp=timestamp,
            metadata={
                "exchange_id": exchange_id,
                "user_memory": user_memory if user_memory else None
            }
        )
    
    def save_tool_response(self, session_id: str, tool_call_id: str, tool_result: str, timestamp: Optional[str] = None):
        """
        Save a tool response as a separate message
        
        Args:
            session_id: Unique session identifier
            tool_call_id: ID of the tool call
            tool_result: Result from the tool execution
            timestamp: Optional timestamp
        """
        self.save_message(
            session_id=session_id,
            role="tool",
            content=tool_result,
            timestamp=timestamp,
            metadata={"tool_call_id": tool_call_id}
        )
    
    def load_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Load complete session history from file (supports all formats: individual messages, old format, and OpenAI format)
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            List of messages in chronological order
        """
        session_file = self.get_session_file_path(session_id)
        
        if not os.path.exists(session_file):
            return []
        
        messages = []
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data = json.loads(line)
                        
                        # Handle different formats
                        if "role" in data and "content" in data:
                            # New individual message format
                            messages.append(data)
                        elif "messages" in data:
                            # Old OpenAI exchange format
                            for msg in data["messages"]:
                                if msg["role"] in ["user", "assistant", "tool"]:
                                    # Add metadata from the exchange to each message
                                    enhanced_msg = msg.copy()
                                    if "metadata" in data:
                                        enhanced_msg.update({
                                            "timestamp": data["metadata"].get("timestamp", ""),
                                            "session_id": data["metadata"].get("session_id", session_id),
                                            "exchange_id": data["metadata"].get("exchange_id", "")
                                        })
                                    messages.append(enhanced_msg)
                        elif "user_query" in data and "api_response" in data:
                            # Very old format - convert to individual messages
                            user_msg = {
                                "role": "user",
                                "content": data["user_query"],
                                "timestamp": data.get("timestamp", ""),
                                "session_id": data.get("session_id", session_id),
                                "message_id": str(uuid.uuid4())
                            }
                            assistant_msg = {
                                "role": "assistant", 
                                "content": data["api_response"],
                                "timestamp": data.get("timestamp", ""),
                                "session_id": data.get("session_id", session_id),
                                "message_id": str(uuid.uuid4())
                            }
                            messages.extend([user_msg, assistant_msg])
                            
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load session {session_id}: {e}")
            return []
        
        # Sort by timestamp to ensure chronological order
        messages.sort(key=lambda x: x.get("timestamp", ""))
        return messages
    
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists"""
        return os.path.exists(self.get_session_file_path(session_id))
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """
        List all available sessions with metadata
        
        Returns:
            List of session info dictionaries
        """
        sessions = []
        
        if not os.path.exists(self.sessions_dir):
            return sessions
        
        for filename in os.listdir(self.sessions_dir):
            if filename.endswith('.jsonl'):
                session_id = filename[:-6]  # Remove .jsonl extension
                session_file = os.path.join(self.sessions_dir, filename)
                
                try:
                    # Get file metadata
                    stat = os.stat(session_file)
                    created_time = datetime.fromtimestamp(stat.st_ctime).isoformat()
                    modified_time = datetime.fromtimestamp(stat.st_mtime).isoformat()
                    
                    # Count messages and exchanges (handle all formats)
                    message_count = 0
                    user_message_count = 0
                    with open(session_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                try:
                                    data = json.loads(line.strip())
                                    if "role" in data and "content" in data:
                                        # New individual message format
                                        message_count += 1
                                        if data["role"] == "user":
                                            user_message_count += 1
                                    elif "messages" in data:
                                        # Old OpenAI exchange format
                                        messages = data["messages"]
                                        for msg in messages:
                                            if msg["role"] in ["user", "assistant", "tool"]:
                                                message_count += 1
                                                if msg["role"] == "user":
                                                    user_message_count += 1
                                    elif "user_query" in data and "api_response" in data:
                                        # Very old format - 2 messages per exchange
                                        message_count += 2
                                        user_message_count += 1
                                except json.JSONDecodeError:
                                    continue
                    
                    exchange_count = user_message_count  # Number of user messages = number of exchanges
                    
                    sessions.append({
                        "session_id": session_id,
                        "created_time": created_time,
                        "modified_time": modified_time,
                        "exchange_count": exchange_count,
                        "file_size": stat.st_size
                    })
                
                except (OSError, IOError) as e:
                    print(f"Warning: Could not read session file {filename}: {e}")
        
        # Sort by modification time (most recent first)
        sessions.sort(key=lambda x: x['modified_time'], reverse=True)
        return sessions
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session file
        
        Args:
            session_id: Session to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        session_file = self.get_session_file_path(session_id)
        
        if os.path.exists(session_file):
            try:
                os.remove(session_file)
                return True
            except OSError as e:
                print(f"Error deleting session {session_id}: {e}")
                return False
        return False
    
    def export_for_openai_training(self, session_id: str, output_file: Optional[str] = None) -> str:
        """
        Export session in pure OpenAI training format (JSONL) - reconstructs conversations from individual messages
        
        Args:
            session_id: Session to export
            output_file: Optional output file path, defaults to sessions/{session_id}_training.jsonl
            
        Returns:
            Path to the exported file
        """
        if output_file is None:
            output_file = os.path.join(self.sessions_dir, f"{session_id}_training.jsonl")
        
        messages = self.load_session_history(session_id)
        
        # Group messages by exchange_id to reconstruct conversations
        exchanges = {}
        for message in messages:
            exchange_id = message.get("exchange_id", "default")
            if exchange_id not in exchanges:
                exchanges[exchange_id] = []
            exchanges[exchange_id].append(message)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for exchange_id, exchange_messages in exchanges.items():
                # Build OpenAI conversation format
                conversation = []
                
                # Add system message if we have user memory
                user_memory = None
                for msg in exchange_messages:
                    if msg["role"] == "assistant" and msg.get("user_memory"):
                        user_memory = msg["user_memory"]
                        break
                
                if user_memory:
                    conversation.append({
                        "role": "system",
                        "content": f"You are a knowledgeable and concise assistant. User Memory: {user_memory}"
                    })
                else:
                    conversation.append({
                        "role": "system",
                        "content": "You are a knowledgeable and concise assistant."
                    })
                
                # Add user, assistant, and tool messages in chronological order
                sorted_messages = sorted(exchange_messages, key=lambda x: x.get("timestamp", ""))
                for msg in sorted_messages:
                    if msg["role"] in ["user", "assistant", "tool"]:
                        openai_msg = {"role": msg["role"], "content": msg["content"]}
                        if msg["role"] == "tool" and "tool_call_id" in msg:
                            openai_msg["tool_call_id"] = msg["tool_call_id"]
                        conversation.append(openai_msg)
                
                # Write as pure OpenAI training format
                if len(conversation) > 1:  # Only export if there are actual messages beyond system
                    training_format = {"messages": conversation}
                    f.write(json.dumps(training_format, ensure_ascii=False) + '\n')
        
        return output_file
    
    def export_all_sessions_for_training(self, output_file: str = "sessions/all_sessions_training.jsonl") -> str:
        """
        Export all sessions combined into a single OpenAI training file
        
        Args:
            output_file: Path for the combined training file
            
        Returns:
            Path to the exported file
        """
        all_sessions = self.list_sessions()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for session_info in all_sessions:
                session_id = session_info['session_id']
                
                # Use the individual session export method and read the results
                temp_file = f"temp_{session_id}_training.jsonl"
                try:
                    self.export_for_openai_training(session_id, temp_file)
                    
                    # Read the exported session and append to combined file
                    with open(temp_file, 'r', encoding='utf-8') as temp_f:
                        for line in temp_f:
                            f.write(line)
                    
                    # Clean up temp file
                    os.remove(temp_file)
                except Exception as e:
                    print(f"Warning: Could not export session {session_id}: {e}")
                    # Clean up temp file if it exists
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
        
        return output_file


class SimpleQAChatBot:
    """
    Simple Q&A chatbot that maintains conversation history with session persistence
    and configurable history management. User memory is managed by RAG chatbot in background.
    """
    
    def __init__(self, user_id: str, session_id: Optional[str] = None, template_path: str = "prompt_templates/simple_qa.yaml", 
                 max_history_length: int = 3, enable_background_memory: bool = True):
        """
        Initialize Simple QA chatbot
        
        Args:
            user_id: User ID for session management and background memory
            session_id: Optional session ID to load existing session, or None for new session
            template_path: Path to the YAML template file
            max_history_length: Maximum number of message pairs to keep in memory (N) - default is 3
            enable_background_memory: Whether to enable background memory creation via RAG chatbot
        """
        self.user_id = user_id
        self.template_path = template_path
        self.session_manager = SessionManager()
        self.session_id = session_id or self.session_manager.generate_session_id()
        self.conversation_history = []
        
        # Configuration for history management
        self.max_history_length = max_history_length  # N
        self.max_working_length = max_history_length * 2  # 2N - when to trigger clipping
        self.enable_background_memory = enable_background_memory
        
        # Memory mapping: user_message -> retrieved_docs
        self.message_memory_mapping = []  # List of (user_message, retrieved_docs) tuples
        
        # Initialize background RAG chatbot for memory management
        self.background_rag_chatbot = None
        if self.enable_background_memory:
            try:
                from rag_chat_example import RAGChatBot
                self.background_rag_chatbot = RAGChatBot(user_id=self.user_id)
            except ImportError:
                self.enable_background_memory = False
        
        # Load existing session if session_id was provided
        if session_id and self.session_manager.session_exists(session_id):
            self.load_session(session_id)
    
    def _process_old_messages_to_background_memory(self, old_message_mappings: List[tuple]):
        """
        Process old user messages through background RAG chatbot
        when conversation history is clipped
        
        Args:
            old_message_mappings: List of (user_message, retrieved_docs) tuples to process
        """
        if not self.enable_background_memory or not self.background_rag_chatbot:
            return
        
        try:
            # Send each old user message to the RAG chatbot
            # Let it handle retrieval, processing, and storage internally
            for user_message, retrieved_docs in old_message_mappings:
                # Just send the user message - RAG chatbot handles everything internally
                self.background_rag_chatbot.chat(user_message)
                
        except Exception as e:
            pass  # Silently handle background memory processing errors
    
    def _manage_conversation_history(self):
        """
        Manage conversation history length, clipping to N when reaching 2N
        Send old message mappings to background RAG chatbot for processing
        """
        # Count message pairs (user + assistant)
        message_pairs = len(self.conversation_history) // 2
        
        if message_pairs >= self.max_working_length:
            # Calculate how many messages to remove (keep as pairs)
            messages_to_keep = self.max_history_length * 2  # N pairs = 2N messages
            pairs_to_remove = message_pairs - self.max_history_length
            
            # Extract old message mappings for background processing
            old_message_mappings = self.message_memory_mapping[:pairs_to_remove]
            
            # Process old mappings through background RAG chatbot
            if old_message_mappings:
                self._process_old_messages_to_background_memory(old_message_mappings)
            
            # Keep only the newest N pairs in both conversation history and memory mapping
            self.conversation_history = self.conversation_history[-messages_to_keep:]
            self.message_memory_mapping = self.message_memory_mapping[-self.max_history_length:]
    
    def get_retrieved_documents(self, user_message: str) -> List[Dict[str, Any]]:
        """
        Get relevant documents for the user message from the background RAG system
        
        Args:
            user_message: User's input message
            
        Returns:
            List of retrieved documents with similarity scores
        """
        if not self.enable_background_memory or not self.background_rag_chatbot:
            return []
        
        try:
            # Use the RAG executor to search for relevant documents
            search_result = self.background_rag_chatbot.rag_executor.execute_tool("search_documents", {
                "user_id": self.user_id,
                "query": user_message,
                "top_k": 5
            })
            
            if search_result and "data" in search_result and "results" in search_result["data"]:
                return search_result["data"]["results"]
            return []
        except Exception as e:
            return []
    
    def load_session(self, session_id: str):
        """
        Load a previous session and rebuild conversation history from individual messages
        
        Args:
            session_id: Session ID to load
        """
        messages = self.session_manager.load_session_history(session_id)
        
        # Rebuild conversation history from individual messages
        self.conversation_history = []
        for message in messages:
            if message["role"] in ["user", "assistant", "tool"]:
                # Convert to conversation history format (role + content)
                history_msg = {
                    "role": message["role"],
                    "content": message["content"]
                }
                
                # Add tool_call_id if it's a tool message
                if message["role"] == "tool" and "tool_call_id" in message:
                    history_msg["tool_call_id"] = message["tool_call_id"]
                
                self.conversation_history.append(history_msg)
                
                # Note: User memory is now managed by background RAG chatbot
        
        self.session_id = session_id
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get current session information"""
        return {
            "session_id": self.session_id,
            "exchange_count": len(self.conversation_history) // 2,
            "max_history_length": self.max_history_length,
            "max_working_length": self.max_working_length,
            "user_id": self.user_id,
            "background_memory_enabled": self.enable_background_memory
        }
    
    def list_available_sessions(self) -> List[Dict[str, Any]]:
        """List all available sessions"""
        return self.session_manager.list_sessions()
    
    def delete_current_session(self) -> bool:
        """Delete the current session"""
        return self.session_manager.delete_session(self.session_id)
    
    def export_session_for_training(self, output_file: Optional[str] = None) -> str:
        """Export current session in OpenAI training format"""
        return self.session_manager.export_for_openai_training(self.session_id, output_file)
    
    def export_all_sessions_for_training(self, output_file: str = "sessions/all_sessions_training.jsonl") -> str:
        """Export all sessions in OpenAI training format"""
        return self.session_manager.export_all_sessions_for_training(output_file)
    
    def _build_template_context(self, user_message: str) -> Dict[str, Any]:
        """
        Build context for template rendering
        """
        return {
            "user_input": user_message,
            "chat_history": self.conversation_history
        }
    
    def chat(self, user_message: str) -> str:
        """
        Process a user message and return the assistant's response using RAG chatbot directly
        
        Args:
            user_message: User's input message
            
        Returns:
            Assistant's response
        """
        # Use RAG chatbot directly if available, otherwise fallback to simple approach
        if self.enable_background_memory and self.background_rag_chatbot:
            try:
                # Use RAG chatbot directly - it will handle all document retrieval and context building
                assistant_response = self.background_rag_chatbot.chat(user_message)
                
                # Get retrieved documents for this message (for mapping storage)
                retrieved_docs = self.get_retrieved_documents(user_message)
                
                # Store message and retrieved docs mapping
                self.message_memory_mapping.append((user_message, retrieved_docs))
                
                # Save exchange to session file
                self.session_manager.save_exchange(
                    session_id=self.session_id,
                    user_query=user_message,
                    api_response=assistant_response,
                    user_memory=None  # Memory is handled by RAG chatbot
                )
                
                # Add to conversation history
                self.conversation_history.append({
                    "role": "user",
                    "content": user_message
                })
                self.conversation_history.append({
                    "role": "assistant", 
                    "content": assistant_response
                })
                
                # Manage conversation history with configurable length and background processing
                self._manage_conversation_history()
                
                return assistant_response
                
            except Exception as e:
                print(f"RAG chatbot error, falling back to simple mode: {e}")
                # Fall through to simple mode
        
        # Fallback to simple template-based approach
        context = self._build_template_context(user_message)
        
        # Render the template to get the full conversation
        try:
            messages = render_template(self.template_path, context)
        except Exception as e:
            print(f"Template rendering error: {e}")
            # Fallback to simple message structure
            messages = [
                {"role": "system", "content": "You are a helpful and knowledgeable assistant."},
                {"role": "user", "content": user_message}
            ]
            # Add conversation history to fallback
            if self.conversation_history:
                messages = [messages[0]] + self.conversation_history + [messages[1]]
        
        # Call OpenAI
        response = call_openai_chat_with_messages(
            messages=messages,
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=1024
        )
        
        # Extract the response
        assistant_response = response.choices[0].message.content
        
        # Get retrieved documents for this message
        retrieved_docs = self.get_retrieved_documents(user_message)
        
        # Store message and retrieved docs mapping
        self.message_memory_mapping.append((user_message, retrieved_docs))
        
        # Save exchange to session file
        self.session_manager.save_exchange(
            session_id=self.session_id,
            user_query=user_message,
            api_response=assistant_response,
            user_memory=None  # No direct user memory
        )
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        self.conversation_history.append({
            "role": "assistant", 
            "content": assistant_response
        })
        
        # Manage conversation history with configurable length and background processing
        self._manage_conversation_history()
        
        return assistant_response
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the full conversation history"""
        return self.conversation_history.copy()
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def clear_background_memory(self):
        """Clear background memory by deleting all documents in RAG system"""
        if self.enable_background_memory and self.background_rag_chatbot:
            try:
                # Get all documents and delete them
                stats_result = self.background_rag_chatbot.rag_executor.execute_tool("get_database_stats", {"user_id": self.user_id})
                if stats_result and "data" in stats_result and "document_ids" in stats_result["data"]:
                    for doc_id in stats_result["data"]["document_ids"]:
                        self.background_rag_chatbot.rag_executor.execute_tool("delete_document", {
                            "user_id": self.user_id,
                            "doc_id": doc_id
                        })
            except Exception as e:
                pass  # Silently handle errors
    
    def set_history_length(self, max_history_length: int):
        """
        Update the maximum conversation history length
        
        Args:
            max_history_length: New maximum number of message pairs to keep (N)
        """
        self.max_history_length = max_history_length
        self.max_working_length = max_history_length * 2
        
        # Immediately apply new limits if current history exceeds them
        self._manage_conversation_history()
    
    def set_background_memory(self, enable: bool = True):
        """
        Enable or disable background memory processing
        
        Args:
            enable: Whether to enable background memory processing
        """
        if enable and not self.background_rag_chatbot:
            try:
                from rag_chat_example import RAGChatBot
                self.background_rag_chatbot = RAGChatBot(user_id=self.user_id)
                self.enable_background_memory = True
            except ImportError:
                pass  # Silently fail if RAG chatbot not available
        else:
            self.enable_background_memory = enable
    
    def get_background_memory_stats(self) -> Optional[Dict[str, Any]]:
        """
        Get background memory statistics for the current user
        
        Returns:
            Dictionary with background memory statistics or None if disabled
        """
        if not self.enable_background_memory or not self.background_rag_chatbot:
            return None
        
        try:
            stats_result = self.background_rag_chatbot.rag_executor.execute_tool("get_database_stats", {"user_id": self.user_id})
            if stats_result and "data" in stats_result:
                return {
                    "user_id": self.user_id,
                    "stats": stats_result["data"]
                }
            return None
        except Exception as e:
            return None


def run_interactive_chat():
    """
    Run an interactive chat session with the simple Q&A bot
    """
    print("🤖 Simple Q&A Chatbot")
    print("=" * 50)
    
    # Get user ID
    user_id = input("\nEnter your user ID: ").strip()
    if not user_id:
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        print(f"Using generated user ID: {user_id}")
    
    # Get session ID (optional)
    session_input = input("Enter session ID (or press Enter for new session): ").strip()
    session_id = session_input if session_input else None
    
    # Initialize chatbot
    chatbot = SimpleQAChatBot(user_id=user_id, session_id=session_id)
    
    print(f"\n✅ Chatbot initialized!")
    print(f"   User ID: {chatbot.user_id}")
    print(f"   Session ID: {chatbot.session_id[:8]}...")
    print(f"\nHello! I'm here to help. What would you like to know?")
    print("(Type 'help' for commands or 'quit' to exit)\n")
    
    # Chat loop
    while True:
        try:
            user_input = input(f"\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() == 'help':
                print("\n💡 Available Commands:")
                print("- Chat normally for Q&A (background memory is automatically managed)")
                print("- 'remember <info>' - Explicitly add information to background memory")
                print("- 'forget' - Clear background memory")
                print("- 'history' - Show conversation history (default: keeps 3 pairs)")
                print("- 'clear' - Clear conversation history")
                print("- 'quit' - Exit")
                print("\nAdvanced commands: 'sessions', 'load', 'session', 'export', 'set-history', 'memory-stats', 'toggle-memory'")
                continue
            
            elif user_input.lower().startswith('remember '):
                info = user_input[9:]  # Remove 'remember '
                # Process as a regular message to store in background memory
                if chatbot.enable_background_memory:
                    # Just send it as a chat message, which will be processed normally
                    print(f"✅ Remembered: {info}")
                    # Process it through the normal chat flow which will handle background memory
                    chatbot.chat(f"Please remember this information: {info}")
                else:
                    print("❌ Background memory is disabled")
                continue
            
            elif user_input.lower() == 'forget':
                chatbot.clear_background_memory()
                print("🧹 Background memory cleared!")
                continue
            
            elif user_input.lower() == 'history':
                history = chatbot.get_conversation_history()
                if history:
                    print("\n📜 Conversation History:")
                    for msg in history:
                        role = msg['role'].title()
                        content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
                        print(f"  {role}: {content}")
                else:
                    print("📜 No conversation history yet.")
                continue
            
            elif user_input.lower() == 'clear':
                chatbot.clear_conversation()
                print("🧹 Conversation history cleared!")
                continue
            
            elif user_input.lower() == 'sessions':
                sessions = chatbot.list_available_sessions()
                if sessions:
                    print("\n📁 Available Sessions:")
                    for session in sessions[:10]:  # Show last 10 sessions
                        short_id = session['session_id'][:8]
                        modified = session['modified_time'][:19].replace('T', ' ')
                        count = session['exchange_count']
                        print(f"  {short_id}... | {modified} | {count} exchanges")
                    if len(sessions) > 10:
                        print(f"  ... and {len(sessions) - 10} more sessions")
                else:
                    print("📁 No previous sessions found.")
                continue
            
            elif user_input.lower().startswith('load '):
                session_id = user_input[5:].strip()  # Remove 'load '
                if len(session_id) < 8:
                    # If partial ID provided, try to find matching session
                    sessions = chatbot.list_available_sessions()
                    matches = [s for s in sessions if s['session_id'].startswith(session_id)]
                    if len(matches) == 1:
                        session_id = matches[0]['session_id']
                    elif len(matches) > 1:
                        print(f"🔍 Multiple sessions match '{session_id}'. Please be more specific.")
                        for match in matches[:5]:
                            short_id = match['session_id'][:8]
                            print(f"  {short_id}...")
                        continue
                    else:
                        print(f"❌ No session found matching '{session_id}'")
                        continue
                
                if chatbot.session_manager.session_exists(session_id):
                    chatbot.load_session(session_id)
                    print(f"✅ Loaded session: {session_id[:8]}...")
                    info = chatbot.get_session_info()
                    print(f"📊 Exchanges loaded: {info['exchange_count']}")
                else:
                    print(f"❌ Session not found: {session_id}")
                continue
            
            elif user_input.lower() == 'session':
                info = chatbot.get_session_info()
                print(f"\n📊 Current Session Info:")
                print(f"  Session ID: {info['session_id']}")
                print(f"  Exchanges: {info['exchange_count']}")
                print(f"  Background memory: {'enabled' if info['background_memory_enabled'] else 'disabled'}")
                print(f"  Max history length: {info['max_history_length']} pairs")
                print(f"  Working length: {info['max_working_length']} pairs")
                print(f"  User ID: {info['user_id']}")
                print(f"  Background memory: {'enabled' if info['background_memory_enabled'] else 'disabled'}")
                continue
            
            elif user_input.lower() == 'delete-session':
                confirm = input(f"⚠️  Delete session {chatbot.session_id[:8]}...? (yes/no): ").strip().lower()
                if confirm in ['yes', 'y']:
                    if chatbot.delete_current_session():
                        print("🗑️ Session deleted!")
                        # Start new session
                        chatbot = SimpleQAChatBot(user_id=chatbot.user_id)
                        print(f"🆕 Started new session: {chatbot.session_id[:8]}...")
                    else:
                        print("❌ Failed to delete session.")
                else:
                    print("❌ Session deletion cancelled.")
                continue
            
            elif user_input.lower() == 'export':
                try:
                    output_file = chatbot.export_session_for_training()
                    print(f"✅ Session exported to: {output_file}")
                except Exception as e:
                    print(f"❌ Export failed: {e}")
                continue
            
            elif user_input.lower() == 'export-all':
                try:
                    output_file = chatbot.export_all_sessions_for_training()
                    print(f"✅ All sessions exported to: {output_file}")
                except Exception as e:
                    print(f"❌ Export failed: {e}")
                continue
            
            elif user_input.lower().startswith('set-history '):
                try:
                    n = int(user_input[12:].strip())  # Remove 'set-history '
                    if n <= 0:
                        print("❌ History length must be positive")
                    else:
                        chatbot.set_history_length(n)
                        print(f"✅ History length updated to {n} pairs")
                except ValueError:
                    print("❌ Please provide a valid number: 'set-history <N>'")
                continue
            
            elif user_input.lower() == 'memory-stats':
                memory_stats = chatbot.get_background_memory_stats()
                if memory_stats:
                    print(f"\n📚 Background Memory Statistics:")
                    print(f"  User ID: {memory_stats['user_id']}")
                    stats = memory_stats.get('stats', {})
                    print(f"  Documents: {stats.get('document_count', 0)}")
                    print(f"  Database path: {stats.get('database_path', 'N/A')}")
                else:
                    print("📚 Background memory is disabled or unavailable")
                continue
            
            elif user_input.lower() == 'toggle-memory':
                current_status = chatbot.enable_background_memory
                chatbot.set_background_memory(not current_status)
                new_status = "enabled" if not current_status else "disabled"
                print(f"📚 Background memory {new_status}")
                continue
            
            # Regular chat
            print(f"🤖 Assistant: ", end="", flush=True)
            response = chatbot.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


def demo_simple_chat():
    """
    Demonstrate simple chatbot capabilities
    """
    print("🚀 Simple Q&A Chatbot Demo")
    print("=" * 50)
    
    # Use demo user
    chatbot = SimpleQAChatBot(user_id="demo_user")
    
    # Send initial information to background memory via chat
    if chatbot.enable_background_memory:
        print("Setting up initial user context...")
        chatbot.chat("Please remember that I am learning about AI and programming. I am particularly interested in Python and machine learning.")
    
    print(f"User ID: {chatbot.user_id}")
    print(f"Session ID: {chatbot.session_id}")
    
    # Demo conversation
    demo_questions = [
        "Hello! How are you?",
        "What can you help me with?",
        "Can you explain what machine learning is?",
        "What programming language should I start with?",
        "Thank you for the help!"
    ]
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n{i}. User: {question}")
        response = chatbot.chat(question)
        print(f"   Assistant: {response}")
        print("-" * 50)
    
    # Show session info
    session_info = chatbot.get_session_info()
    print(f"\n📊 Session Stats:")
    print(f"   Session ID: {session_info['session_id']}")
    print(f"   Total exchanges: {session_info['exchange_count']}")
    print(f"   Session saved to: sessions/{chatbot.session_id}.jsonl")



def demo_configurable_history():
    """
    Demonstrate configurable history length with background memory processing
    """
    print("🚀 Configurable History & Background Memory Processing Demo")
    print("=" * 60)
    
    # Create chatbot with default history length for demo
    print("\n1. Creating chatbot with default max_history_length=3 pairs...")
    chatbot = SimpleQAChatBot(
        user_id="demo_user",
        enable_background_memory=True
    )
    
    info = chatbot.get_session_info()
    print(f"   Session ID: {info['session_id'][:8]}...")
    print(f"   Max history: {info['max_history_length']} pairs")
    print(f"   Working length: {info['max_working_length']} pairs")
    print(f"   Background memory: {'enabled' if info['background_memory_enabled'] else 'disabled'}")
    
    # Have many conversations to trigger clipping (default N=3, so 2N=6)
    questions = [
        "Hello! What's the weather like today?",           # Exchange 1
        "Tell me about machine learning",                  # Exchange 2
        "What are neural networks?",                       # Exchange 3
        "How do I learn Python programming?",              # Exchange 4
        "What's the difference between AI and ML?",        # Exchange 5
        "Can you explain deep learning?",                  # Exchange 6
        "What are the best programming practices?",        # Exchange 7 (should trigger clipping)
        "How do databases work?",                          # Exchange 8
    ]
    
    print(f"\n2. Having {len(questions)} conversations to demonstrate clipping...")
    
    for i, question in enumerate(questions, 1):
        print(f"\n   Exchange {i}: {question[:50]}...")
        response = chatbot.chat(question)
        print(f"   Response: {response[:80]}...")
        
        # Show history status
        current_pairs = len(chatbot.conversation_history) // 2
        print(f"   📊 Current history: {current_pairs} pairs")
        
        # Show when clipping happens
        if i >= 6:  # At 2N=6 pairs (default), clipping should happen
            print(f"   📏 Clipping triggered at exchange {i}")
    
    # Show final session info
    print(f"\n3. Final session status:")
    info = chatbot.get_session_info()
    print(f"   Total exchanges processed: {len(questions)}")
    print(f"   Current history pairs: {info['exchange_count']}")
    print(f"   Should be ≤ {info['max_history_length']} due to clipping")
    
    # Show background memory stats
    memory_stats = chatbot.get_background_memory_stats()
    if memory_stats:
        print(f"\n4. Background Memory Status:")
        print(f"   User ID: {memory_stats['user_id']}")
        stats = memory_stats.get('stats', {})
        print(f"   Stored documents: {stats.get('document_count', 0)}")
        print(f"   Database path: {stats.get('database_path', 'N/A')}")
    
    # Test configuration changes
    print(f"\n5. Testing runtime configuration changes...")
    print(f"   Changing max history length from {chatbot.max_history_length} to 2...")
    chatbot.set_history_length(2)
    
    # Show updated info
    info = chatbot.get_session_info()
    print(f"   New history pairs: {info['exchange_count']}")
    print(f"   New max: {info['max_history_length']} pairs")
    
    # Test disabling background memory
    print(f"\n6. Testing background memory toggle...")
    chatbot.set_background_memory(False)
    
    # Add one more conversation
    final_question = "What did we discuss earlier?"
    print(f"\n   Final test: {final_question}")
    final_response = chatbot.chat(final_question)
    print(f"   Response: {final_response[:100]}...")
    
    print(f"\n✅ Configurable history demo complete!")
    print(f"   - Demonstrated history clipping at 2N → N")
    print(f"   - Showed background memory processing")
    print(f"   - Tested runtime configuration changes")
    print(f"   - Session file: sessions/{chatbot.session_id}.jsonl")


if __name__ == "__main__":
    # You can run interactive chat or demos
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            demo_simple_chat()
        elif sys.argv[1] == "history-demo":
            demo_configurable_history()
        else:
            print("Usage:")
            print("  python simple_qa_chatbot.py              # Interactive chat")
            print("  python simple_qa_chatbot.py demo         # Basic demo")
            print("  python simple_qa_chatbot.py history-demo # Configurable history & background memory demo")
    else:
        run_interactive_chat()