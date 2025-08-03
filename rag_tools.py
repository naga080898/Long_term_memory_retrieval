"""
Tool schemas for RAG system CRUD operations
Compatible with OpenAI function calling format
"""

# CRUD Operations Tools

ADD_DOCUMENT_TOOL = {
    "type": "function",
    "function": {
        "name": "add_document",
        "description": "Add a new document to the RAG system for a specific user. Automatically creates database for new users.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "Unique identifier for the user (e.g., 'john_doe', 'alice')"
                },
                "document": {
                    "type": "string",
                    "description": "Text content of the document to add"
                },
                "metadata": {
                    "type": "object",
                    "description": "Optional metadata for the document (e.g., {'source': 'email', 'date': '2024-01-01', 'category': 'work'})",
                    "properties": {},
                    "additionalProperties": True
                }
            },
            "required": ["user_id", "document"],
            "additionalProperties": False
        }
    }
}

SEARCH_DOCUMENTS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_documents",
        "description": "Search for similar documents in the RAG system using semantic similarity.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "Unique identifier for the user whose documents to search"
                },
                "query": {
                    "type": "string",
                    "description": "Search query to find similar documents"
                },
                "top_k": {
                    "type": "integer",
                    "description": "Number of top results to return (default: 5)",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 50
                }
            },
            "required": ["user_id", "query"],
            "additionalProperties": False
        }
    }
}

UPDATE_DOCUMENT_TOOL = {
    "type": "function",
    "function": {
        "name": "update_document",
        "description": "Update an existing document in the RAG system.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "Unique identifier for the user"
                },
                "doc_id": {
                    "type": "string",
                    "description": "ID of the document to update (e.g., 'doc_0', 'doc_1')"
                },
                "new_document": {
                    "type": "string",
                    "description": "New text content for the document"
                },
                "new_metadata": {
                    "type": "object",
                    "description": "New metadata for the document (optional)",
                    "properties": {},
                    "additionalProperties": True
                }
            },
            "required": ["user_id", "doc_id", "new_document"],
            "additionalProperties": False
        }
    }
}

DELETE_DOCUMENT_TOOL = {
    "type": "function",
    "function": {
        "name": "delete_document",
        "description": "Delete a document from the RAG system.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "Unique identifier for the user"
                },
                "doc_id": {
                    "type": "string",
                    "description": "ID of the document to delete (e.g., 'doc_0', 'doc_1')"
                }
            },
            "required": ["user_id", "doc_id"],
            "additionalProperties": False
        }
    }
}

# Database Management Tools

SAVE_DATABASE_TOOL = {
    "type": "function",
    "function": {
        "name": "save_database",
        "description": "Save the current RAG database to disk for the loaded user.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    }
}

LOAD_DATABASE_TOOL = {
    "type": "function",
    "function": {
        "name": "load_database",
        "description": "Load an existing RAG database for a specific user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID of the database to load"
                }
            },
            "required": ["user_id"],
            "additionalProperties": False
        }
    }
}

# Information and Statistics Tools

GET_STATS_TOOL = {
    "type": "function",
    "function": {
        "name": "get_database_stats",
        "description": "Get statistics about a user's RAG database (number of documents, index type, etc.).",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID to get statistics for"
                }
            },
            "required": ["user_id"],
            "additionalProperties": False
        }
    }
}

LIST_USERS_TOOL = {
    "type": "function",
    "function": {
        "name": "list_users",
        "description": "List all users that have databases in the RAG system.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    }
}

GET_USER_INFO_TOOL = {
    "type": "function",
    "function": {
        "name": "get_user_directory_info",
        "description": "Get information about a user's directory and files in the RAG system.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID to get directory information for"
                }
            },
            "required": ["user_id"],
            "additionalProperties": False
        }
    }
}

# Document Export/Import Tools

SAVE_DOCUMENTS_ONLY_TOOL = {
    "type": "function",
    "function": {
        "name": "save_documents_only",
        "description": "Save only document IDs and text mapping for visualization/export purposes.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID whose documents to save"
                },
                "file_path": {
                    "type": "string",
                    "description": "Optional custom file path. If not provided, uses default naming convention."
                }
            },
            "required": ["user_id"],
            "additionalProperties": False
        }
    }
}

LOAD_DOCUMENTS_ONLY_TOOL = {
    "type": "function",
    "function": {
        "name": "load_documents_only",
        "description": "Load documents from a documents-only file for inspection/analysis.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the documents-only file to load"
                }
            },
            "required": ["file_path"],
            "additionalProperties": False
        }
    }
}

# Collection of all tools for easy import
ALL_RAG_TOOLS = [
    ADD_DOCUMENT_TOOL,
    SEARCH_DOCUMENTS_TOOL,
    UPDATE_DOCUMENT_TOOL,
    DELETE_DOCUMENT_TOOL,
    SAVE_DATABASE_TOOL,
    LOAD_DATABASE_TOOL,
    GET_STATS_TOOL,
    LIST_USERS_TOOL,
    GET_USER_INFO_TOOL,
    SAVE_DOCUMENTS_ONLY_TOOL,
    LOAD_DOCUMENTS_ONLY_TOOL
]

# Grouped tools for specific use cases
CRUD_TOOLS = [
    ADD_DOCUMENT_TOOL,
    SEARCH_DOCUMENTS_TOOL,
    UPDATE_DOCUMENT_TOOL,
    DELETE_DOCUMENT_TOOL
]

MANAGEMENT_TOOLS = [
    SAVE_DATABASE_TOOL,
    LOAD_DATABASE_TOOL,
    GET_STATS_TOOL,
    LIST_USERS_TOOL,
    GET_USER_INFO_TOOL
]

EXPORT_IMPORT_TOOLS = [
    SAVE_DOCUMENTS_ONLY_TOOL,
    LOAD_DOCUMENTS_ONLY_TOOL
]