"""
Conflict Detection - AI-powered detection of contradictory statements in bid documents
"""

import streamlit as st
from utils.theme import create_section_header
from utils.ai_services import ai_service
from utils.rag_service import get_rag_service
import pandas as pd


def render():
    """Render the conflict detection page"""

    st.markdown(create_section_header(
        "Document Conflict Detection",
        "AI-powered semantic and numeric conflict detection across all bid documents"
    ), unsafe_allow_html=True)

    # Project selector
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        selected_project = st.selectbox(
            "Select Project",
            [
                "Dubai Marina Tower Complex (PRJ-001)",
                "Abu Dhabi Highway Extension (PRJ-002)",
                "Riyadh Infrastructure Project (PRJ-005)"
            ],
            key="conflict_project"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 Run Detection", use_container_width=True, type="primary"):
            run_conflict_detection()

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📥 Export Report", use_container_width=True):
            st.success("✅ Report exported!")

    st.markdown("<br>", unsafe_allow_html=True)

    # Summary stats
    render_conflict_stats()

    st.markdown("<br>", unsafe_allow_html=True)

    # Detected conflicts
    render_conflicts()


def run_conflict_detection():
    """Simulate conflict detection"""
    with st.spinner("🔍 Analyzing documents for conflicts..."):
        import time
        progress_bar = st.progress(0)
        status_text = st.empty()

        steps = [
            "Loading documents...",
            "Extracting text content...",
            "Generating embeddings...",
            "Analyzing semantic similarity...",
            "Detecting numeric conflicts...",
            "Calculating severity scores...",
            "Generating report..."
        ]

        for i, step in enumerate(steps):
            status_text.text(step)
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.4)

        status_text.empty()
        progress_bar.empty()

    st.success("✅ Conflict detection complete!")


