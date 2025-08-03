import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional, Tuple


class RAGSystem:
    """
    RAG System using All-mini-LM-v2 for embeddings and Faiss for indexing
    Supports multiple indexing strategies and CRUD operations
    Automatically creates databases for new user_ids
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", index_type: str = "flat"):
        """
        Initialize RAG System
        
        Args:
            model_name: Name of the sentence transformer model
            index_type: Type of Faiss index ('flat', 'ivf', 'hnsw')
        """
        self.model = SentenceTransformer(model_name)
        self.index_type = index_type
        self.dimension = 384  # all-MiniLM-L6-v2 embedding dimension
        
        # Current user context
        self.current_user_id = None
        
        # Storage for documents and metadata
        self.documents = {}  # doc_id -> document text
        self.metadata = {}   # doc_id -> metadata
        self.doc_counter = 0
        
        # Initialize Faiss index based on type
        self.index = self._create_index()
        
        # Database storage path
        self.db_path = None
        
    def _create_index(self) -> faiss.Index:
        """Create Faiss index based on index_type"""
        if self.index_type == "flat":
            # Flat index - exact search, good for small datasets
            return faiss.IndexFlatIP(self.dimension)  # Inner Product for cosine similarity
            
        elif self.index_type == "ivf":
            # IVF (Inverted File) index - faster search for larger datasets
            nlist = 100  # number of clusters
            quantizer = faiss.IndexFlatIP(self.dimension)
            index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist)
            return index
            
        elif self.index_type == "hnsw":
            # HNSW (Hierarchical Navigable Small World) - very fast approximate search
            M = 32  # number of connections per node
            index = faiss.IndexHNSWFlat(self.dimension, M)
            index.hnsw.efConstruction = 40
            return index
            
        else:
            raise ValueError(f"Unsupported index type: {self.index_type}")
    
    def _get_user_directory(self, user_id: str) -> str:
        """
        Get the directory path for a specific user
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Path to the user's directory
        """
        return os.path.join("user_memory", user_id)
    
    def _ensure_user_database(self, user_id: str):
        """
        Ensure database is loaded for the specified user
        If user doesn't exist, create a new database
        
        Args:
            user_id: Unique identifier for the user
        """
        if self.current_user_id == user_id:
            return  # Already loaded
        
        # Try to load existing database
        if self.load_database(user_id):
            self.current_user_id = user_id
            return
        
        # Create new database for new user
        self.documents = {}
        self.metadata = {}
        self.doc_counter = 0
        self.index = self._create_index()
        
        # Create user directory structure
        user_dir = self._get_user_directory(user_id)
        os.makedirs(user_dir, exist_ok=True)
        
        self.db_path = os.path.join(user_dir, f"rag_db_{user_id}.pkl")
        self.current_user_id = user_id
        print(f"Created new database for user: {user_id} in {user_dir}")
    
    def add_document(self, user_id: str, document: str, metadata: Optional[Dict] = None) -> str:
        """
        Add a new document to the RAG system
        Automatically creates database for new user_id
        
        Args:
            user_id: Unique identifier for the user
            document: Text content of the document
            metadata: Optional metadata for the document
            
        Returns:
            Document ID
        """
        # Ensure user database is loaded/created
        self._ensure_user_database(user_id)
        doc_id = f"doc_{self.doc_counter}"
        self.doc_counter += 1
        
        # Store document and metadata
        self.documents[doc_id] = document
        self.metadata[doc_id] = metadata or {}
        
        # Generate embedding
        embedding = self.model.encode([document], normalize_embeddings=True)
        
        # Handle IVF index training if needed
        if self.index_type == "ivf" and not self.index.is_trained:
            if len(self.documents) >= 100:  # Train when we have enough documents
                all_embeddings = np.array([
                    self.model.encode([doc], normalize_embeddings=True)[0] 
                    for doc in self.documents.values()
                ])
                self.index.train(all_embeddings)
                # Add all existing embeddings
                for i, emb in enumerate(all_embeddings):
                    self.index.add(emb.reshape(1, -1))
            else:
                # Store embedding temporarily until we can train
                return doc_id
        else:
            # Add embedding to index
            self.index.add(embedding)
        
        # Save database after operation
        self.save_database()
        
        return doc_id
    
    def update_document(self, user_id: str, doc_id: str, new_document: str, new_metadata: Optional[Dict] = None) -> bool:
        """
        Update an existing document
        
        Args:
            user_id: Unique identifier for the user
            doc_id: ID of the document to update
            new_document: New document content
            new_metadata: New metadata (optional)
            
        Returns:
            True if successful, False if document not found
        """
        # Ensure user database is loaded
        self._ensure_user_database(user_id)
        if doc_id not in self.documents:
            return False
        
        # Get the index position of this document
        doc_ids = list(self.documents.keys())
        doc_position = doc_ids.index(doc_id)
        
        # Remove old embedding by rebuilding index (Faiss doesn't support direct removal)
        self._rebuild_index_without_document(doc_position)
        
        # Update document and metadata
        self.documents[doc_id] = new_document
        if new_metadata is not None:
            self.metadata[doc_id] = new_metadata
        
        # Add new embedding
        embedding = self.model.encode([new_document], normalize_embeddings=True)
        
        if self.index_type == "ivf" and not self.index.is_trained:
            if len(self.documents) >= 100:
                self._retrain_ivf_index()
        else:
            self.index.add(embedding)
        
        # Save database after operation
        self.save_database()
        
        return True
    
    def delete_document(self, user_id: str, doc_id: str) -> bool:
        """
        Delete a document from the RAG system
        
        Args:
            user_id: Unique identifier for the user
            doc_id: ID of the document to delete
            
        Returns:
            True if successful, False if document not found
        """
        # Ensure user database is loaded
        self._ensure_user_database(user_id)
        if doc_id not in self.documents:
            return False
        
        # Get the index position of this document
        doc_ids = list(self.documents.keys())
        doc_position = doc_ids.index(doc_id)
        
        # Remove from storage
        del self.documents[doc_id]
        del self.metadata[doc_id]
        
        # Rebuild index without this document
        self._rebuild_index_without_document(doc_position)
        
        # Save database after operation
        self.save_database()
        
        return True
    
    def search(self, user_id: str, query: str, top_k: int = 5) -> List[Tuple[str, str, float, Dict]]:
        """
        Search for similar documents
        
        Args:
            user_id: Unique identifier for the user
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of tuples (doc_id, document, similarity_score, metadata)
        """
        # Ensure user database is loaded
        self._ensure_user_database(user_id)
        if len(self.documents) == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        
        # Search in index
        if self.index_type == "ivf" and not self.index.is_trained:
            # Fallback to linear search if IVF not trained
            all_embeddings = np.array([
                self.model.encode([doc], normalize_embeddings=True)[0] 
                for doc in self.documents.values()
            ])
            similarities = np.dot(all_embeddings, query_embedding.T).flatten()
            top_indices = np.argsort(similarities)[::-1][:top_k]
            scores = similarities[top_indices]
        else:
            scores, indices = self.index.search(query_embedding, min(top_k, len(self.documents)))
            top_indices = indices[0]
            scores = scores[0]
        
        # Prepare results
        results = []
        doc_ids = list(self.documents.keys())
        
        for i, (idx, score) in enumerate(zip(top_indices, scores)):
            if idx >= 0 and idx < len(doc_ids):  # Valid index
                doc_id = doc_ids[idx]
                document = self.documents[doc_id]
                metadata = self.metadata[doc_id]
                results.append((doc_id, document, float(score), metadata))
        
        return results
    
    def _rebuild_index_without_document(self, exclude_position: int):
        """Rebuild the index excluding a specific document position"""
        # Create new index
        self.index = self._create_index()
        
        # Get all documents except the excluded one
        doc_list = list(self.documents.values())
        if exclude_position < len(doc_list):
            doc_list.pop(exclude_position)
        
        if not doc_list:
            return
        
        # Generate embeddings for remaining documents
        embeddings = self.model.encode(doc_list, normalize_embeddings=True)
        
        # Handle IVF training
        if self.index_type == "ivf" and len(doc_list) >= 100:
            self.index.train(embeddings)
        
        # Add embeddings to index
        if self.index_type != "ivf" or self.index.is_trained:
            self.index.add(embeddings)
    
    def _retrain_ivf_index(self):
        """Retrain IVF index with all current documents"""
        if not self.documents:
            return
        
        # Create new IVF index
        self.index = self._create_index()
        
        # Generate all embeddings
        all_embeddings = np.array([
            self.model.encode([doc], normalize_embeddings=True)[0] 
            for doc in self.documents.values()
        ])
        
        # Train and add
        self.index.train(all_embeddings)
        self.index.add(all_embeddings)
    
    def save_database(self):
        """Save the RAG database to disk"""
        if not self.db_path:
            raise ValueError("Database path not set. No user database loaded.")
        
        # Prepare data for saving
        db_data = {
            'index_type': self.index_type,
            'dimension': self.dimension,
            'documents': self.documents,
            'metadata': self.metadata,
            'doc_counter': self.doc_counter,
            'index_data': faiss.serialize_index(self.index)
        }
        
        # Save to file
        with open(self.db_path, 'wb') as f:
            pickle.dump(db_data, f)
        
        print(f"Database saved to {self.db_path}")
    
    def save_documents_only(self, user_id: str, file_path: Optional[str] = None) -> str:
        """
        Save only document IDs and document text mapping for visualization
        
        Args:
            user_id: Unique identifier for the user
            file_path: Optional custom file path. If None, uses default naming
            
        Returns:
            Path to the saved file
        """
        # Ensure user database is loaded
        self._ensure_user_database(user_id)
        
        # Determine file path
        if file_path is None:
            user_dir = self._get_user_directory(user_id)
            os.makedirs(user_dir, exist_ok=True)
            file_path = os.path.join(user_dir, f"documents_only_{user_id}.pkl")
        
        # Save direct mapping: document_id -> document_text
        with open(file_path, 'wb') as f:
            pickle.dump(self.documents.copy(), f)
        
        print(f"Documents saved to {file_path} ({len(self.documents)} documents)")
        return file_path
    
    def load_documents_only(self, file_path: str) -> Optional[Dict[str, str]]:
        """
        Load documents from a documents-only file
        
        Args:
            file_path: Path to the documents-only file
            
        Returns:
            Dictionary of document_id -> document_text, or None if file doesn't exist/error
        """
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None
        
        try:
            with open(file_path, 'rb') as f:
                documents = pickle.load(f)
            
            # Ensure it's a dictionary (direct mapping format)
            if not isinstance(documents, dict):
                print(f"Invalid file format: expected dictionary mapping")
                return None
            
            print(f"Loaded {len(documents)} documents from {file_path}")
            return documents
            
        except Exception as e:
            print(f"Error loading documents file: {e}")
            return None
    
    def load_database(self, user_id: str) -> bool:
        """
        Load an existing RAG database
        
        Args:
            user_id: User ID of the database to load
            
        Returns:
            True if successful, False if database not found
        """
        user_dir = self._get_user_directory(user_id)
        db_path = os.path.join(user_dir, f"rag_db_{user_id}.pkl")
        
        if not os.path.exists(db_path):
            return False
        
        try:
            with open(db_path, 'rb') as f:
                db_data = pickle.load(f)
            
            # Restore data
            self.index_type = db_data['index_type']
            self.dimension = db_data['dimension']
            self.documents = db_data['documents']
            self.metadata = db_data['metadata']
            self.doc_counter = db_data['doc_counter']
            self.db_path = db_path
            self.current_user_id = user_id
            
            # Restore Faiss index
            self.index = faiss.deserialize_index(db_data['index_data'])
            
            print(f"Database loaded from {db_path}")
            return True
            
        except Exception as e:
            print(f"Error loading database: {e}")
            return False
    
    def get_stats(self, user_id: str) -> Dict:
        """Get database statistics"""
        # Ensure user database is loaded
        self._ensure_user_database(user_id)
        
        return {
            'user_id': user_id,
            'num_documents': len(self.documents),
            'index_type': self.index_type,
            'dimension': self.dimension,
            'is_trained': getattr(self.index, 'is_trained', True)
        }
    
    def list_users(self) -> List[str]:
        """
        List all users that have databases in the user_memory directory
        
        Returns:
            List of user IDs
        """
        user_memory_dir = "user_memory"
        if not os.path.exists(user_memory_dir):
            return []
        
        users = []
        for item in os.listdir(user_memory_dir):
            user_dir = os.path.join(user_memory_dir, item)
            if os.path.isdir(user_dir):
                # Check if this directory contains a database file
                db_file = os.path.join(user_dir, f"rag_db_{item}.pkl")
                if os.path.exists(db_file):
                    users.append(item)
        
        return sorted(users)
    
    def get_user_directory_info(self, user_id: str) -> Optional[Dict]:
        """
        Get information about a user's directory and files
        
        Args:
            user_id: User ID to inspect
            
        Returns:
            Dictionary with directory information or None if user doesn't exist
        """
        user_dir = self._get_user_directory(user_id)
        if not os.path.exists(user_dir):
            return None
        
        info = {
            'user_id': user_id,
            'directory': user_dir,
            'files': []
        }
        
        for file_name in os.listdir(user_dir):
            file_path = os.path.join(user_dir, file_name)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                info['files'].append({
                    'name': file_name,
                    'size_bytes': file_size,
                    'size_mb': round(file_size / (1024 * 1024), 2)
                })
        
        return info