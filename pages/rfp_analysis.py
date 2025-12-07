"""
RFP Analysis - AI-powered RFP document analysis and risk assessment
"""

import streamlit as st
from utils.theme import create_section_header, get_risk_color
import plotly.graph_objects as go


def render():
    """Render the RFP analysis page"""

    st.markdown(create_section_header(
        "RFP Analysis & Risk Assessment",
        "AI-powered analysis of RFQ documents with risk scoring and recommendations"
    ), unsafe_allow_html=True)

    # Project selector
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        selected_project = st.selectbox(
            "Select Project",
            [
                "Dubai Marina Tower Complex (PRJ-001)",
                "Abu Dhabi Highway Extension (PRJ-002)",
                "Qatar Sports Stadium (PRJ-004)"
            ],
            key="analysis_project"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🤖 Run Analysis", use_container_width=True, type="primary"):
            run_analysis()

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📥 Export Report", use_container_width=True):
            st.info("Report export feature coming soon!")

    st.markdown("<br>", unsafe_allow_html=True)

    # Analysis results
    render_analysis_results()


def run_analysis():
    """Simulate running AI analysis"""
    with st.spinner("🤖 AI is analyzing the RFP documents..."):
        import time
        progress_bar = st.progress(0)
        status_text = st.empty()

        steps = [
            "Loading documents...",
            "Extracting text content...",
            "Analyzing requirements...",
            "Assessing risks...",
            "Generating recommendations...",
            "Finalizing report..."
        ]

        for i, step in enumerate(steps):
            status_text.text(step)
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.5)

        status_text.empty()
        progress_bar.empty()

    st.success("✅ Analysis complete!")
    st.balloons()


def render_analysis_results():
    """Render the analysis results"""

    # Overall Risk Assessment
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(13, 115, 119, 0.1) 100%);
                    border: 1px solid rgba(184, 153, 90, 0.3);
                    border-radius: 16px;
                    padding: 2rem;
                    margin-bottom: 2rem;'>
            <h3 style='color: #b8995a; margin: 0 0 1.5rem 0;'>
                🎯 Overall Risk Assessment
            </h3>
            <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 2rem;'>
                <div style='text-align: center;'>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>
                        OVERALL RISK LEVEL
                    </div>
                    <div style='color: #4ade80; font-size: 3rem; font-weight: 800; font-family: "Syne", sans-serif;'>
                        LOW
                    </div>
                    <div style='color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-top: 0.5rem;'>
                        ✓ Recommended to proceed with bid
                    </div>
                </div>
                <div style='text-align: center;'>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-bottom: 0.5rem;'>
                        WIN PROBABILITY
                    </div>
                    <div style='color: #b8995a; font-size: 3rem; font-weight: 800; font-family: "Syne", sans-serif;'>
                        72%
                    </div>
                    <div style='color: rgba(255,255,255,0.6); font-size: 0.85rem; margin-top: 0.5rem;'>
                        ↗ Strong likelihood of success
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Score cards
    col1, col2, col3, col4 = st.columns(4)

    scores = [
        {"label": "Quality Score", "value": 87, "icon": "⭐", "color": "#4ade80"},
        {"label": "Clarity Score", "value": 92, "icon": "📝", "color": "#4ade80"},
        {"label": "Doability Score", "value": 78, "icon": "🔧", "color": "#fbbf24"},
        {"label": "Vendor Risk", "value": 15, "icon": "⚠️", "color": "#4ade80"}
    ]

    for i, score_data in enumerate(scores):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(13, 115, 119, 0.05) 100%);
                            border: 1px solid rgba(184, 153, 90, 0.2);
                            border-radius: 12px;
                            padding: 1.5rem;
                            text-align: center;'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>{score_data['icon']}</div>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.75rem; text-transform: uppercase;
                                letter-spacing: 1px; margin-bottom: 0.5rem;'>
                        {score_data['label']}
                    </div>
                    <div style='color: {score_data['color']}; font-size: 2.5rem; font-weight: 800;
                                font-family: "Syne", sans-serif;'>
                        {score_data['value']}
                    </div>
                    <div style='background: rgba(184, 153, 90, 0.2); height: 4px; border-radius: 2px;
                                margin-top: 1rem; overflow: hidden;'>
                        <div style='background: {score_data['color']}; height: 100%; width: {score_data['value']}%;'></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs for detailed analysis
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Key Findings",
        "🚩 Red Flags & Opportunities",
        "📊 Recommendations",
        "📄 Missing Documents"
    ])

    with tab1:
        render_key_findings()

    with tab2:
        render_red_flags()

    with tab3:
        render_recommendations()

    with tab4:
        render_missing_documents()