def render_conflict_stats():
    """Render conflict statistics"""

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(248, 113, 113, 0.2) 0%, rgba(26, 26, 26, 0.9) 100%);
                        padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(248, 113, 113, 0.3);'>
                <div style='color: rgba(255,255,255,0.7); font-size: 0.75rem; text-transform: uppercase;
                            letter-spacing: 1px; margin-bottom: 0.5rem;'>Critical Conflicts</div>
                <div style='color: #f87171; font-size: 2.5rem; font-weight: 800; font-family: "Syne", sans-serif;'>
                    2
                </div>
                <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-top: 0.5rem;'>
                    Require immediate action
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(251, 191, 36, 0.2) 0%, rgba(26, 26, 26, 0.9) 100%);
                        padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(251, 191, 36, 0.3);'>
                <div style='color: rgba(255,255,255,0.7); font-size: 0.75rem; text-transform: uppercase;
                            letter-spacing: 1px; margin-bottom: 0.5rem;'>High Priority</div>
                <div style='color: #fbbf24; font-size: 2.5rem; font-weight: 800; font-family: "Syne", sans-serif;'>
                    5
                </div>
                <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-top: 0.5rem;'>
                    Should be reviewed
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(13, 115, 119, 0.2) 0%, rgba(26, 26, 26, 0.9) 100%);
                        padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(13, 115, 119, 0.3);'>
                <div style='color: rgba(255,255,255,0.7); font-size: 0.75rem; text-transform: uppercase;
                            letter-spacing: 1px; margin-bottom: 0.5rem;'>Medium Priority</div>
                <div style='color: #0d7377; font-size: 2.5rem; font-weight: 800; font-family: "Syne", sans-serif;'>
                    8
                </div>
                <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-top: 0.5rem;'>
                    Monitor for changes
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(74, 222, 128, 0.2) 0%, rgba(26, 26, 26, 0.9) 100%);
                        padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(74, 222, 128, 0.3);'>
                <div style='color: rgba(255,255,255,0.7); font-size: 0.75rem; text-transform: uppercase;
                            letter-spacing: 1px; margin-bottom: 0.5rem;'>Resolved</div>
                <div style='color: #4ade80; font-size: 2.5rem; font-weight: 800; font-family: "Syne", sans-serif;'>
                    12
                </div>
                <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-top: 0.5rem;'>
                    Already addressed
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_conflicts():
    """Render detected conflicts"""

    st.markdown(create_section_header("🚨 Detected Conflicts"), unsafe_allow_html=True)

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        severity_filter = st.multiselect(
            "Severity",
            ["Critical", "High", "Medium", "Low"],
            default=["Critical", "High"],
            key="severity_filter"
        )

    with col2:
        status_filter = st.selectbox(
            "Status",
            ["All", "Unresolved", "Resolved", "In Review"],
            key="conflict_status"
        )

    with col3:
        type_filter = st.multiselect(
            "Conflict Type",
            ["Semantic", "Numeric", "Date", "Both"],
            default=["Semantic", "Numeric"],
            key="type_filter"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Sample conflicts
    conflicts = [
        {
            'id': 'CNF-001',
            'severity': 'Critical',
            'type': 'Numeric',
            'title': 'Contradictory Budget Values',
            'source': 'Budget_Breakdown.xlsx - Cell B12',
            'target': 'RFQ_Main_Document.pdf - Page 15',
            'source_text': 'Total project cost: $12,500,000',
            'target_text': 'Estimated budget allocation: $11,800,000',
            'confidence': 0.95,
            'status': 'Unresolved'
        },
        {
            'id': 'CNF-002',
            'severity': 'Critical',
            'type': 'Date',
            'title': 'Timeline Inconsistency',
            'source': 'Technical_Specifications.pdf - Section 3.2',
            'target': 'Client_Email.msg',
            'source_text': 'Project completion deadline: January 15, 2025',
            'target_text': 'We need the facility operational by December 31, 2024',
            'confidence': 0.98,
            'status': 'Unresolved'
        },
        {
            'id': 'CNF-003',
            'severity': 'High',
            'type': 'Semantic',
            'title': 'Conflicting Material Specifications',
            'source': 'Technical_Specifications.pdf - Page 8',
            'target': 'Technical_Specifications.pdf - Page 22',
            'source_text': 'All structural steel shall be Grade A572-50',
            'target_text': 'Structural members to use Grade A36 steel as per standard',
            'confidence': 0.88,
            'status': 'Unresolved'
        },
        {
            'id': 'CNF-004',
            'severity': 'High',
            'type': 'Numeric',
            'title': 'Floor Area Discrepancy',
            'source': 'RFQ_Main_Document.pdf - Page 3',
            'target': 'Site_Plans.pdf - Sheet A-1',
            'source_text': 'Total building area: 450,000 sq ft',
            'target_text': 'Calculated gross area: 428,500 sq ft',
            'confidence': 0.92,
            'status': 'In Review'
        },
        {
            'id': 'CNF-005',
            'severity': 'Medium',
            'type': 'Semantic',
            'title': 'Accessibility Requirements Variation',
            'source': 'Building_Codes.pdf - Section 5',
            'target': 'RFQ_Main_Document.pdf - Page 12',
            'source_text': 'Minimum 4 accessible parking spaces required',
            'target_text': 'Provide at least 6 ADA-compliant parking stalls',
            'confidence': 0.75,
            'status': 'Resolved'
        }
    ]

    for conflict in conflicts:
        severity_colors = {
            'Critical': '#dc2626',
            'High': '#f87171',
            'Medium': '#fbbf24',
            'Low': '#4ade80'
        }
        severity_color = severity_colors.get(conflict['severity'], '#e0e0e0')

        status_colors = {
            'Unresolved': '#f87171',
            'In Review': '#fbbf24',
            'Resolved': '#4ade80'
        }
        status_color = status_colors.get(conflict['status'], '#e0e0e0')

        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(13, 115, 119, 0.05) 100%);
                        border-left: 4px solid {severity_color};
                        border: 1px solid rgba(184, 153, 90, 0.2);
                        border-radius: 12px;
                        padding: 1.5rem;
                        margin-bottom: 1.5rem;'>

                <!-- Header -->
                <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;'>
                    <div>
                        <div style='color: #b8995a; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.3rem;'>
                            {conflict['id']}
                        </div>
                        <div style='color: #ffffff; font-size: 1.2rem; font-weight: 700;'>
                            {conflict['title']}
                        </div>
                    </div>
                    <div style='display: flex; gap: 0.5rem;'>
                        <span style='background: {severity_color}; color: white;
                                     padding: 0.4rem 0.8rem; border-radius: 6px;
                                     font-size: 0.8rem; font-weight: 700;'>
                            {conflict['severity']}
                        </span>
                        <span style='background: rgba(184, 153, 90, 0.3); color: #b8995a;
                                     padding: 0.4rem 0.8rem; border-radius: 6px;
                                     font-size: 0.8rem; font-weight: 600;'>
                            {conflict['type']}
                        </span>
                    </div>
                </div>

                <!-- Conflict Details -->
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin: 1.5rem 0;'>
                    <!-- Source -->
                    <div style='background: rgba(248, 113, 113, 0.1); padding: 1rem; border-radius: 8px;
                                border: 1px solid rgba(248, 113, 113, 0.3);'>
                        <div style='color: #f87171; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.5rem;'>
                            📍 SOURCE
                        </div>
                        <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-bottom: 0.5rem;'>
                            {conflict['source']}
                        </div>
                        <div style='color: #ffffff; font-size: 0.9rem; font-style: italic; line-height: 1.5;'>
                            "{conflict['source_text']}"
                        </div>
                    </div>

                    <!-- Target -->
                    <div style='background: rgba(251, 191, 36, 0.1); padding: 1rem; border-radius: 8px;
                                border: 1px solid rgba(251, 191, 36, 0.3);'>
                        <div style='color: #fbbf24; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.5rem;'>
                            🎯 TARGET
                        </div>
                        <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-bottom: 0.5rem;'>
                            {conflict['target']}
                        </div>
                        <div style='color: #ffffff; font-size: 0.9rem; font-style: italic; line-height: 1.5;'>
                            "{conflict['target_text']}"
                        </div>
                    </div>
                </div>

                <!-- Footer -->
                <div style='display: flex; justify-content: space-between; align-items: center;
                            padding-top: 1rem; border-top: 1px solid rgba(184, 153, 90, 0.2);'>
                    <div>
                        <span style='color: rgba(255,255,255,0.6); font-size: 0.8rem;'>
                            Confidence:
                        </span>
                        <span style='color: #b8995a; font-weight: 700; font-size: 0.9rem;'>
                            {int(conflict['confidence'] * 100)}%
                        </span>
                        <span style='margin-left: 2rem; color: rgba(255,255,255,0.6); font-size: 0.8rem;'>
                            Status:
                        </span>
                        <span style='color: {status_color}; font-weight: 700; font-size: 0.9rem;'>
                            {conflict['status']}
                        </span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Action buttons
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button(f"✅ Mark Resolved", key=f"resolve_{conflict['id']}", use_container_width=True):
                st.success(f"Conflict {conflict['id']} marked as resolved")

        with col2:
            if st.button(f"🔍 View Context", key=f"context_{conflict['id']}", use_container_width=True):
                st.info("Opening full document context...")

        with col3:
            if st.button(f"✏️ Add Note", key=f"note_{conflict['id']}", use_container_width=True):
                st.text_area(f"Note for {conflict['id']}", key=f"note_text_{conflict['id']}")

        with col4:
            if st.button(f"🚫 Dismiss", key=f"dismiss_{conflict['id']}", use_container_width=True):
                st.info(f"Conflict {conflict['id']} dismissed")

        st.markdown("<br>", unsafe_allow_html=True)
