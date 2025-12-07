# RAG Implementation for BidForgeAI

## Overview

This document describes the Retrieval-Augmented Generation (RAG) implementation for the BidForgeAI application, which enables context-aware bid generation and semantic conflict detection.

## Architecture

### Components

1. **RAG Service** (`utils/rag_service.py`)
   - Core RAG functionality
   - Embeddings generation using Sentence Transformers
   - Vector storage using ChromaDB
   - Semantic search and similarity matching

2. **Document Manager** (`utils/document_manager.py`)
   - Document indexing pipeline
   - Batch processing of project documents
   - Sample data creation for testing

3. **AI Services Integration** (`utils/ai_services.py`)
   - RAG-enhanced bid generation
   - Semantic conflict detection using embeddings
   - Multi-model support (OpenAI, Claude, Gemini)

4. **UI Integration** (`pages/bid_generation.py`, `pages/conflict_detection.py`)
   - Real-time RAG statistics display
   - Context-aware bid generation interface

## Features

### 1. Document Indexing

The RAG service can index various document types:
- **RFQ/RFP documents**: Request for Quotation/Proposal files
- **Historical bids**: Past winning bid proposals
- **Conflict documents**: Documents for semantic conflict analysis

**Supported file formats:**
- PDF (.pdf)
- Word documents (.docx)
- Text files (.txt)
- Excel spreadsheets (.xlsx)
- Outlook emails (.msg)

### 2. Embeddings

- **Model**: `all-MiniLM-L6-v2` (Sentence Transformers)
- **Dimension**: 384-dimensional vectors
- **Features**:
  - Fast inference
  - Good balance between quality and speed
  - Multilingual support

### 3. Vector Storage

- **Database**: ChromaDB with persistent storage
- **Collections**:
  - `rfq_documents`: RFQ/RFP content
  - `historical_bids`: Past winning bids
  - `conflict_documents`: Documents for conflict detection

### 4. Semantic Search

- **Cosine similarity** for vector matching
- **Configurable result count**
- **Similarity scoring** (distance → similarity conversion)
- **Metadata filtering** for refined searches

### 5. Context-Aware Bid Generation

When generating bids, the RAG system:
1. Takes the RFQ text as input
2. Searches for similar historical winning bids
3. Retrieves relevant RFQ chunks from the database
4. Provides context to the LLM for bid generation
5. Ensures consistency with past successful approaches

### 6. Semantic Conflict Detection

The RAG service can detect:
- **Semantic similarities** between documents (potential conflicts)
- **Redundant information** across multiple sources
- **Contradictory statements** (high similarity with opposite meanings)

**Conflict severity levels:**
- **High**: Similarity > 95%
- **Medium**: Similarity > 85%

## Usage

### Initialize RAG Service

```python
from utils.rag_service import get_rag_service

rag_service = get_rag_service()
```

### Index a Document

```python
result = rag_service.index_document(
    file_path="/path/to/document.pdf",
    document_type="rfq",  # or "bid", "conflict"
    metadata={
        "project": "Dubai Tower",
        "doc_id": "rfq_001"
    }
)
```

### Search for Similar Documents

```python
results = rag_service.search_similar(
    query="luxury high-rise construction",
    document_type="bid",
    n_results=5
)

for result in results['results']:
    print(f"Similarity: {result['similarity_score']:.2%}")
    print(f"Document: {result['document'][:200]}...")
```

### Get Context for Bid Generation

```python
context = rag_service.get_context_for_bid(
    rfq_text="Full RFQ text here...",
    n_historical_bids=5,
    n_rfq_chunks=10
)

print(f"Historical bids found: {len(context['historical_bids'])}")
print(f"Relevant RFQ chunks: {len(context['similar_rfqs'])}")
```

### Detect Semantic Conflicts

```python
from utils.ai_services import ai_service

documents = [
    {'content': 'Document 1 text...', 'source': 'RFQ.pdf'},
    {'content': 'Document 2 text...', 'source': 'Spec.pdf'}
]

conflicts = ai_service.detect_conflicts(documents)

for conflict in conflicts:
    print(f"Conflict: {conflict['description']}")
    print(f"Similarity: {conflict['similarity_score']:.2%}")
```

