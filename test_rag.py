#!/usr/bin/env python3
"""
Test RAG Implementation

This script tests the RAG functionality by:
1. Initializing the RAG service
2. Creating sample documents
3. Testing document indexing
4. Testing similarity search
5. Testing conflict detection
"""

import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.rag_service import get_rag_service
from utils.document_manager import get_document_manager
from utils.ai_services import ai_service


def test_rag_initialization():
    """Test RAG service initialization"""
    print("=" * 80)
    print("TEST 1: RAG Service Initialization")
    print("=" * 80)

    try:
        rag_service = get_rag_service()
        print("✅ RAG service initialized successfully")

        stats = rag_service.get_collection_stats()
        print(f"\nInitial statistics:")
        print(f"  - RFQ documents: {stats['rfq_documents']}")
        print(f"  - Historical bids: {stats['historical_bids']}")
        print(f"  - Conflict documents: {stats['conflict_documents']}")
        print(f"  - Embedding dimension: {stats['embedding_dimension']}")
        print(f"  - Model: {stats['embedding_model']}")

        return True
    except Exception as e:
        print(f"❌ Failed to initialize RAG service: {e}")
        return False


def test_sample_data_creation():
    """Test creation of sample data"""
    print("\n" + "=" * 80)
    print("TEST 2: Sample Data Creation")
    print("=" * 80)

    try:
        doc_manager = get_document_manager()
        print("Creating sample RFQs and historical bids...")

        results = doc_manager.create_sample_data()

        if results.get('success'):
            print(f"✅ Sample data created successfully")
            print(f"  - RFQs indexed: {results['rfqs_indexed']}")
            print(f"  - Bids indexed: {results['bids_indexed']}")
            print(f"  - Total documents: {results['total_indexed']}")

            if results['errors']:
                print(f"\n⚠️  Errors encountered:")
                for error in results['errors']:
                    print(f"    - {error['type']}: {error['error']}")

            return True
        else:
            print(f"❌ Failed to create sample data")
            return False

    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_similarity_search():
    """Test similarity search functionality"""
    print("\n" + "=" * 80)
    print("TEST 3: Similarity Search")
    print("=" * 80)

    try:
        rag_service = get_rag_service()

        # Test query for similar RFQs
        query = "high-rise building construction with luxury finishes"
        print(f"\nQuery: '{query}'")
        print("Searching RFQ collection...")

        results = rag_service.search_similar(
            query=query,
            document_type="rfq",
            n_results=3
        )

        if results.get('success'):
            print(f"✅ Found {results['total_found']} similar documents")

            for i, result in enumerate(results['results'][:3], 1):
                print(f"\n  Result {i}:")
                print(f"    - ID: {result['id']}")
                print(f"    - Similarity: {result['similarity_score']:.2%}")
                print(f"    - Preview: {result['document'][:150]}...")

            # Test query for historical bids
            query2 = "project timeline and methodology"
            print(f"\n\nQuery: '{query2}'")
            print("Searching historical bids collection...")

            results2 = rag_service.search_similar(
                query=query2,
                document_type="bid",
                n_results=3
            )

            if results2.get('success'):
                print(f"✅ Found {results2['total_found']} similar bids")

                for i, result in enumerate(results2['results'][:3], 1):
                    print(f"\n  Result {i}:")
                    print(f"    - ID: {result['id']}")
                    print(f"    - Similarity: {result['similarity_score']:.2%}")
                    print(f"    - Preview: {result['document'][:150]}...")

            return True
        else:
            print(f"❌ Search failed: {results.get('message', 'Unknown error')}")
            return False

    except Exception as e:
        print(f"❌ Error during similarity search: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_context_retrieval():
    """Test context retrieval for bid generation"""
    print("\n" + "=" * 80)
    print("TEST 4: Context Retrieval for Bid Generation")
    print("=" * 80)

    try:
        rag_service = get_rag_service()

        rfq_text = """
        We need a construction contractor for a 40-story luxury residential tower
        in Dubai. The project includes high-end finishes, premium materials,
        and must achieve LEED certification. Timeline is 24 months with a budget
        of $12 million.
        """

        print("RFQ Text:")
        print(rfq_text)
        print("\nRetrieving relevant context...")

        context = rag_service.get_context_for_bid(
            rfq_text=rfq_text,
            n_historical_bids=3,
            n_rfq_chunks=5
        )

        print(f"✅ Context retrieved successfully")
        print(f"  - Historical bids found: {len(context['historical_bids'])}")
        print(f"  - Similar RFQ chunks found: {len(context['similar_rfqs'])}")
        print(f"  - Total context chunks: {context['total_context_chunks']}")

        if context['historical_bids']:
            print(f"\n  Top historical bid:")
            top_bid = context['historical_bids'][0]
            print(f"    - ID: {top_bid['id']}")
            print(f"    - Similarity: {top_bid['similarity_score']:.2%}")
            print(f"    - Preview: {top_bid['document'][:200]}...")

        return True

    except Exception as e:
        print(f"❌ Error during context retrieval: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_conflict_detection():
    """Test semantic conflict detection"""
    print("\n" + "=" * 80)
    print("TEST 5: Semantic Conflict Detection")
    print("=" * 80)

    try:
        # Test documents with semantic similarity
        documents = [
            "The project budget is $10 million with a 20-month timeline.",
            "Total investment required is approximately $10M over 20 months duration.",
            "The sports facility will include a retractable roof and climate control.",
            "This highway project requires asphalt paving and drainage systems."
        ]

        print("Testing documents:")
        for i, doc in enumerate(documents, 1):
            print(f"  {i}. {doc}")

        print("\nDetecting semantic conflicts...")

        conflicts = ai_service.detect_conflicts([
            {'content': doc, 'source': f'Document {i}'}
            for i, doc in enumerate(documents, 1)
        ])

        print(f"✅ Conflict detection complete")
        print(f"  - Conflicts found: {len(conflicts)}")

        if conflicts:
            for i, conflict in enumerate(conflicts, 1):
                print(f"\n  Conflict {i}:")
                print(f"    - Type: {conflict['type']}")
                print(f"    - Severity: {conflict['severity']}")
                print(f"    - Between: {conflict['source1']} and {conflict['source2']}")
                print(f"    - Similarity: {conflict['similarity_score']:.2%}")
                print(f"    - Description: {conflict['description']}")

        return True

    except Exception as e:
        print(f"❌ Error during conflict detection: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_statistics():
    """Display final statistics"""
    print("\n" + "=" * 80)
    print("FINAL STATISTICS")
    print("=" * 80)

    try:
        doc_manager = get_document_manager()
        stats = doc_manager.get_stats()

        print(f"\nRAG Database Statistics:")
        print(f"  - RFQ documents indexed: {stats['rfq_documents']}")
        print(f"  - Historical bids indexed: {stats['historical_bids']}")
        print(f"  - Conflict documents indexed: {stats['conflict_documents']}")
        print(f"  - Embedding dimension: {stats['embedding_dimension']}")
        print(f"  - Persist directory: {stats['persist_directory']}")

        return True

    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "BidForgeAI - RAG Implementation Test" + " " * 22 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    tests = [
        ("Initialization", test_rag_initialization),
        ("Sample Data Creation", test_sample_data_creation),
        ("Similarity Search", test_similarity_search),
        ("Context Retrieval", test_context_retrieval),
        ("Conflict Detection", test_conflict_detection),
        ("Statistics", test_statistics),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! RAG implementation is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
