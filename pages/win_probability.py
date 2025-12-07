"""
Win Probability - ML-based prediction of bid win probability
"""

import streamlit as st
from utils.theme import create_section_header
import plotly.graph_objects as go


def render():
    """Render the win probability page"""

    st.markdown(create_section_header(
        "Win Probability Analysis",
        "Machine learning-powered prediction of bid success probability"
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
            key="winprob_project"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎯 Calculate Probability", use_container_width=True, type="primary"):
            calculate_probability()

    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📊 View History", use_container_width=True):
            st.info("Historical predictions feature coming soon!")

    st.markdown("<br>", unsafe_allow_html=True)

    # Main probability display
    render_probability_gauge()

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature breakdown
    render_feature_scores()

    st.markdown("<br>", unsafe_allow_html=True)

    # Risk and strength factors
    col1, col2 = st.columns(2)

    with col1:
        render_risk_factors()

    with col2:
        render_strength_factors()

    st.markdown("<br>", unsafe_allow_html=True)

    # Recommendations
    render_recommendations()


def calculate_probability():
    """Simulate probability calculation"""
    with st.spinner("🎯 Analyzing project factors and calculating win probability..."):
        import time
        progress_bar = st.progress(0)
        status_text = st.empty()

        steps = [
            "Extracting project features...",
            "Analyzing client relationship...",
            "Assessing competitiveness...",
            "Evaluating team capacity...",
            "Checking timeline feasibility...",
            "Calculating probability...",
            "Generating recommendations..."
        ]

        for i, step in enumerate(steps):
            status_text.text(step)
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.4)

        status_text.empty()
        progress_bar.empty()

    st.success("✅ Win probability calculated!")
    st.balloons()


def render_probability_gauge():
    """Render the main probability gauge"""

    win_probability = 72

    # Gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=win_probability,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Win Probability", 'font': {'size': 24, 'color': '#b8995a'}},
        delta={'reference': 65, 'increasing': {'color': "#4ade80"}},
        number={'suffix': "%", 'font': {'size': 60, 'color': '#ffffff'}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#b8995a"},
            'bar': {'color': "#0d7377"},
            'bgcolor': "rgba(26, 26, 26, 0.6)",
            'borderwidth': 2,
            'bordercolor': "#b8995a",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(248, 113, 113, 0.3)'},
                {'range': [30, 60], 'color': 'rgba(251, 191, 36, 0.3)'},
                {'range': [60, 100], 'color': 'rgba(74, 222, 128, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "#b8995a", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#e0e0e0", 'family': "Inter"},
        height=350,
        margin=dict(l=20, r=20, t=80, b=20)
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Probability interpretation
    if win_probability >= 70:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(74, 222, 128, 0.2) 0%, rgba(26, 26, 26, 0.9) 100%);
                        border: 1px solid rgba(74, 222, 128, 0.4);
                        border-radius: 12px;
                        padding: 1.5rem;
                        text-align: center;'>
                <div style='color: #4ade80; font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;'>
                    ✅ Strong Likelihood of Success
                </div>
                <div style='color: rgba(255,255,255,0.8); font-size: 0.95rem;'>
                    Project characteristics align well with your strengths and past successes.
                    Recommend proceeding with bid preparation.
                </div>
            </div>
        """, unsafe_allow_html=True)
    elif win_probability >= 50:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(251, 191, 36, 0.2) 0%, rgba(26, 26, 26, 0.9) 100%);
                        border: 1px solid rgba(251, 191, 36, 0.4);
                        border-radius: 12px;
                        padding: 1.5rem;
                        text-align: center;'>
                <div style='color: #fbbf24; font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;'>
                    ⚠️ Moderate Win Probability
                </div>
                <div style='color: rgba(255,255,255,0.8); font-size: 0.95rem;'>
                    Consider addressing identified risk factors before submitting.
                    Review recommendations to improve your competitive position.
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(248, 113, 113, 0.2) 0%, rgba(26, 26, 26, 0.9) 100%);
                        border: 1px solid rgba(248, 113, 113, 0.4);
                        border-radius: 12px;
                        padding: 1.5rem;
                        text-align: center;'>
                <div style='color: #f87171; font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;'>
                    ❌ Low Win Probability
                </div>
                <div style='color: rgba(255,255,255,0.8); font-size: 0.95rem;'>
                    Significant risk factors detected. Carefully evaluate whether to proceed with this bid.
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_feature_scores():
    """Render individual feature scores"""

    st.markdown(create_section_header("📊 Feature Analysis"), unsafe_allow_html=True)

    features = [
        {'name': 'Project Type Alignment', 'score': 85, 'description': 'Strong match with company expertise'},
        {'name': 'Client Relationship', 'score': 92, 'description': 'Excellent history with this client'},
        {'name': 'Competitive Position', 'score': 68, 'description': 'Moderate competition expected'},
        {'name': 'Team Capacity', 'score': 75, 'description': 'Adequate resources available'},
        {'name': 'Timeline Feasibility', 'score': 80, 'description': 'Realistic schedule expectations'},
        {'name': 'Project Complexity', 'score': 70, 'description': 'Well within capabilities'},
        {'name': 'Requirements Clarity', 'score': 88, 'description': 'Well-defined scope'},
        {'name': 'Budget Alignment', 'score': 65, 'description': 'Tight but achievable budget'}
    ]

    for feature in features:
        # Determine color based on score
        if feature['score'] >= 80:
            color = '#4ade80'
            bg_color = 'rgba(74, 222, 128, 0.1)'
        elif feature['score'] >= 60:
            color = '#fbbf24'
            bg_color = 'rgba(251, 191, 36, 0.1)'
        else:
            color = '#f87171'
            bg_color = 'rgba(248, 113, 113, 0.1)'

        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, {bg_color} 100%);
                        border: 1px solid rgba(184, 153, 90, 0.2);
                        border-radius: 10px;
                        padding: 1rem;
                        margin-bottom: 0.75rem;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;'>
                    <div>
                        <div style='color: #ffffff; font-weight: 600; font-size: 0.95rem;'>
                            {feature['name']}
                        </div>
                        <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-top: 0.25rem;'>
                            {feature['description']}
                        </div>
                    </div>
                    <div style='color: {color}; font-size: 1.5rem; font-weight: 800;'>
                        {feature['score']}
                    </div>
                </div>
                <div style='background: rgba(184, 153, 90, 0.2); height: 6px; border-radius: 3px; overflow: hidden;'>
                    <div style='background: {color}; height: 100%; width: {feature['score']}%;
                                transition: width 1s ease;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_risk_factors():
    """Render risk factors"""

    st.markdown("""
        <h4 style='color: #f87171; margin-bottom: 1rem;'>⚠️ Risk Factors</h4>
    """, unsafe_allow_html=True)

    risk_factors = [
        {
            'factor': 'High Competition',
            'impact': 'Medium',
            'description': '3-4 strong competitors expected to bid on this project'
        },
        {
            'factor': 'Budget Constraints',
            'impact': 'Medium',
            'description': 'Client budget appears tight for scope, may limit profit margins'
        },
        {
            'factor': 'Resource Allocation',
            'impact': 'Low',
            'description': 'Potential overlap with ongoing projects in Q1 2025'
        }
    ]

    for risk in risk_factors:
        impact_color = '#f87171' if risk['impact'] == 'High' else '#fbbf24' if risk['impact'] == 'Medium' else '#4ade80'

        st.markdown(f"""
            <div style='background: rgba(248, 113, 113, 0.1); border: 1px solid rgba(248, 113, 113, 0.3);
                        border-radius: 10px; padding: 1rem; margin-bottom: 1rem;'>
                <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;'>
                    <div style='color: #f87171; font-weight: 700;'>{risk['factor']}</div>
                    <div style='background: {impact_color}; color: #1a1a1a;
                                padding: 0.2rem 0.6rem; border-radius: 4px;
                                font-size: 0.75rem; font-weight: 700;'>
                        {risk['impact']}
                    </div>
                </div>
                <div style='color: rgba(255,255,255,0.8); font-size: 0.85rem;'>
                    {risk['description']}
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_strength_factors():
    """Render strength factors"""

    st.markdown("""
        <h4 style='color: #4ade80; margin-bottom: 1rem;'>💪 Strength Factors</h4>
    """, unsafe_allow_html=True)

    strengths = [
        {
            'factor': 'Established Client Relationship',
            'impact': 'High',
            'description': '3 successful projects completed for this client with 100% satisfaction'
        },
        {
            'factor': 'Technical Expertise',
            'impact': 'High',
            'description': 'Specialized experience in high-rise construction with proven methodologies'
        },
        {
            'factor': 'Regional Presence',
            'impact': 'Medium',
            'description': 'Local office and established supply chain in Dubai market'
        },
        {
            'factor': 'Safety Record',
            'impact': 'Medium',
            'description': 'Outstanding safety performance with zero LTI in past 2 years'
        }
    ]

    for strength in strengths:
        impact_color = '#4ade80' if strength['impact'] == 'High' else '#0d7377'

        st.markdown(f"""
            <div style='background: rgba(74, 222, 128, 0.1); border: 1px solid rgba(74, 222, 128, 0.3);
                        border-radius: 10px; padding: 1rem; margin-bottom: 1rem;'>
                <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;'>
                    <div style='color: #4ade80; font-weight: 700;'>{strength['factor']}</div>
                    <div style='background: {impact_color}; color: #1a1a1a;
                                padding: 0.2rem 0.6rem; border-radius: 4px;
                                font-size: 0.75rem; font-weight: 700;'>
                        {strength['impact']}
                    </div>
                </div>
                <div style='color: rgba(255,255,255,0.8); font-size: 0.85rem;'>
                    {strength['description']}
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_recommendations():
    """Render AI recommendations to improve win probability"""

    st.markdown(create_section_header("💡 Recommendations to Improve Win Probability"), unsafe_allow_html=True)

    recommendations = [
        {
            'title': 'Emphasize Past Success Stories',
            'impact': '+8%',
            'description': 'Highlight the 3 successful projects completed for this client, particularly the similar tower project in 2023',
            'priority': 'High'
        },
        {
            'title': 'Offer Value Engineering Options',
            'impact': '+6%',
            'description': 'Present 2-3 alternative approaches that can reduce costs by 10-15% without compromising quality',
            'priority': 'High'
        },
        {
            'title': 'Strengthen Safety Narrative',
            'impact': '+4%',
            'description': 'Showcase zero-accident record and advanced safety protocols as competitive differentiator',
            'priority': 'Medium'
        },
        {
            'title': 'Propose Accelerated Timeline',
            'impact': '+5%',
            'description': 'Demonstrate ability to complete 2-3 weeks ahead of requested schedule using advanced methodologies',
            'priority': 'Medium'
        }
    ]

    for rec in recommendations:
        priority_color = '#f87171' if rec['priority'] == 'High' else '#fbbf24'

        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(13, 115, 119, 0.05) 100%);
                        border: 1px solid rgba(184, 153, 90, 0.2);
                        border-radius: 12px;
                        padding: 1.5rem;
                        margin-bottom: 1rem;'>
                <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.75rem;'>
                    <div>
                        <div style='color: #b8995a; font-weight: 700; font-size: 1.05rem;'>
                            {rec['title']}
                        </div>
                    </div>
                    <div style='display: flex; gap: 0.5rem; align-items: center;'>
                        <span style='background: rgba(74, 222, 128, 0.2); color: #4ade80;
                                     padding: 0.3rem 0.7rem; border-radius: 6px;
                                     font-size: 0.85rem; font-weight: 700;'>
                            {rec['impact']}
                        </span>
                        <span style='background: rgba(248, 113, 113, 0.2); color: {priority_color};
                                     padding: 0.3rem 0.7rem; border-radius: 6px;
                                     font-size: 0.75rem; font-weight: 700;'>
                            {rec['priority']}
                        </span>
                    </div>
                </div>
                <div style='color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 1.6;'>
                    {rec['description']}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Projected impact
    st.markdown("""
        <div style='background: linear-gradient(135deg, #0d7377 0%, #0a5a5d 100%);
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                    margin-top: 2rem;'>
            <div style='color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-bottom: 0.5rem;'>
                Projected Win Probability with Recommendations
            </div>
            <div style='color: #b8995a; font-size: 3rem; font-weight: 800; font-family: "Syne", sans-serif;'>
                85%
            </div>
            <div style='color: #4ade80; font-size: 1rem; font-weight: 600; margin-top: 0.5rem;'>
                ↗ +13% improvement potential
            </div>
        </div>
    """, unsafe_allow_html=True)
