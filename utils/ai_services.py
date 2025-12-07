"""
AI Services - Integration with multiple AI providers
"""

import os
from typing import Dict, List, Optional
import openai
from anthropic import Anthropic
from google import generativeai as genai

from .rag_service import get_rag_service


class AIServiceManager:
    """Manages connections to multiple AI providers"""

    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.gemini_model = None
        self.rag_service = get_rag_service()
        self.initialize_clients()

    def initialize_clients(self):
        """Initialize AI client connections"""
        # OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            self.openai_client = openai.OpenAI(api_key=openai_key)

        # Anthropic
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key:
            self.anthropic_client = Anthropic(api_key=anthropic_key)

        # Google Gemini
        gemini_key = os.getenv("GOOGLE_API_KEY")
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def generate_bid(
        self,
        project_context: str,
        rfp_content: str,
        model: str = "openai",
        temperature: float = 0.7,
        use_rag: bool = True
    ) -> Dict[str, str]:
        """
        Generate bid proposal using specified AI model with RAG context

        Args:
            project_context: Context about the project and company
            rfp_content: RFP document content
            model: AI model to use ('openai', 'anthropic', 'gemini')
            temperature: Creativity level (0.0 - 1.0)
            use_rag: Whether to use RAG for context retrieval

        Returns:
            Dict with generated bid content and metadata
        """

        # Get RAG context if enabled
        rag_context = None
        if use_rag:
            try:
                rag_context = self.rag_service.get_context_for_bid(
                    rfp_text=rfp_content,
                    n_historical_bids=5,
                    n_rfq_chunks=10
                )
            except Exception as e:
                print(f"RAG context retrieval failed: {e}")
                rag_context = None

        prompt = self._create_bid_prompt(project_context, rfp_content, rag_context)

        try:
            if model == "openai" and self.openai_client:
                result = self._generate_with_openai(prompt, temperature)
            elif model == "anthropic" and self.anthropic_client:
                result = self._generate_with_anthropic(prompt, temperature)
            elif model == "gemini" and self.gemini_model:
                result = self._generate_with_gemini(prompt, temperature)
            else:
                raise ValueError(f"Model {model} not available or not configured")

            # Add RAG metadata to result
            if rag_context:
                result['rag_context'] = {
                    'historical_bids_count': len(rag_context.get('historical_bids', [])),
                    'similar_rfqs_count': len(rag_context.get('similar_rfqs', [])),
                    'total_context_chunks': rag_context.get('total_context_chunks', 0)
                }

            return result
        except Exception as e:
            return {
                "content": "",
                "model": model,
                "error": str(e),
                "success": False
            }

    def analyze_rfp(
        self,
        rfp_content: str,
        historical_data: Optional[str] = None
    ) -> Dict:
        """
        Analyze RFP document and provide risk assessment

        Args:
            rfp_content: RFP document content
            historical_data: Historical project data for context

        Returns:
            Dict with analysis scores and recommendations
        """

        prompt = f"""
        Analyze the following RFP document and provide a comprehensive risk assessment:

        RFP Content:
        {rfp_content}

        {f"Historical Context: {historical_data}" if historical_data else ""}

        Provide your analysis in the following JSON format:
        {{
            "quality_score": <0-100>,
            "clarity_score": <0-100>,
            "doability_score": <0-100>,
            "vendor_risk_score": <0-100>,
            "overall_risk": "<Low|Medium|High|Critical>",
            "key_findings": [
                {{
                    "category": "<category>",
                    "status": "<positive|warning|negative>",
                    "title": "<title>",
                    "description": "<description>"
                }}
            ],
            "red_flags": [
                {{
                    "severity": "<Low|Medium|High|Critical>",
                    "title": "<title>",
                    "description": "<description>"
                }}
            ],
            "opportunities": [
                {{
                    "impact": "<Low|Medium|High>",
                    "title": "<title>",
                    "description": "<description>"
                }}
            ],
            "recommendations": [
                {{
                    "priority": "<Low|Medium|High>",
                    "action": "<action>",
                    "description": "<description>",
                    "estimated_time": "<time>",
                    "owner": "<role>"
                }}
            ]
        }}
        """

        try:
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                import json
                return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {
                "error": str(e),
                "success": False
            }

    def detect_conflicts(
        self,
        documents: List[Dict[str, str]]
    ) -> List[Dict]:
        """
        Detect semantic and numeric conflicts in documents using embeddings

        Args:
            documents: List of document dicts with 'content' and 'source'

        Returns:
            List of detected conflicts
        """

        conflicts = []

        # Extract document contents
        doc_texts = [doc.get('content', '') for doc in documents if doc.get('content')]

        if len(doc_texts) < 2:
            return conflicts

        try:
            # Use RAG service for semantic conflict detection
            semantic_conflicts = self.rag_service.detect_semantic_conflicts(
                documents=doc_texts,
                threshold=0.85
            )

            # Format conflicts with source information
            for conflict in semantic_conflicts:
                idx1 = conflict['doc1_index']
                idx2 = conflict['doc2_index']

                conflicts.append({
                    'type': 'semantic',
                    'severity': conflict['severity'],
                    'source1': documents[idx1].get('source', f'Document {idx1+1}'),
                    'source2': documents[idx2].get('source', f'Document {idx2+1}'),
                    'description': f"High semantic similarity detected between documents (similarity: {conflict['similarity_score']:.2%})",
                    'snippet1': conflict['doc1_preview'],
                    'snippet2': conflict['doc2_preview'],
                    'similarity_score': conflict['similarity_score'],
                    'confidence': int(conflict['similarity_score'] * 100)
                })

        except Exception as e:
            print(f"Semantic conflict detection failed: {e}")

        return conflicts

    def calculate_win_probability(
        self,
        project_features: Dict
    ) -> Dict:
        """
        Calculate win probability based on project features

        Args:
            project_features: Dict of extracted project features

        Returns:
            Dict with probability, confidence, and recommendations
        """

        # Simple weighted scoring model
        # In production, this would use a trained ML model

        weights = {
            'project_type_score': 0.15,
            'client_relationship_score': 0.20,
            'competitiveness_score': 0.15,
            'team_capacity_score': 0.10,
            'timeline_score': 0.10,
            'complexity_score': 0.10,
            'requirements_clarity_score': 0.10,
            'budget_alignment_score': 0.10
        }

        weighted_sum = sum(
            project_features.get(key, 50) * weight
            for key, weight in weights.items()
        )

        # Apply sigmoid transformation
        import math
        probability = 1 / (1 + math.exp(-0.05 * (weighted_sum - 50)))
        probability_pct = int(probability * 100)

        return {
            "win_probability": probability_pct,
            "confidence": 85,
            "features": project_features,
            "success": True
        }

    def _create_bid_prompt(self, project_context: str, rfp_content: str, rag_context: Optional[Dict] = None) -> str:
        """Create prompt for bid generation with optional RAG context"""

        # Build RAG context section
        rag_section = ""
        if rag_context and rag_context.get('total_context_chunks', 0) > 0:
            rag_section = "\n\nRELEVANT HISTORICAL CONTEXT:\n"

            # Add historical bids
            if rag_context.get('historical_bids'):
                rag_section += "\nSimilar Winning Bids:\n"
                for i, bid in enumerate(rag_context['historical_bids'][:3], 1):
                    rag_section += f"\n{i}. {bid['document'][:500]}...\n"

            # Add similar RFQs
            if rag_context.get('similar_rfqs'):
                rag_section += "\nSimilar RFQ/RFP Requirements:\n"
                for i, rfq in enumerate(rag_context['similar_rfqs'][:3], 1):
                    rag_section += f"\n{i}. {rfq['document'][:500]}...\n"

        return f"""
        You are an expert construction bid proposal writer. Generate a professional, comprehensive bid proposal
        based on the following information:

        PROJECT CONTEXT:
        {project_context}

        RFP REQUIREMENTS:
        {rfp_content}
        {rag_section}

        Generate a complete HTML bid proposal document that includes:
        1. Executive Summary
        2. Company Qualifications and Experience
        3. Technical Approach and Methodology
        4. Project Timeline and Schedule
        5. Pricing and Investment Summary
        6. Risk Mitigation and Safety Protocols
        7. Quality Assurance Measures
        8. References and Past Projects

        Format the output as professional HTML with appropriate styling for printing.
        Use persuasive but professional language appropriate for C-level executives.
        {f"Use the historical context provided to ensure consistency with past successful bids." if rag_section else ""}
        """

    def _generate_with_openai(self, prompt: str, temperature: float) -> Dict:
        """Generate content using OpenAI"""

        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=4000
        )

        return {
            "content": response.choices[0].message.content,
            "model": "gpt-4o",
            "tokens": response.usage.total_tokens,
            "success": True
        }

    def _generate_with_anthropic(self, prompt: str, temperature: float) -> Dict:
        """Generate content using Anthropic Claude"""

        response = self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "content": response.content[0].text,
            "model": "claude-sonnet-4-20250514",
            "tokens": response.usage.input_tokens + response.usage.output_tokens,
            "success": True
        }

    def _generate_with_gemini(self, prompt: str, temperature: float) -> Dict:
        """Generate content using Google Gemini"""

        response = self.gemini_model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=4000
            )
        )

        return {
            "content": response.text,
            "model": "gemini-2.0-flash-exp",
            "success": True
        }


# Global instance
ai_service = AIServiceManager()
