#!/usr/bin/env python3
"""
Quick RAG Initialization Script

This script initializes the RAG system with sample data for immediate use.
"""

import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("=" * 70)
    print("BidForgeAI - RAG Initialization")
    print("=" * 70)
    print()

    try:
        print("Step 1: Importing RAG components...")
        from utils.document_manager import get_document_manager
        from utils.rag_service import get_rag_service
        print("✅ Imports successful")
        print()

        print("Step 2: Initializing RAG service...")
        rag_service = get_rag_service()
        print("✅ RAG service initialized")
        print()

        print("Step 3: Creating sample data...")
        doc_manager = get_document_manager()
        results = doc_manager.create_sample_data()

        if results.get('success'):
            print("✅ Sample data created successfully!")
            print(f"   - RFQs indexed: {results['rfqs_indexed']}")
            print(f"   - Historical bids indexed: {results['bids_indexed']}")
            print(f"   - Total documents: {results['total_indexed']}")
            print()

            # Show stats
            print("Step 4: Verifying RAG database...")
            stats = rag_service.get_collection_stats()
            print("✅ RAG database ready!")
            print(f"   - RFQ documents: {stats['rfq_documents']}")
            print(f"   - Historical bids: {stats['historical_bids']}")
            print(f"   - Embedding dimension: {stats['embedding_dimension']}")
            print()

            print("=" * 70)
            print("🎉 RAG system initialized successfully!")
            print("=" * 70)
            print()
            print("You can now:")
            print("  1. Run the Streamlit app: streamlit run app.py")
            print("  2. Run full tests: python test_rag.py")
            print("  3. Index your own documents using the Document Manager")
            print()

            return 0
        else:
            print("❌ Failed to create sample data")
            return 1

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print()
        print("Please install required dependencies:")
        print("  pip install numpy sentence-transformers chromadb")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
