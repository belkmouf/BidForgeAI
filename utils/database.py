"""
Database utilities for BidForge AI
Simple file-based storage for demonstration
In production, this would use PostgreSQL with pgvector
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class Database:
    """Simple file-based database for demonstration"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        # Create subdirectories
        (self.data_dir / "projects").mkdir(exist_ok=True)
        (self.data_dir / "documents").mkdir(exist_ok=True)
        (self.data_dir / "analyses").mkdir(exist_ok=True)
        (self.data_dir / "bids").mkdir(exist_ok=True)
        (self.data_dir / "conflicts").mkdir(exist_ok=True)
        (self.data_dir / "predictions").mkdir(exist_ok=True)

    # Project Management
    def create_project(self, project_data: Dict) -> str:
        """Create a new project"""
        project_id = f"PRJ-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        project_data['id'] = project_id
        project_data['created_at'] = datetime.now().isoformat()
        project_data['updated_at'] = datetime.now().isoformat()
        project_data['status'] = project_data.get('status', 'Active')

        file_path = self.data_dir / "projects" / f"{project_id}.json"
        with open(file_path, 'w') as f:
            json.dump(project_data, f, indent=2)

        return project_id

    def get_project(self, project_id: str) -> Optional[Dict]:
        """Get project by ID"""
        file_path = self.data_dir / "projects" / f"{project_id}.json"

        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return None

    def update_project(self, project_id: str, updates: Dict) -> bool:
        """Update project data"""
        project = self.get_project(project_id)

        if project:
            project.update(updates)
            project['updated_at'] = datetime.now().isoformat()

            file_path = self.data_dir / "projects" / f"{project_id}.json"
            with open(file_path, 'w') as f:
                json.dump(project, f, indent=2)
            return True

        return False

    def list_projects(self, status: Optional[str] = None) -> List[Dict]:
        """List all projects, optionally filtered by status"""
        projects = []
        project_dir = self.data_dir / "projects"

        for file_path in project_dir.glob("*.json"):
            with open(file_path, 'r') as f:
                project = json.load(f)
                if status is None or project.get('status') == status:
                    projects.append(project)

        # Sort by creation date, newest first
        projects.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return projects

    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        file_path = self.data_dir / "projects" / f"{project_id}.json"

        if file_path.exists():
            file_path.unlink()
            return True

        return False

    # Document Management
    def save_document(self, project_id: str, document_data: Dict) -> str:
        """Save a document for a project"""
        doc_id = f"DOC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        document_data['id'] = doc_id
        document_data['project_id'] = project_id
        document_data['uploaded_at'] = datetime.now().isoformat()

        file_path = self.data_dir / "documents" / f"{doc_id}.json"
        with open(file_path, 'w') as f:
            json.dump(document_data, f, indent=2)

        return doc_id

    def get_project_documents(self, project_id: str) -> List[Dict]:
        """Get all documents for a project"""
        documents = []
        doc_dir = self.data_dir / "documents"

        for file_path in doc_dir.glob("*.json"):
            with open(file_path, 'r') as f:
                doc = json.load(f)
                if doc.get('project_id') == project_id:
                    documents.append(doc)

        return documents

    # Analysis Management
    def save_analysis(self, project_id: str, analysis_data: Dict) -> str:
        """Save RFP analysis results"""
        analysis_id = f"ANL-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        analysis_data['id'] = analysis_id
        analysis_data['project_id'] = project_id
        analysis_data['created_at'] = datetime.now().isoformat()

        file_path = self.data_dir / "analyses" / f"{analysis_id}.json"
        with open(file_path, 'w') as f:
            json.dump(analysis_data, f, indent=2)

        return analysis_id

    def get_analysis(self, project_id: str) -> Optional[Dict]:
        """Get latest analysis for a project"""
        analyses = []
        analysis_dir = self.data_dir / "analyses"

        for file_path in analysis_dir.glob("*.json"):
            with open(file_path, 'r') as f:
                analysis = json.load(f)
                if analysis.get('project_id') == project_id:
                    analyses.append(analysis)

        if analyses:
            # Return most recent
            analyses.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return analyses[0]

        return None

    # Bid Management
    def save_bid(self, project_id: str, bid_data: Dict) -> str:
        """Save generated bid"""
        bid_id = f"BID-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        bid_data['id'] = bid_id
        bid_data['project_id'] = project_id
        bid_data['created_at'] = datetime.now().isoformat()

        file_path = self.data_dir / "bids" / f"{bid_id}.json"
        with open(file_path, 'w') as f:
            json.dump(bid_data, f, indent=2)

        return bid_id

    def get_bid(self, project_id: str) -> Optional[Dict]:
        """Get latest bid for a project"""
        bids = []
        bid_dir = self.data_dir / "bids"

        for file_path in bid_dir.glob("*.json"):
            with open(file_path, 'r') as f:
                bid = json.load(f)
                if bid.get('project_id') == project_id:
                    bids.append(bid)

        if bids:
            # Return most recent
            bids.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return bids[0]

        return None

    # Conflict Detection
    def save_conflicts(self, project_id: str, conflicts: List[Dict]) -> str:
        """Save detected conflicts"""
        conflict_id = f"CNF-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        conflict_data = {
            'id': conflict_id,
            'project_id': project_id,
            'conflicts': conflicts,
            'created_at': datetime.now().isoformat()
        }

        file_path = self.data_dir / "conflicts" / f"{conflict_id}.json"
        with open(file_path, 'w') as f:
            json.dump(conflict_data, f, indent=2)

        return conflict_id

    def get_conflicts(self, project_id: str) -> List[Dict]:
        """Get conflicts for a project"""
        conflict_dir = self.data_dir / "conflicts"

        for file_path in conflict_dir.glob("*.json"):
            with open(file_path, 'r') as f:
                data = json.load(f)
                if data.get('project_id') == project_id:
                    return data.get('conflicts', [])

        return []

    # Win Probability
    def save_prediction(self, project_id: str, prediction_data: Dict) -> str:
        """Save win probability prediction"""
        pred_id = f"PRED-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        prediction_data['id'] = pred_id
        prediction_data['project_id'] = project_id
        prediction_data['created_at'] = datetime.now().isoformat()

        file_path = self.data_dir / "predictions" / f"{pred_id}.json"
        with open(file_path, 'w') as f:
            json.dump(prediction_data, f, indent=2)

        return pred_id

    def get_prediction(self, project_id: str) -> Optional[Dict]:
        """Get latest prediction for a project"""
        predictions = []
        pred_dir = self.data_dir / "predictions"

        for file_path in pred_dir.glob("*.json"):
            with open(file_path, 'r') as f:
                pred = json.load(f)
                if pred.get('project_id') == project_id:
                    predictions.append(pred)

        if predictions:
            # Return most recent
            predictions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return predictions[0]

        return None

    # Statistics and Reporting
    def get_dashboard_stats(self) -> Dict:
        """Get statistics for dashboard"""
        projects = self.list_projects()

        active_count = len([p for p in projects if p.get('status') == 'Active'])
        submitted_count = len([p for p in projects if p.get('status') == 'Submitted'])
        won_count = len([p for p in projects if p.get('status') == 'Closed-Won'])
        lost_count = len([p for p in projects if p.get('status') == 'Closed-Lost'])

        total_completed = won_count + lost_count
        win_rate = (won_count / total_completed * 100) if total_completed > 0 else 0

        return {
            'active_projects': active_count,
            'submitted_projects': submitted_count,
            'won_projects': won_count,
            'lost_projects': lost_count,
            'win_rate': round(win_rate, 1),
            'total_projects': len(projects)
        }


# Global database instance
db = Database()
