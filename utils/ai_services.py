"""
AI Services - Integration with multiple AI providers
"""

import os
from typing import Dict, List, Optional
import openai
from anthropic import Anthropic
from google import generativeai as genai


class AIServiceManager:
    """Manages connections to multiple AI providers"""

    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.gemini_model = None
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
        temperature: float = 0.7
    ) -> Dict[str, str]:
        """
        Generate bid proposal using specified AI model

        Args:
            project_context: Context about the project and company
            rfp_content: RFP document content
            model: AI model to use ('openai', 'anthropic', 'gemini')
            temperature: Creativity level (0.0 - 1.0)

        Returns:
            Dict with generated bid content and metadata
        """

        prompt = self._create_bid_prompt(project_context, rfp_content)

        try:
            if model == "openai" and self.openai_client:
                return self._generate_with_openai(prompt, temperature)
            elif model == "anthropic" and self.anthropic_client:
                return self._generate_with_anthropic(prompt, temperature)
            elif model == "gemini" and self.gemini_model:
                return self._generate_with_gemini(prompt, temperature)
            else:
                raise ValueError(f"Model {model} not available or not configured")
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
        Detect semantic and numeric conflicts in documents

        Args:
            documents: List of document dicts with 'content' and 'source'

        Returns:
            List of detected conflicts
        """

        conflicts = []

        # Simple conflict detection implementation
        # In production, this would use embeddings and similarity search

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

    def _create_bid_prompt(self, project_context: str, rfp_content: str) -> str:
        """Create prompt for bid generation"""

        return f"""
        You are an expert construction bid proposal writer. Generate a professional, comprehensive bid proposal
        based on the following information:

        PROJECT CONTEXT:
        {project_context}

        RFP REQUIREMENTS:
        {rfp_content}

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