def render_key_findings():
    """Render key findings section"""

    findings = [
        {
            'category': 'Project Scope',
            'status': 'positive',
            'title': 'Well-Defined Requirements',
            'description': 'The RFP provides clear, detailed technical specifications and scope of work. All major deliverables are explicitly outlined with acceptance criteria.'
        },
        {
            'category': 'Timeline',
            'status': 'positive',
            'title': 'Realistic Schedule',
            'description': 'The proposed timeline aligns well with industry standards for a project of this size and complexity. Sufficient buffer time is included.'
        },
        {
            'category': 'Budget',
            'status': 'warning',
            'title': 'Budget Constraints Noted',
            'description': 'Budget appears tight for the scope. Recommend value engineering opportunities to optimize costs while maintaining quality.'
        },
        {
            'category': 'Client',
            'status': 'positive',
            'title': 'Established Relationship',
            'description': 'Previous successful projects with this client. Payment history is excellent with average payment cycle of 28 days.'
        }
    ]

    for finding in findings:
        status_config = {
            'positive': {'color': '#4ade80', 'icon': '✅'},
            'warning': {'color': '#fbbf24', 'icon': '⚠️'},
            'negative': {'color': '#f87171', 'icon': '❌'}
        }
        config = status_config[finding['status']]

        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(13, 115, 119, 0.05) 100%);
                        border-left: 4px solid {config['color']};
                        border-radius: 12px;
                        padding: 1.5rem;
                        margin-bottom: 1rem;
                        border: 1px solid rgba(184, 153, 90, 0.15);'>
                <div style='display: flex; align-items: start; gap: 1rem;'>
                    <div style='font-size: 1.5rem;'>{config['icon']}</div>
                    <div style='flex: 1;'>
                        <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;'>
                            <div style='color: #b8995a; font-weight: 700; font-size: 1rem;'>
                                {finding['title']}
                            </div>
                            <div style='background: rgba(184, 153, 90, 0.2); color: #b8995a;
                                        padding: 0.25rem 0.75rem; border-radius: 6px; font-size: 0.75rem;
                                        font-weight: 600;'>
                                {finding['category']}
                            </div>
                        </div>
                        <div style='color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 1.6;'>
                            {finding['description']}
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_red_flags():
    """Render red flags and opportunities"""

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <h4 style='color: #f87171; margin-bottom: 1rem;'>🚩 Red Flags</h4>
        """, unsafe_allow_html=True)

        red_flags = [
            {
                'severity': 'Medium',
                'title': 'Aggressive Payment Terms',
                'description': 'Net-60 payment terms requested, longer than standard industry practice.'
            },
            {
                'severity': 'Low',
                'title': 'Limited Site Access',
                'description': 'Site access restricted to business hours only, may impact construction schedule.'
            }
        ]

        for flag in red_flags:
            severity_color = '#fbbf24' if flag['severity'] == 'Medium' else '#4ade80'

            st.markdown(f"""
                <div style='background: rgba(248, 113, 113, 0.1); border: 1px solid rgba(248, 113, 113, 0.3);
                            border-radius: 10px; padding: 1rem; margin-bottom: 1rem;'>
                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;'>
                        <div style='color: #f87171; font-weight: 700;'>{flag['title']}</div>
                        <div style='background: {severity_color}; color: #1a1a1a;
                                    padding: 0.2rem 0.6rem; border-radius: 4px;
                                    font-size: 0.75rem; font-weight: 700;'>
                            {flag['severity']}
                        </div>
                    </div>
                    <div style='color: rgba(255,255,255,0.8); font-size: 0.85rem;'>
                        {flag['description']}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <h4 style='color: #4ade80; margin-bottom: 1rem;'>💎 Opportunities</h4>
        """, unsafe_allow_html=True)

        opportunities = [
            {
                'impact': 'High',
                'title': 'Value Engineering Potential',
                'description': 'Multiple areas identified for cost optimization without compromising quality standards.'
            },
            {
                'impact': 'High',
                'title': 'Long-term Partnership',
                'description': 'Client indicated interest in ongoing relationship for future phases of development.'
            },
            {
                'impact': 'Medium',
                'title': 'Technology Differentiation',
                'description': 'Our BIM and project management capabilities align perfectly with client\'s digital transformation goals.'
            }
        ]

        for opp in opportunities:
            impact_color = '#4ade80' if opp['impact'] == 'High' else '#0d7377'

            st.markdown(f"""
                <div style='background: rgba(74, 222, 128, 0.1); border: 1px solid rgba(74, 222, 128, 0.3);
                            border-radius: 10px; padding: 1rem; margin-bottom: 1rem;'>
                    <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;'>
                        <div style='color: #4ade80; font-weight: 700;'>{opp['title']}</div>
                        <div style='background: {impact_color}; color: #1a1a1a;
                                    padding: 0.2rem 0.6rem; border-radius: 4px;
                                    font-size: 0.75rem; font-weight: 700;'>
                            {opp['impact']}
                        </div>
                    </div>
                    <div style='color: rgba(255,255,255,0.8); font-size: 0.85rem;'>
                        {opp['description']}
                    </div>
                </div>
            """, unsafe_allow_html=True)


def render_recommendations():
    """Render AI recommendations"""

    recommendations = [
        {
            'priority': 'High',
            'action': 'Address Payment Terms',
            'description': 'Negotiate payment terms to Net-45 or request progress payments to align with cash flow requirements.',
            'estimated_time': '2-3 days',
            'owner': 'Contract Manager'
        },
        {
            'priority': 'High',
            'action': 'Submit Value Engineering Proposals',
            'description': 'Prepare alternative solutions for HVAC and electrical systems that maintain performance while reducing costs by 15-20%.',
            'estimated_time': '5-7 days',
            'owner': 'Engineering Team'
        },
        {
            'priority': 'Medium',
            'action': 'Schedule Site Visit',
            'description': 'Conduct detailed site inspection to verify access constraints and develop optimized logistics plan.',
            'estimated_time': '1 day',
            'owner': 'Project Manager'
        },
        {
            'priority': 'Medium',
            'action': 'Prepare Digital Proposal',
            'description': 'Showcase BIM capabilities and digital project management platform as key differentiators.',
            'estimated_time': '3-4 days',
            'owner': 'Technical Team'
        },
        {
            'priority': 'Low',
            'action': 'Reference Check',
            'description': 'Contact previous contractors who worked with this client to validate payment history and working relationship.',
            'estimated_time': '1-2 days',
            'owner': 'Business Development'
        }
    ]

    for rec in recommendations:
        priority_config = {
            'High': {'color': '#f87171', 'bg': 'rgba(248, 113, 113, 0.2)'},
            'Medium': {'color': '#fbbf24', 'bg': 'rgba(251, 191, 36, 0.2)'},
            'Low': {'color': '#4ade80', 'bg': 'rgba(74, 222, 128, 0.2)'}
        }
        config = priority_config[rec['priority']]

        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(13, 115, 119, 0.05) 100%);
                        border: 1px solid rgba(184, 153, 90, 0.2);
                        border-left: 4px solid {config['color']};
                        border-radius: 12px;
                        padding: 1.5rem;
                        margin-bottom: 1rem;'>
                <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;'>
                    <div>
                        <div style='color: #b8995a; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;'>
                            {rec['action']}
                        </div>
                        <div style='color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 1.6;'>
                            {rec['description']}
                        </div>
                    </div>
                    <div style='background: {config['bg']}; color: {config['color']};
                                padding: 0.4rem 0.8rem; border-radius: 6px;
                                font-size: 0.8rem; font-weight: 700; white-space: nowrap;'>
                        {rec['priority']} Priority
                    </div>
                </div>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;
                            padding-top: 1rem; border-top: 1px solid rgba(184, 153, 90, 0.2);'>
                    <div>
                        <span style='color: rgba(255,255,255,0.6); font-size: 0.8rem;'>⏱️ Est. Time:</span>
                        <span style='color: #ffffff; font-weight: 600; margin-left: 0.5rem;'>{rec['estimated_time']}</span>
                    </div>
                    <div>
                        <span style='color: rgba(255,255,255,0.6); font-size: 0.8rem;'>👤 Owner:</span>
                        <span style='color: #ffffff; font-weight: 600; margin-left: 0.5rem;'>{rec['owner']}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_missing_documents():
    """Render missing documents section with WhatsApp integration"""

    st.markdown("""
        <div style='background: rgba(251, 191, 36, 0.1); border: 1px solid rgba(251, 191, 36, 0.3);
                    border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem;'>
            <h4 style='color: #fbbf24; margin: 0 0 0.5rem 0;'>⚠️ Missing Documents Detected</h4>
            <p style='color: rgba(255,255,255,0.8); margin: 0;'>
                The following documents are typically required but were not found in the uploaded files.
                You can request them from the vendor using WhatsApp or Email.
            </p>
        </div>
    """, unsafe_allow_html=True)

    missing_docs = [
        {
            'name': 'Site Survey Report',
            'importance': 'High',
            'description': 'Detailed topographical and geotechnical survey of the construction site'
        },
        {
            'name': 'Environmental Impact Assessment',
            'importance': 'High',
            'description': 'Environmental compliance and impact analysis documentation'
        },
        {
            'name': 'Utility Connection Details',
            'importance': 'Medium',
            'description': 'Specifications for water, electricity, and other utility connections'
        },
        {
            'name': 'Insurance Requirements',
            'importance': 'Medium',
            'description': 'Required insurance coverage and bonding details'
        }
    ]

    for doc in missing_docs:
        importance_color = '#f87171' if doc['importance'] == 'High' else '#fbbf24'

        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(251, 191, 36, 0.05) 100%);
                        border: 1px solid rgba(184, 153, 90, 0.2);
                        border-radius: 12px;
                        padding: 1.5rem;
                        margin-bottom: 1rem;'>
                <div style='display: flex; justify-content: space-between; align-items: start;'>
                    <div style='flex: 1;'>
                        <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;'>
                            <div style='color: #b8995a; font-weight: 700; font-size: 1rem;'>
                                📄 {doc['name']}
                            </div>
                            <div style='background: {importance_color}; color: #1a1a1a;
                                        padding: 0.25rem 0.6rem; border-radius: 6px;
                                        font-size: 0.75rem; font-weight: 700;'>
                                {doc['importance']}
                            </div>
                        </div>
                        <div style='color: rgba(255,255,255,0.7); font-size: 0.85rem; margin-bottom: 1rem;'>
                            {doc['description']}
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"📱 Request via WhatsApp", key=f"wa_{doc['name']}", use_container_width=True):
                show_whatsapp_message(doc['name'])
        with col2:
            if st.button(f"📧 Request via Email", key=f"email_{doc['name']}", use_container_width=True):
                show_email_template(doc['name'])


def show_whatsapp_message(doc_name):
    """Show WhatsApp message preview"""
    st.info(f"""
    📱 **WhatsApp Message Preview**

    Hello! We're reviewing the RFP for the Dubai Marina Tower Complex project.

    Could you please provide the **{doc_name}**? This document is required to complete our technical assessment and proposal.

    Thank you for your assistance!

    Best regards,
    BidForge AI Team
    """)


def show_email_template(doc_name):
    """Show email template"""
    st.info(f"""
    📧 **Email Template**

    Subject: Request for {doc_name} - Dubai Marina Tower Complex

    Dear Sir/Madam,

    We are currently preparing our bid proposal for the Dubai Marina Tower Complex project.

    We kindly request the **{doc_name}** to ensure our proposal addresses all technical requirements comprehensively.

    Please send the document at your earliest convenience.

    Best regards,
    [Your Name]
    BidForge AI
    """)
