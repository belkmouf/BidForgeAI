"""
Dashboard page - Main overview and analytics
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from utils.theme import create_section_header, create_stat_badge


def render():
    """Render the dashboard page"""

    # Page header
    st.markdown(create_section_header(
        "Dashboard",
        "Real-time insights into your bidding pipeline and performance metrics"
    ), unsafe_allow_html=True)

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(13, 115, 119, 0.2) 0%, rgba(26, 26, 26, 0.9) 100%);
                        padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(184, 153, 90, 0.3);
                        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);'>
                <div style='color: rgba(255,255,255,0.7); font-size: 0.75rem; text-transform: uppercase;
                            letter-spacing: 1px; margin-bottom: 0.5rem; font-weight: 600;'>Active Projects</div>
                <div style='color: #b8995a; font-size: 2.5rem; font-weight: 800; font-family: "Syne", sans-serif;
                            margin-bottom: 0.5rem;'>24</div>
                <div style='color: #4ade80; font-size: 0.85rem; font-weight: 600;'>
                    ↗ +12% vs last month
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(184, 153, 90, 0.2) 0%, rgba(26, 26, 26, 0.9) 100%);
                        padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(13, 115, 119, 0.3);
                        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);'>
                <div style='color: rgba(255,255,255,0.7); font-size: 0.75rem; text-transform: uppercase;
                            letter-spacing: 1px; margin-bottom: 0.5rem; font-weight: 600;'>Win Rate</div>
                <div style='color: #b8995a; font-size: 2.5rem; font-weight: 800; font-family: "Syne", sans-serif;
                            margin-bottom: 0.5rem;'>68%</div>
                <div style='color: #4ade80; font-size: 0.85rem; font-weight: 600;'>
                    ↗ +5% vs last quarter
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(13, 115, 119, 0.2) 0%, rgba(26, 26, 26, 0.9) 100%);
                        padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(184, 153, 90, 0.3);
                        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);'>
                <div style='color: rgba(255,255,255,0.7); font-size: 0.75rem; text-transform: uppercase;
                            letter-spacing: 1px; margin-bottom: 0.5rem; font-weight: 600;'>Total Value</div>
                <div style='color: #b8995a; font-size: 2.5rem; font-weight: 800; font-family: "Syne", sans-serif;
                            margin-bottom: 0.5rem;'>$45.2M</div>
                <div style='color: #4ade80; font-size: 0.85rem; font-weight: 600;'>
                    ↗ +28% pipeline growth
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(184, 153, 90, 0.2) 0%, rgba(26, 26, 26, 0.9) 100%);
                        padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(13, 115, 119, 0.3);
                        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);'>
                <div style='color: rgba(255,255,255,0.7); font-size: 0.75rem; text-transform: uppercase;
                            letter-spacing: 1px; margin-bottom: 0.5rem; font-weight: 600;'>Avg Response Time</div>
                <div style='color: #b8995a; font-size: 2.5rem; font-weight: 800; font-family: "Syne", sans-serif;
                            margin-bottom: 0.5rem;'>2.4h</div>
                <div style='color: #4ade80; font-size: 0.85rem; font-weight: 600;'>
                    ↗ 85% faster with AI
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts row
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(13, 115, 119, 0.05) 100%);
                        border: 1px solid rgba(184, 153, 90, 0.2); border-radius: 16px;
                        padding: 1.5rem; margin-bottom: 1.5rem;'>
                <h3 style='color: #b8995a; margin: 0 0 1.5rem 0; font-size: 1.2rem;'>
                    📈 Pipeline Performance
                </h3>
            </div>
        """, unsafe_allow_html=True)

        # Create sample data for pipeline chart
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        won = [12, 15, 18, 22, 25, 28]
        lost = [8, 7, 5, 6, 4, 3]
        active = [15, 18, 20, 24, 26, 24]

        fig = go.Figure()
        fig.add_trace(go.Bar(name='Won', x=months, y=won, marker_color='#4ade80'))
        fig.add_trace(go.Bar(name='Lost', x=months, y=lost, marker_color='#f87171'))
        fig.add_trace(go.Bar(name='Active', x=months, y=active, marker_color='#0d7377'))

        fig.update_layout(
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0', family='Inter'),
            xaxis=dict(showgrid=False, color='#e0e0e0'),
            yaxis=dict(showgrid=True, gridcolor='rgba(184, 153, 90, 0.1)', color='#e0e0e0'),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                bgcolor='rgba(26, 26, 26, 0.8)',
                bordercolor='rgba(184, 153, 90, 0.3)',
                borderwidth=1
            ),
            height=350,
            margin=dict(l=10, r=10, t=40, b=10)
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(13, 115, 119, 0.05) 100%);
                        border: 1px solid rgba(184, 153, 90, 0.2); border-radius: 16px;
                        padding: 1.5rem; margin-bottom: 1.5rem;'>
                <h3 style='color: #b8995a; margin: 0 0 1.5rem 0; font-size: 1.2rem;'>
                    🎯 Project Status
                </h3>
            </div>
        """, unsafe_allow_html=True)

        # Pie chart for project status
        labels = ['Active', 'Submitted', 'Won', 'Lost']
        values = [24, 12, 35, 8]
        colors = ['#0d7377', '#b8995a', '#4ade80', '#f87171']

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker=dict(colors=colors, line=dict(color='#1a1a1a', width=2)),
            textfont=dict(size=14, color='#ffffff', family='Inter'),
            hovertemplate='<b>%{label}</b><br>%{value} projects<br>%{percent}<extra></extra>'
        )])

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0', family='Inter'),
            showlegend=True,
            legend=dict(
                orientation='v',
                yanchor='middle',
                y=0.5,
                xanchor='left',
                x=0.85,
                bgcolor='rgba(26, 26, 26, 0.8)',
                bordercolor='rgba(184, 153, 90, 0.3)',
                borderwidth=1
            ),
            height=350,
            margin=dict(l=10, r=10, t=10, b=10)
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Recent activity
    st.markdown(create_section_header(
        "Recent Activity",
        "Latest updates from your bidding pipeline"
    ), unsafe_allow_html=True)

    # Activity timeline
    activities = [
        {
            'icon': '✅',
            'title': 'Bid Submitted - Dubai Marina Tower Project',
            'time': '2 hours ago',
            'status': 'success',
            'value': '$12.5M'
        },
        {
            'icon': '🤖',
            'title': 'AI Analysis Complete - Abu Dhabi Highway Extension',
            'time': '5 hours ago',
            'status': 'info',
            'value': 'Risk: Low'
        },
        {
            'icon': '🎯',
            'title': 'Won Project - Sharjah Commercial Complex',
            'time': '1 day ago',
            'status': 'success',
            'value': '$8.3M'
        },
        {
            'icon': '📄',
            'title': 'New RFP Uploaded - Qatar Sports Stadium',
            'time': '2 days ago',
            'status': 'info',
            'value': '$25.7M'
        },
        {
            'icon': '⚠️',
            'title': 'Conflict Detected - Riyadh Infrastructure Project',
            'time': '3 days ago',
            'status': 'warning',
            'value': '3 issues'
        }
    ]

    for activity in activities:
        status_colors = {
            'success': '#4ade80',
            'info': '#0d7377',
            'warning': '#fbbf24',
            'error': '#f87171'
        }
        color = status_colors.get(activity['status'], '#e0e0e0')

        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(13, 115, 119, 0.05) 100%);
                        border-left: 4px solid {color};
                        border-radius: 12px;
                        padding: 1.25rem;
                        margin-bottom: 1rem;
                        transition: all 0.3s ease;
                        border: 1px solid rgba(184, 153, 90, 0.15);'>
                <div style='display: flex; align-items: center; justify-content: space-between;'>
                    <div style='display: flex; align-items: center; gap: 1rem;'>
                        <div style='font-size: 1.5rem;'>{activity['icon']}</div>
                        <div>
                            <div style='color: #ffffff; font-weight: 600; font-size: 0.95rem; margin-bottom: 0.3rem;'>
                                {activity['title']}
                            </div>
                            <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem;'>
                                {activity['time']}
                            </div>
                        </div>
                    </div>
                    <div style='background: linear-gradient(135deg, rgba(184, 153, 90, 0.2) 0%, rgba(13, 115, 119, 0.1) 100%);
                                padding: 0.5rem 1rem; border-radius: 8px;
                                border: 1px solid rgba(184, 153, 90, 0.3);'>
                        <span style='color: #b8995a; font-weight: 700; font-size: 0.9rem;'>
                            {activity['value']}
                        </span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Quick actions
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(create_section_header(
        "Quick Actions",
        "Get started with your next bid"
    ), unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📄 New Project", use_container_width=True, type="primary"):
            st.session_state.current_page = "Projects"
            st.rerun()

    with col2:
        if st.button("🤖 AI Analysis", use_container_width=True, type="primary"):
            st.session_state.current_page = "RFP Analysis"
            st.rerun()

    with col3:
        if st.button("✍️ Generate Bid", use_container_width=True, type="primary"):
            st.session_state.current_page = "Bid Generation"
            st.rerun()

    with col4:
        if st.button("📊 View Reports", use_container_width=True, type="secondary"):
            st.info("Reports feature coming soon!")
