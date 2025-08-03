"""
Tool executor for RAG system CRUD operations
Bridges tool schemas with the actual RAG system implementation
"""

import json
from typing import Dict, Any, Optional
from rag_system import RAGSystem


class RAGToolExecutor:
    """
    Executor class that handles tool function calls for the RAG system
    """
    
    def __init__(self, rag_system: Optional[RAGSystem] = None):
        """
        Initialize the tool executor
        
        Args:
            rag_system: Optional pre-initialized RAG system. If None, creates a new one.
        """
        self.rag_system = rag_system if rag_system else RAGSystem()
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool function by name with given arguments
        
        Args:
            tool_name: Name of the tool function to execute
            arguments: Dictionary of arguments for the tool
            
        Returns:
            Dictionary containing the result and status
        """
        try:
            # Map tool names to executor methods
            tool_map = {
                "add_document": self._add_document,
                "search_documents": self._search_documents,
                "update_document": self._update_document,
                "delete_document": self._delete_document,
                "save_database": self._save_database,
                "load_database": self._load_database,
                "get_database_stats": self._get_database_stats,
                "list_users": self._list_users,
                "get_user_directory_info": self._get_user_directory_info,
                "save_documents_only": self._save_documents_only,
                "load_documents_only": self._load_documents_only
            }
            
            if tool_name not in tool_map:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}",
                    "data": None
                }
            
            # Execute the tool function
            result = tool_map[tool_name](**arguments)
            
            return {
                "success": True,
                "error": None,
                "data": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def _add_document(self, user_id: str, document: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Add a new document to the RAG system"""
        doc_id = self.rag_system.add_document(user_id, document, metadata)
        return {
            "doc_id": doc_id,
            "message": f"Document added successfully for user {user_id}",
            "user_id": user_id,
            "document_preview": document[:100] + "..." if len(document) > 100 else document
        }
    
    def _search_documents(self, user_id: str, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Search for similar documents"""
        results = self.rag_system.search(user_id, query, top_k)
        
        formatted_results = []
        for doc_id, document, score, metadata in results:
            formatted_results.append({
                "doc_id": doc_id,
                "document": document,
                "similarity_score": score,
                "metadata": metadata
            })
        
        return {
            "query": query,
            "user_id": user_id,
            "num_results": len(formatted_results),
            "results": formatted_results
        }
    
    def _update_document(self, user_id: str, doc_id: str, new_document: str, new_metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Update an existing document"""
        success = self.rag_system.update_document(user_id, doc_id, new_document, new_metadata)
        
        if success:
            return {
                "message": f"Document {doc_id} updated successfully for user {user_id}",
                "doc_id": doc_id,
                "user_id": user_id,
                "updated": True
            }
        else:
            return {
                "message": f"Document {doc_id} not found for user {user_id}",
                "doc_id": doc_id,
                "user_id": user_id,
                "updated": False
            }
    
    def _delete_document(self, user_id: str, doc_id: str) -> Dict[str, Any]:
        """Delete a document"""
        success = self.rag_system.delete_document(user_id, doc_id)
        
        if success:
            return {
                "message": f"Document {doc_id} deleted successfully for user {user_id}",
                "doc_id": doc_id,
                "user_id": user_id,
                "deleted": True
            }
        else:
            return {
                "message": f"Document {doc_id} not found for user {user_id}",
                "doc_id": doc_id,
                "user_id": user_id,
                "deleted": False
            }
    
    def _save_database(self) -> Dict[str, Any]:
        """Save the current database"""
        try:
            self.rag_system.save_database()
            return {
                "message": "Database saved successfully",
                "saved": True
            }
        except ValueError as e:
            return {
                "message": str(e),
                "saved": False
            }
    
    def _load_database(self, user_id: str) -> Dict[str, Any]:
        """Load a database for a specific user"""
        success = self.rag_system.load_database(user_id)
        
        if success:
            stats = self.rag_system.get_stats(user_id)
            return {
                "message": f"Database loaded successfully for user {user_id}",
                "user_id": user_id,
                "loaded": True,
                "stats": stats
            }
        else:
            return {
                "message": f"Database not found for user {user_id}",
                "user_id": user_id,
                "loaded": False
            }
    
    def _get_database_stats(self, user_id: str) -> Dict[str, Any]:
        """Get database statistics"""
        stats = self.rag_system.get_stats(user_id)
        return {
            "message": f"Statistics retrieved for user {user_id}",
            "stats": stats
        }
    
    def _list_users(self) -> Dict[str, Any]:
        """List all users with databases"""
        users = self.rag_system.list_users()
        return {
            "message": f"Found {len(users)} users with databases",
            "num_users": len(users),
            "users": users
        }
    
    def _get_user_directory_info(self, user_id: str) -> Dict[str, Any]:
        """Get user directory information"""
        info = self.rag_system.get_user_directory_info(user_id)
        
        if info:
            return {
                "message": f"Directory information retrieved for user {user_id}",
                "user_id": user_id,
                "found": True,
                "info": info
            }
        else:
            return {
                "message": f"Directory not found for user {user_id}",
                "user_id": user_id,
                "found": False,
                "info": None
            }
    
    def _save_documents_only(self, user_id: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Save documents-only file"""
        saved_path = self.rag_system.save_documents_only(user_id, file_path)
        return {
            "message": f"Documents saved for user {user_id}",
            "user_id": user_id,
            "file_path": saved_path,
            "saved": True
        }
    
    def _load_documents_only(self, file_path: str) -> Dict[str, Any]:
        """Load documents from documents-only file"""
        documents = self.rag_system.load_documents_only(file_path)
        
        if documents:
            return {
                "message": f"Loaded {len(documents)} documents from {file_path}",
                "file_path": file_path,
                "loaded": True,
                "num_documents": len(documents),
                "document_ids": list(documents.keys()),
                "documents": documents
            }
        else:
            return {
                "message": f"Failed to load documents from {file_path}",
                "file_path": file_path,
                "loaded": False,
                "documents": None
            }


def process_tool_call(tool_call: Dict[str, Any], rag_executor: RAGToolExecutor) -> str:
    """
    Process a tool call from OpenAI function calling format
    
    Args:
        tool_call: Tool call object with function name and arguments
        rag_executor: RAG tool executor instance
        
    Returns:
        JSON string result of the tool execution
    """
    function_name = tool_call.get("function", {}).get("name")
    arguments_str = tool_call.get("function", {}).get("arguments", "{}")
    
    try:
        # Parse arguments from JSON string
        arguments = json.loads(arguments_str) if isinstance(arguments_str, str) else arguments_str
        
        # Execute the tool
        result = rag_executor.execute_tool(function_name, arguments)
        
        # Return result as JSON string
        return json.dumps(result, indent=2)
        
    except json.JSONDecodeError as e:
        error_result = {
            "success": False,
            "error": f"Invalid JSON arguments: {str(e)}",
            "data": None
        }
        return json.dumps(error_result, indent=2)
    
    except Exception as e:
        error_result = {
            "success": False,
            "error": f"Tool execution error: {str(e)}",
            "data": None
        }
        return json.dumps(error_result, indent=2)


# Example usage function
def create_rag_enabled_chat(user_id: str = None, index_type: str = "flat") -> tuple:
    """
    Create a RAG-enabled chat setup with tools
    
    Args:
        user_id: Optional user ID to load initially
        index_type: Type of Faiss index to use
        
    Returns:
        Tuple of (rag_executor, tools_list) ready for OpenAI chat completion
    """
    from rag_tools import ALL_RAG_TOOLS
    
    # Initialize RAG system and executor
    rag_system = RAGSystem(index_type=index_type)
    rag_executor = RAGToolExecutor(rag_system)
    
    # Load user database if specified
    if user_id:
        rag_executor.execute_tool("load_database", {"user_id": user_id})
    
    return rag_executor, ALL_RAG_TOOLS