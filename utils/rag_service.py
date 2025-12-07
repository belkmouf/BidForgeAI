"""
RAG (Retrieval-Augmented Generation) Service for BidForgeAI

This module provides embeddings generation, vector storage, and semantic search
capabilities for context-aware bid generation and conflict detection.
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from .document_processor import DocumentProcessor


class RAGService:
    """Service for RAG operations including embeddings and vector search"""

    def __init__(self,
                 model_name: str = "all-MiniLM-L6-v2",
                 persist_directory: str = "./chroma_db"):
        """
        Initialize RAG service with embeddings model and vector store

        Args:
            model_name: SentenceTransformer model name (default: all-MiniLM-L6-v2)
            persist_directory: Directory for ChromaDB persistence
        """
        # Initialize embeddings model
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

        # Initialize ChromaDB
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Initialize collections
        self._init_collections()

        # Document processor for chunking
        self.doc_processor = DocumentProcessor()

    def _init_collections(self):
        """Initialize ChromaDB collections for different document types"""
        # Collection for RFQ/RFP documents
        try:
            self.rfq_collection = self.client.get_collection("rfq_documents")
        except:
            self.rfq_collection = self.client.create_collection(
                name="rfq_documents",
                metadata={"description": "RFQ and RFP documents"}
            )

        # Collection for historical bids
        try:
            self.bids_collection = self.client.get_collection("historical_bids")
        except:
            self.bids_collection = self.client.create_collection(
                name="historical_bids",
                metadata={"description": "Historical winning bids"}
            )

        # Collection for conflict detection
        try:
            self.conflicts_collection = self.client.get_collection("conflict_documents")
        except:
            self.conflicts_collection = self.client.create_collection(
                name="conflict_documents",
                metadata={"description": "Documents for conflict detection"}
            )

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts

        Args:
            texts: List of text strings to embed

        Returns:
            Array of embeddings
        """
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings

    def index_document(self,
                      file_path: str,
                      document_type: str = "rfq",
                      metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process and index a document into the vector store

        Args:
            file_path: Path to document file
            document_type: Type of document (rfq, bid, conflict)
            metadata: Additional metadata for the document

        Returns:
            Dictionary with indexing statistics
        """
        # Process document
        doc_data = self.doc_processor.process_file(file_path)

        if not doc_data or not doc_data.get('text'):
            return {
                'success': False,
                'error': 'Failed to extract text from document'
            }

        # Chunk the document
        chunks = self.doc_processor.chunk_text(
            doc_data['text'],
            chunk_size=1000,
            overlap=200
        )

        if not chunks:
            return {
                'success': False,
                'error': 'No chunks generated from document'
            }

        # Generate embeddings
        embeddings = self.generate_embeddings(chunks)

        # Select collection based on document type
        if document_type == "rfq":
            collection = self.rfq_collection
        elif document_type == "bid":
            collection = self.bids_collection
        elif document_type == "conflict":
            collection = self.conflicts_collection
        else:
            return {
                'success': False,
                'error': f'Unknown document type: {document_type}'
            }

        # Prepare metadata for each chunk
        base_metadata = metadata or {}
        base_metadata.update({
            'source_file': os.path.basename(file_path),
            'document_type': document_type,
            'indexed_at': datetime.now().isoformat(),
            'file_type': doc_data.get('file_type', 'unknown'),
            'total_chunks': len(chunks)
        })

        # Generate unique IDs for chunks
        doc_id = base_metadata.get('doc_id', os.path.basename(file_path))
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]

        # Prepare metadata for each chunk
        metadatas = []
        for i, chunk in enumerate(chunks):
            chunk_meta = base_metadata.copy()
            chunk_meta['chunk_index'] = i
            chunk_meta['chunk_text_preview'] = chunk[:100]
            metadatas.append(chunk_meta)

        # Add to collection
        collection.add(
            ids=ids,
            embeddings=embeddings.tolist(),
            documents=chunks,
            metadatas=metadatas
        )

        return {
            'success': True,
            'document_type': document_type,
            'chunks_indexed': len(chunks),
            'embedding_dim': self.embedding_dim,
            'doc_id': doc_id,
            'metadata': base_metadata
        }

    def search_similar(self,
                      query: str,
                      document_type: str = "rfq",
                      n_results: int = 5) -> Dict[str, Any]:
        """
        Search for similar documents/chunks using semantic search

        Args:
            query: Search query text
            document_type: Type of documents to search (rfq, bid, conflict)
            n_results: Number of results to return

        Returns:
            Dictionary with search results
        """
        # Select collection
        if document_type == "rfq":
            collection = self.rfq_collection
        elif document_type == "bid":
            collection = self.bids_collection
        elif document_type == "conflict":
            collection = self.conflicts_collection
        else:
            return {
                'success': False,
                'error': f'Unknown document type: {document_type}'
            }

        # Check if collection has documents
        if collection.count() == 0:
            return {
                'success': True,
                'results': [],
                'message': f'No documents indexed in {document_type} collection'
            }

        # Generate query embedding
        query_embedding = self.generate_embeddings([query])[0]

        # Search
        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=min(n_results, collection.count())
        )

        # Format results
        formatted_results = []
        if results['ids'] and len(results['ids']) > 0:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i],
                    'similarity_score': 1 - results['distances'][0][i]  # Convert distance to similarity
                })

        return {
            'success': True,
            'query': query,
            'results': formatted_results,
            'total_found': len(formatted_results)
        }

    def get_context_for_bid(self,
                           rfq_text: str,
                           n_historical_bids: int = 5,
                           n_rfq_chunks: int = 10) -> Dict[str, Any]:
        """
        Retrieve relevant context for bid generation

        Args:
            rfq_text: RFQ/RFP text to generate bid for
            n_historical_bids: Number of historical bids to retrieve
            n_rfq_chunks: Number of relevant RFQ chunks to retrieve

        Returns:
            Dictionary with context information
        """
        context = {
            'historical_bids': [],
            'similar_rfqs': [],
            'total_context_chunks': 0
        }

        # Search historical bids
        bid_results = self.search_similar(
            query=rfq_text[:1000],  # Use first 1000 chars as query
            document_type="bid",
            n_results=n_historical_bids
        )

        if bid_results['success']:
            context['historical_bids'] = bid_results['results']

        # Search similar RFQs
        rfq_results = self.search_similar(
            query=rfq_text[:1000],
            document_type="rfq",
            n_results=n_rfq_chunks
        )

        if rfq_results['success']:
            context['similar_rfqs'] = rfq_results['results']

        context['total_context_chunks'] = (
            len(context['historical_bids']) +
            len(context['similar_rfqs'])
        )

        return context

    def detect_semantic_conflicts(self,
                                 documents: List[str],
                                 threshold: float = 0.85) -> List[Dict[str, Any]]:
        """
        Detect semantic conflicts between documents using embeddings

        Args:
            documents: List of document texts to compare
            threshold: Similarity threshold for conflict detection

        Returns:
            List of detected conflicts
        """
        if len(documents) < 2:
            return []

        # Generate embeddings for all documents
        embeddings = self.generate_embeddings(documents)

        # Calculate pairwise similarities
        conflicts = []
        for i in range(len(documents)):
            for j in range(i + 1, len(documents)):
                # Cosine similarity
                similarity = np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
                )

                # High similarity might indicate conflict or redundancy
                if similarity > threshold:
                    conflicts.append({
                        'doc1_index': i,
                        'doc2_index': j,
                        'doc1_preview': documents[i][:200],
                        'doc2_preview': documents[j][:200],
                        'similarity_score': float(similarity),
                        'conflict_type': 'semantic_similarity',
                        'severity': 'high' if similarity > 0.95 else 'medium'
                    })

        return conflicts

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about indexed documents

        Returns:
            Dictionary with collection statistics
        """
        return {
            'rfq_documents': self.rfq_collection.count(),
            'historical_bids': self.bids_collection.count(),
            'conflict_documents': self.conflicts_collection.count(),
            'embedding_model': self.model.get_sentence_embedding_dimension(),
            'embedding_dimension': self.embedding_dim,
            'persist_directory': self.persist_directory
        }

    def clear_collection(self, document_type: str) -> bool:
        """
        Clear all documents from a collection

        Args:
            document_type: Type of collection to clear (rfq, bid, conflict)

        Returns:
            True if successful
        """
        try:
            if document_type == "rfq":
                self.client.delete_collection("rfq_documents")
                self.rfq_collection = self.client.create_collection(
                    name="rfq_documents",
                    metadata={"description": "RFQ and RFP documents"}
                )
            elif document_type == "bid":
                self.client.delete_collection("historical_bids")
                self.bids_collection = self.client.create_collection(
                    name="historical_bids",
                    metadata={"description": "Historical winning bids"}
                )
            elif document_type == "conflict":
                self.client.delete_collection("conflict_documents")
                self.conflicts_collection = self.client.create_collection(
                    name="conflict_documents",
                    metadata={"description": "Documents for conflict detection"}
                )
            return True
        except Exception as e:
            print(f"Error clearing collection: {e}")
            return False


# Singleton instance
_rag_service_instance = None

def get_rag_service() -> RAGService:
    """Get or create RAG service singleton instance"""
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = RAGService()
    return _rag_service_instance