### Create Sample Data

```python
from utils.document_manager import get_document_manager

doc_manager = get_document_manager()
results = doc_manager.create_sample_data()

print(f"RFQs indexed: {results['rfqs_indexed']}")
print(f"Bids indexed: {results['bids_indexed']}")
```

### Get Statistics

```python
stats = rag_service.get_collection_stats()

print(f"RFQ documents: {stats['rfq_documents']}")
print(f"Historical bids: {stats['historical_bids']}")
print(f"Embedding dimension: {stats['embedding_dimension']}")
```

## Testing

Run the comprehensive test suite:

```bash
python test_rag.py
```

This will test:
1. RAG service initialization
2. Sample data creation
3. Similarity search
4. Context retrieval for bid generation
5. Semantic conflict detection
6. Statistics and metrics

## Performance

### Indexing Speed
- **Small document** (<10 pages): ~1-2 seconds
- **Medium document** (10-50 pages): ~3-5 seconds
- **Large document** (50+ pages): ~5-10 seconds

### Search Speed
- **Typical query**: ~50-200ms
- **Batch queries**: Parallel processing available

### Storage
- **ChromaDB**: Persistent storage in `./chroma_db/`
- **Embedding size**: ~1.5KB per chunk
- **Typical document**: 500KB - 2MB indexed

## Configuration

### Embedding Model

To use a different Sentence Transformer model:

```python
rag_service = RAGService(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)
```

**Popular alternatives:**
- `all-mpnet-base-v2`: Higher quality, slower (768 dim)
- `paraphrase-MiniLM-L3-v2`: Faster, smaller (384 dim)
- `multi-qa-mpnet-base-dot-v1`: Optimized for Q&A

### Chunk Size

Default: 1000 characters with 200 character overlap

```python
from utils.document_processor import DocumentProcessor

doc_processor = DocumentProcessor()
chunks = doc_processor.chunk_text(
    text="Your document text...",
    chunk_size=1500,  # Custom size
    overlap=300       # Custom overlap
)
```

### Similarity Threshold

For conflict detection:

```python
conflicts = rag_service.detect_semantic_conflicts(
    documents=docs,
    threshold=0.90  # Stricter threshold
)
```

## Integration with Streamlit UI

The RAG system is integrated into the Streamlit interface:

### Bid Generation Page

```python
# Shows real-time RAG stats
from utils.rag_service import get_rag_service

rag_service = get_rag_service()
stats = rag_service.get_collection_stats()

# Display in UI
st.write(f"RFQ documents: {stats['rfq_documents']}")
st.write(f"Historical bids: {stats['historical_bids']}")
```

### Conflict Detection Page

```python
from utils.ai_services import ai_service

# Use RAG-enhanced conflict detection
conflicts = ai_service.detect_conflicts(documents)
```

## Troubleshooting

### ChromaDB Errors

If you encounter ChromaDB initialization errors:

```bash
rm -rf ./chroma_db
python test_rag.py  # Will reinitialize
```

### Out of Memory

For large documents, reduce chunk size:

```python
chunks = doc_processor.chunk_text(text, chunk_size=500, overlap=100)
```

### Slow Embedding Generation

Use GPU acceleration (if available):

```python
model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')
```

## Future Enhancements

1. **PostgreSQL with pgvector**: Production-ready vector database
2. **Hybrid search**: Combine keyword + semantic search
3. **Re-ranking**: Improve result quality with cross-encoder
4. **Multi-modal embeddings**: Support images and diagrams
5. **Incremental updates**: Update embeddings without full reindex
6. **Query optimization**: Cache frequent searches
7. **Advanced chunking**: Semantic chunking based on document structure

## Dependencies

```
numpy>=1.24.0
sentence-transformers>=3.3.1
chromadb>=0.5.23
```

Optional (for production):
```
faiss-cpu>=1.9.0
pgvector>=0.3.6
psycopg2-binary>=2.9.10
```

## License

Part of BidForgeAI project.

## Support

For issues or questions about the RAG implementation, please refer to the test script (`test_rag.py`) or contact the development team.
