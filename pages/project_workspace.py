"""
Project Workspace - Project management and document handling
"""

import streamlit as st
from datetime import datetime
from utils.theme import create_section_header, create_stat_badge, get_risk_color


def render():
    """Render the project workspace page"""

    # Page header
    st.markdown(create_section_header(
        "Project Workspace",
        "Manage your construction bid projects and documents"
    ), unsafe_allow_html=True)

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 All Projects", "➕ New Project", "📁 Project Details"])

    with tab1:
        render_project_list()

    with tab2:
        render_new_project()

    with tab3:
        render_project_details()


def render_project_list():
    """Render the list of all projects"""

    # Filters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "Active", "Submitted", "Closed-Won", "Closed-Lost"],
            key="status_filter"
        )

    with col2:
        sort_by = st.selectbox(
            "Sort By",
            ["Recent", "Value (High to Low)", "Value (Low to High)", "Client Name"],
            key="sort_by"
        )

    with col3:
        search = st.text_input("🔍 Search", placeholder="Search projects...", key="search_projects")

    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Sample projects data
    projects = [
        {
            'id': 'PRJ-001',
            'name': 'Dubai Marina Tower Complex',
            'client': 'Emirates Development Corp',
            'value': '$12,500,000',
            'status': 'Active',
            'risk': 'Low',
            'progress': 75,
            'deadline': '2025-01-15',
            'documents': 12
        },
        {
            'id': 'PRJ-002',
            'name': 'Abu Dhabi Highway Extension',
            'client': 'UAE Roads Authority',
            'value': '$25,700,000',
            'status': 'Active',
            'risk': 'Medium',
            'progress': 45,
            'deadline': '2025-01-20',
            'documents': 8
        },
        {
            'id': 'PRJ-003',
            'name': 'Sharjah Commercial Complex',
            'client': 'Sharjah Investment Group',
            'value': '$8,300,000',
            'status': 'Closed-Won',
            'risk': 'Low',
            'progress': 100,
            'deadline': '2024-12-01',
            'documents': 15
        },
        {
            'id': 'PRJ-004',
            'name': 'Qatar Sports Stadium',
            'client': 'Qatar Sports Federation',
            'value': '$45,000,000',
            'status': 'Active',
            'risk': 'High',
            'progress': 20,
            'deadline': '2025-02-10',
            'documents': 5
        },
        {
            'id': 'PRJ-005',
            'name': 'Riyadh Infrastructure Project',
            'client': 'Saudi Infrastructure Agency',
            'value': '$18,900,000',
            'status': 'Submitted',
            'risk': 'Medium',
            'progress': 90,
            'deadline': '2024-12-30',
            'documents': 20
        }
    ]

    # Display projects
    for project in projects:
        status_colors = {
            'Active': '#0d7377',
            'Submitted': '#b8995a',
            'Closed-Won': '#4ade80',
            'Closed-Lost': '#f87171'
        }
        status_color = status_colors.get(project['status'], '#e0e0e0')
        risk_color = get_risk_color(project['risk'])

        st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(13, 115, 119, 0.05) 100%);
                        border: 1px solid rgba(184, 153, 90, 0.2);
                        border-left: 4px solid {status_color};
                        border-radius: 16px;
                        padding: 1.5rem;
                        margin-bottom: 1rem;
                        transition: all 0.3s ease;
                        cursor: pointer;'>
                <div style='display: grid; grid-template-columns: 2fr 1fr 1fr 1fr 100px; gap: 1.5rem; align-items: center;'>
                    <!-- Project Info -->
                    <div>
                        <div style='color: #b8995a; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.3rem;'>
                            {project['id']}
                        </div>
                        <div style='color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;'>
                            {project['name']}
                        </div>
                        <div style='color: rgba(255,255,255,0.7); font-size: 0.85rem;'>
                            🏢 {project['client']}
                        </div>
                    </div>

                    <!-- Value & Status -->
                    <div>
                        <div style='color: rgba(255,255,255,0.6); font-size: 0.75rem; margin-bottom: 0.3rem;'>
                            PROJECT VALUE
                        </div>
                        <div style='color: #b8995a; font-size: 1.3rem; font-weight: 700;'>
                            {project['value']}
                        </div>
                        <div style='margin-top: 0.5rem;'>
                            <span style='background: {status_color}; color: white; padding: 0.25rem 0.75rem;
                                         border-radius: 6px; font-size: 0.75rem; font-weight: 600;'>
                                {project['status']}
                            </span>
                        </div>
                    </div>

                    <!-- Progress & Risk -->
                    <div>
                        <div style='color: rgba(255,255,255,0.6); font-size: 0.75rem; margin-bottom: 0.3rem;'>
                            COMPLETION
                        </div>
                        <div style='color: #ffffff; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;'>
                            {project['progress']}%
                        </div>
                        <div style='color: rgba(255,255,255,0.6); font-size: 0.75rem; margin-top: 0.5rem;'>
                            Risk: <span style='color: {risk_color}; font-weight: 700;'>{project['risk']}</span>
                        </div>
                    </div>

                    <!-- Deadline & Documents -->
                    <div>
                        <div style='color: rgba(255,255,255,0.6); font-size: 0.75rem; margin-bottom: 0.3rem;'>
                            DEADLINE
                        </div>
                        <div style='color: #ffffff; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;'>
                            📅 {project['deadline']}
                        </div>
                        <div style='color: rgba(255,255,255,0.6); font-size: 0.75rem;'>
                            📄 {project['documents']} docs
                        </div>
                    </div>

                    <!-- Action Button -->
                    <div style='text-align: right;'>
                        <button style='background: linear-gradient(135deg, #0d7377 0%, #0a5a5d 100%);
                                       color: white; border: none; border-radius: 8px;
                                       padding: 0.5rem 1rem; font-weight: 600; cursor: pointer;
                                       transition: all 0.3s ease;'>
                            Open →
                        </button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_new_project():
    """Render the new project creation form"""

    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(13, 115, 119, 0.1) 0%, rgba(26, 26, 26, 0.9) 100%);
                    border: 1px solid rgba(184, 153, 90, 0.3);
                    border-radius: 16px;
                    padding: 2rem;
                    margin-bottom: 2rem;'>
            <h3 style='color: #b8995a; margin: 0 0 1rem 0;'>
                🚀 Create New Bid Project
            </h3>
            <p style='color: rgba(255,255,255,0.7); margin: 0;'>
                Upload RFQ documents and let AI analyze the project requirements
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("new_project_form"):
        col1, col2 = st.columns(2)

        with col1:
            project_name = st.text_input(
                "Project Name *",
                placeholder="e.g., Dubai Marina Tower Complex",
                help="Enter a descriptive name for the project"
            )

            client_name = st.text_input(
                "Client Name *",
                placeholder="e.g., Emirates Development Corp",
                help="Name of the client requesting the bid"
            )

            project_value = st.text_input(
                "Estimated Project Value",
                placeholder="e.g., $12,500,000",
                help="Estimated total project value (optional)"
            )

        with col2:
            deadline = st.date_input(
                "Submission Deadline *",
                help="When does the bid need to be submitted?"
            )

            project_type = st.selectbox(
                "Project Type",
                [
                    "Commercial Construction",
                    "Residential Construction",
                    "Infrastructure",
                    "Industrial",
                    "Healthcare Facility",
                    "Educational Facility",
                    "Mixed-Use Development",
                    "Other"
                ]
            )

            location = st.text_input(
                "Project Location",
                placeholder="e.g., Dubai, UAE",
                help="Where is the project located?"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Document upload section
        st.markdown("""
            <div style='color: #b8995a; font-size: 1.1rem; font-weight: 600; margin-bottom: 1rem;'>
                📎 Upload RFQ Documents
            </div>
        """, unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Drag and drop files here or click to browse",
            type=['pdf', 'docx', 'xlsx', 'msg', 'zip'],
            accept_multiple_files=True,
            help="Supported formats: PDF, DOCX, XLSX, MSG (email), ZIP"
        )

        if uploaded_files:
            st.markdown("<br>", unsafe_allow_html=True)
            st.success(f"✅ {len(uploaded_files)} file(s) ready to upload")

            for file in uploaded_files:
                file_size = len(file.getvalue()) / (1024 * 1024)  # Convert to MB
                st.markdown(f"""
                    <div style='background: rgba(13, 115, 119, 0.1); padding: 0.75rem; border-radius: 8px;
                                border: 1px solid rgba(13, 115, 119, 0.3); margin-bottom: 0.5rem;'>
                        <span style='color: #b8995a;'>📄 {file.name}</span>
                        <span style='color: rgba(255,255,255,0.6); float: right;'>{file_size:.2f} MB</span>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Additional options
        col1, col2 = st.columns(2)

        with col1:
            auto_analyze = st.checkbox("🤖 Auto-run AI analysis after creation", value=True)

        with col2:
            enable_notifications = st.checkbox("🔔 Enable email notifications", value=True)

        # Project notes
        notes = st.text_area(
            "Project Notes (Optional)",
            placeholder="Add any additional notes or requirements...",
            height=100
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Submit buttons
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            submit = st.form_submit_button("🚀 Create Project", type="primary", use_container_width=True)

        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)

        if submit:
            if not project_name or not client_name or not deadline:
                st.error("⚠️ Please fill in all required fields marked with *")
            elif not uploaded_files:
                st.error("⚠️ Please upload at least one RFQ document")
            else:
                with st.spinner("Creating project and processing documents..."):
                    import time
                    time.sleep(2)  # Simulate processing

                st.success("✅ Project created successfully!")
                st.balloons()

                if auto_analyze:
                    st.info("🤖 AI analysis has been queued and will complete shortly")

                # Show project ID
                st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #0d7377 0%, #0a5a5d 100%);
                                padding: 1rem; border-radius: 10px; text-align: center; margin-top: 1rem;'>
                        <div style='color: rgba(255,255,255,0.8); font-size: 0.85rem;'>
                            Project ID
                        </div>
                        <div style='color: #b8995a; font-size: 1.5rem; font-weight: 700; margin-top: 0.25rem;'>
                            PRJ-{datetime.now().strftime('%Y%m%d-%H%M')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        if cancel:
            st.info("Project creation cancelled")


def render_project_details():
    """Render detailed view of a selected project"""

    if not st.session_state.get('current_project'):
        st.info("👈 Select a project from the 'All Projects' tab to view details")
        return

    # Project header
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(13, 115, 119, 0.2) 0%, rgba(26, 26, 26, 0.9) 100%);
                    border: 1px solid rgba(184, 153, 90, 0.3);
                    border-radius: 16px;
                    padding: 2rem;
                    margin-bottom: 2rem;'>
            <div style='display: flex; justify-content: space-between; align-items: start;'>
                <div>
                    <div style='color: #b8995a; font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem;'>
                        PRJ-001
                    </div>
                    <h2 style='color: #ffffff; margin: 0 0 0.5rem 0;'>
                        Dubai Marina Tower Complex
                    </h2>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.95rem;'>
                        🏢 Emirates Development Corp
                    </div>
                </div>
                <div style='text-align: right;'>
                    <div style='background: #4ade80; color: #1a1a1a; padding: 0.5rem 1rem;
                                border-radius: 8px; font-weight: 700; display: inline-block;'>
                        Active
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Project stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Project Value", "$12.5M", "+5% vs estimate")

    with col2:
        st.metric("Completion", "75%", "+15% this week")

    with col3:
        st.metric("Documents", "12", "+3 recent")

    with col4:
        st.metric("Risk Level", "Low", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # Documents section
    st.markdown(create_section_header("📄 Project Documents"), unsafe_allow_html=True)

    # Sample documents
    documents = [
        {'name': 'RFQ_Main_Document.pdf', 'size': '2.4 MB', 'date': '2024-12-01', 'status': 'Processed'},
        {'name': 'Technical_Specifications.pdf', 'size': '1.8 MB', 'date': '2024-12-01', 'status': 'Processed'},
        {'name': 'Budget_Breakdown.xlsx', 'size': '0.5 MB', 'date': '2024-12-02', 'status': 'Processed'},
        {'name': 'Client_Email.msg', 'size': '0.1 MB', 'date': '2024-12-03', 'status': 'Processed'}
    ]

    for doc in documents:
        st.markdown(f"""
            <div style='background: rgba(26, 26, 26, 0.6); border: 1px solid rgba(184, 153, 90, 0.2);
                        border-radius: 10px; padding: 1rem; margin-bottom: 0.75rem;
                        display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <span style='color: #b8995a; font-weight: 600;'>📄 {doc['name']}</span>
                    <span style='color: rgba(255,255,255,0.5); margin-left: 1rem; font-size: 0.85rem;'>
                        {doc['size']} • {doc['date']}
                    </span>
                </div>
                <div>
                    <span style='background: rgba(13, 115, 119, 0.3); color: #0d7377; padding: 0.25rem 0.75rem;
                                 border-radius: 6px; font-size: 0.8rem; font-weight: 600;'>
                        ✓ {doc['status']}
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Actions
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🤖 Run Analysis", use_container_width=True, type="primary"):
            st.info("Redirecting to RFP Analysis...")

    with col2:
        if st.button("✍️ Generate Bid", use_container_width=True, type="primary"):
            st.info("Redirecting to Bid Generation...")

    with col3:
        if st.button("🔍 Check Conflicts", use_container_width=True):
            st.info("Redirecting to Conflict Detection...")

    with col4:
        if st.button("📊 Win Probability", use_container_width=True):
            st.info("Redirecting to Win Probability...")
