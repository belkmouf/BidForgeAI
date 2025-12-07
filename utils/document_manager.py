"""
Document Manager - Helper functions for RAG document indexing and management
"""

import os
from typing import List, Dict, Any, Optional
from pathlib import Path

from .rag_service import get_rag_service
from .document_processor import DocumentProcessor


class DocumentManager:
    """Manager for document operations and RAG indexing"""

    def __init__(self):
        self.rag_service = get_rag_service()
        self.doc_processor = DocumentProcessor()

    def index_project_documents(self,
                                project_path: str,
                                file_patterns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Index all documents in a project directory

        Args:
            project_path: Path to project directory
            file_patterns: Optional list of file patterns (e.g., ['*.pdf', '*.docx'])

        Returns:
            Dictionary with indexing results
        """
        if file_patterns is None:
            file_patterns = ['*.pdf', '*.docx', '*.txt']

        results = {
            'indexed': [],
            'failed': [],
            'total_chunks': 0
        }

        project_dir = Path(project_path)
        if not project_dir.exists():
            return {
                'error': f'Project path does not exist: {project_path}',
                'success': False
            }

        # Find all matching files
        files_to_index = []
        for pattern in file_patterns:
            files_to_index.extend(project_dir.glob(f'**/{pattern}'))

        # Index each file
        for file_path in files_to_index:
            try:
                # Determine document type based on filename/path
                doc_type = self._determine_doc_type(str(file_path))

                # Index the document
                result = self.rag_service.index_document(
                    file_path=str(file_path),
                    document_type=doc_type,
                    metadata={
                        'project': os.path.basename(project_path),
                        'doc_id': file_path.stem
                    }
                )

                if result.get('success'):
                    results['indexed'].append({
                        'file': str(file_path),
                        'type': doc_type,
                        'chunks': result.get('chunks_indexed', 0)
                    })
                    results['total_chunks'] += result.get('chunks_indexed', 0)
                else:
                    results['failed'].append({
                        'file': str(file_path),
                        'error': result.get('error', 'Unknown error')
                    })

            except Exception as e:
                results['failed'].append({
                    'file': str(file_path),
                    'error': str(e)
                })

        results['success'] = True
        results['total_files'] = len(files_to_index)
        results['indexed_count'] = len(results['indexed'])
        results['failed_count'] = len(results['failed'])

        return results

    def _determine_doc_type(self, file_path: str) -> str:
        """
        Determine document type based on filename

        Args:
            file_path: Path to the file

        Returns:
            Document type: 'rfq', 'bid', or 'conflict'
        """
        file_path_lower = file_path.lower()

        # Check for RFQ/RFP keywords
        if any(keyword in file_path_lower for keyword in ['rfq', 'rfp', 'request', 'proposal_request']):
            return 'rfq'

        # Check for bid/proposal keywords
        if any(keyword in file_path_lower for keyword in ['bid', 'proposal', 'winning', 'historical']):
            return 'bid'

        # Default to conflict detection
        return 'conflict'

    def create_sample_data(self) -> Dict[str, Any]:
        """
        Create sample documents for testing RAG functionality

        Returns:
            Dictionary with creation results
        """
        sample_rfqs = [
            {
                'content': """
                REQUEST FOR QUOTATION - Commercial Building Construction

                Project: Dubai Marina Tower Complex
                Location: Dubai Marina, Dubai, UAE
                Project ID: PRJ-001

                Scope of Work:
                - Construction of 45-story mixed-use tower
                - Total built-up area: 850,000 sq ft
                - Includes residential units, retail spaces, and parking
                - High-end finishes with premium materials
                - LEED Gold certification required

                Technical Requirements:
                - Foundation: Piled foundation with basement levels
                - Structure: Reinforced concrete frame with steel elements
                - Façade: Curtain wall system with energy-efficient glazing
                - MEP: Full HVAC, electrical, plumbing, and fire safety systems

                Timeline: 24 months from mobilization
                Budget Range: $10M - $15M
                Submission Deadline: January 15, 2026
                """,
                'metadata': {'doc_id': 'rfq_dubai_marina_001', 'project': 'Dubai Marina'}
            },
            {
                'content': """
                REQUEST FOR PROPOSAL - Infrastructure Project

                Project: Abu Dhabi Highway Extension
                Location: Abu Dhabi, UAE
                Project ID: PRJ-002

                Scope of Work:
                - Extension of existing highway network (15 km)
                - 6-lane expressway with emergency lanes
                - 3 major interchanges with ramps
                - Street lighting and road signage
                - Drainage and utilities relocation

                Technical Requirements:
                - Asphalt concrete pavement design
                - Bridge construction for 2 overpasses
                - Traffic management during construction
                - Environmental impact mitigation

                Timeline: 18 months
                Budget Range: $25M - $30M
                Submission Deadline: February 1, 2026
                """,
                'metadata': {'doc_id': 'rfq_highway_002', 'project': 'Highway Extension'}
            },
            {
                'content': """
                REQUEST FOR QUOTATION - Sports Facility

                Project: Qatar Sports Stadium
                Location: Doha, Qatar
                Project ID: PRJ-004

                Scope of Work:
                - Multi-purpose sports stadium with 25,000 seating capacity
                - Olympic-standard track and field facilities
                - Indoor sports complex with basketball and volleyball courts
                - VIP lounges and premium seating areas
                - State-of-the-art audiovisual systems

                Technical Requirements:
                - Retractable roof structure
                - Climate-controlled environment
                - Advanced acoustics and lighting
                - Accessible facilities for disabled persons

                Timeline: 30 months
                Budget Range: $45M - $55M
                Submission Deadline: January 30, 2026
                """,
                'metadata': {'doc_id': 'rfq_stadium_004', 'project': 'Qatar Stadium'}
            }
        ]

        sample_bids = [
            {
                'content': """
                WINNING BID PROPOSAL - Luxury Residential Tower

                Executive Summary:
                Our company is pleased to submit this comprehensive proposal for the construction
                of the premium residential tower. With 20+ years of experience in high-rise
                construction across the GCC region, we bring proven expertise in delivering
                luxury projects on time and within budget.

                Technical Approach:
                We propose a phased construction methodology utilizing:
                - Advanced BIM (Building Information Modeling) for coordination
                - Just-in-time material delivery to optimize site logistics
                - Prefabricated components for faster construction
                - ISO 9001 quality management system

                Project Team:
                - Project Manager: 15+ years in high-rise construction
                - Site Engineer: LEED AP certified
                - Safety Manager: OSHA 30-hour certified
                - Quality Control: Six Sigma Black Belt

                Timeline: 22 months (2 months ahead of schedule)
                Total Investment: $12.5M (within budget)

                Risk Mitigation:
                - Comprehensive insurance coverage
                - Weather contingency planning
                - Supply chain backup vendors
                - Weekly progress reporting

                This project aligns perfectly with our portfolio of successful luxury
                developments including similar projects in Dubai and Abu Dhabi.
                """,
                'metadata': {'doc_id': 'bid_luxury_tower_win', 'project': 'Luxury Tower', 'won': True}
            },
            {
                'content': """
                PROPOSAL - Highway Infrastructure Development

                Company Qualifications:
                As a leading infrastructure contractor in the Middle East, we have successfully
                completed over 200 km of highway projects across the UAE and GCC region.
                Our track record includes:
                - Dubai-Al Ain Highway expansion (2023)
                - Sharjah Ring Road development (2022)
                - Abu Dhabi Coastal Road improvements (2021)

                Technical Methodology:
                1. Survey and Planning Phase (Weeks 1-4)
                   - Detailed topographical survey
                   - Geotechnical investigation
                   - Utility mapping and coordination

                2. Earthworks and Foundation (Months 2-6)
                   - Site clearing and grading
                   - Drainage system installation
                   - Subgrade preparation

                3. Pavement Construction (Months 7-14)
                   - Base course laying
                   - Asphalt concrete paving
                   - Quality testing at each layer

                4. Finishing Works (Months 15-18)
                   - Road markings and signage
                   - Lighting installation
                   - Landscaping and final touches

                Safety and Environment:
                - Zero-accident safety program
                - Dust suppression measures
                - Noise control during construction
                - Traffic management plan

                Proposed Investment: $27.8M
                Timeline: 17 months (1 month ahead of schedule)
                """,
                'metadata': {'doc_id': 'bid_highway_proposal', 'project': 'Highway', 'won': True}
            }
        ]

        results = {'rfqs_indexed': 0, 'bids_indexed': 0, 'errors': []}

        # Index sample RFQs
        for rfq in sample_rfqs:
            try:
                # Create chunks directly
                chunks = self.doc_processor.chunk_text(rfq['content'])
                embeddings = self.rag_service.generate_embeddings(chunks)

                # Store in RAG
                doc_id = rfq['metadata']['doc_id']
                ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]

                metadatas = []
                for i in range(len(chunks)):
                    meta = rfq['metadata'].copy()
                    meta['chunk_index'] = i
                    meta['document_type'] = 'rfq'
                    metadatas.append(meta)

                self.rag_service.rfq_collection.add(
                    ids=ids,
                    embeddings=embeddings.tolist(),
                    documents=chunks,
                    metadatas=metadatas
                )

                results['rfqs_indexed'] += 1

            except Exception as e:
                results['errors'].append({'type': 'rfq', 'error': str(e)})

        # Index sample bids
        for bid in sample_bids:
            try:
                chunks = self.doc_processor.chunk_text(bid['content'])
                embeddings = self.rag_service.generate_embeddings(chunks)

                doc_id = bid['metadata']['doc_id']
                ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]

                metadatas = []
                for i in range(len(chunks)):
                    meta = bid['metadata'].copy()
                    meta['chunk_index'] = i
                    meta['document_type'] = 'bid'
                    metadatas.append(meta)

                self.rag_service.bids_collection.add(
                    ids=ids,
                    embeddings=embeddings.tolist(),
                    documents=chunks,
                    metadatas=metadatas
                )

                results['bids_indexed'] += 1

            except Exception as e:
                results['errors'].append({'type': 'bid', 'error': str(e)})

        results['success'] = True
        results['total_indexed'] = results['rfqs_indexed'] + results['bids_indexed']

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get current RAG statistics"""
        return self.rag_service.get_collection_stats()


# Singleton instance
_document_manager_instance = None

def get_document_manager() -> DocumentManager:
    """Get or create document manager singleton"""
    global _document_manager_instance
    if _document_manager_instance is None:
        _document_manager_instance = DocumentManager()
    return _document_manager_instance
