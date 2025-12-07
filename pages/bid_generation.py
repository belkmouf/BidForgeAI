"""
Bid Generation - AI-powered bid proposal generation with multi-model support
"""

import streamlit as st
from utils.theme import create_section_header
import time


def render():
    """Render the bid generation page"""

    st.markdown(create_section_header(
        "AI Bid Generation",
        "Generate professional bid proposals using multiple AI models"
    ), unsafe_allow_html=True)

    # Project selector
    col1, col2 = st.columns([3, 1])

    with col1:
        selected_project = st.selectbox(
            "Select Project",
            [
                "Dubai Marina Tower Complex (PRJ-001)",
                "Abu Dhabi Highway Extension (PRJ-002)",
                "Qatar Sports Stadium (PRJ-004)"
            ],
            key="gen_project"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📄 Load Project", use_container_width=True):
            st.success("✅ Project loaded successfully!")

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs for generation and refinement
    tab1, tab2, tab3 = st.tabs(["🤖 Generate Bid", "💬 Refine with AI Chat", "📊 Compare Models"])

    with tab1:
        render_generation_interface()

    with tab2:
        render_chat_interface()

    with tab3:
        render_model_comparison()


def render_generation_interface():
    """Render the bid generation interface"""

    # AI Model selection
    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(13, 115, 119, 0.15) 0%, rgba(26, 26, 26, 0.9) 100%);
                    border: 1px solid rgba(184, 153, 90, 0.3);
                    border-radius: 12px;
                    padding: 1.5rem;
                    margin-bottom: 2rem;'>
            <h4 style='color: #b8995a; margin: 0 0 1rem 0;'>
                🤖 Select AI Model(s)
            </h4>
            <p style='color: rgba(255,255,255,0.7); margin: 0; font-size: 0.9rem;'>
                Choose one or multiple AI models to generate your bid. Multi-model selection enables side-by-side comparison.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        use_openai = st.checkbox(
            "**OpenAI GPT-4o**",
            value=True,
            help="Industry-leading model with excellent technical writing"
        )
        if use_openai:
            st.markdown("""
                <div style='background: rgba(13, 115, 119, 0.1); padding: 0.5rem; border-radius: 6px;
                            margin-top: 0.5rem; font-size: 0.75rem; color: rgba(255,255,255,0.7);'>
                    ⚡ Fast • 💎 Premium Quality
                </div>
            """, unsafe_allow_html=True)

    with col2:
        use_anthropic = st.checkbox(
            "**Claude Sonnet 4.5**",
            value=False,
            help="Excellent for detailed, nuanced proposals"
        )
        if use_anthropic:
            st.markdown("""
                <div style='background: rgba(184, 153, 90, 0.1); padding: 0.5rem; border-radius: 6px;
                            margin-top: 0.5rem; font-size: 0.75rem; color: rgba(255,255,255,0.7);'>
                    🎯 Precise • 📝 Detailed
                </div>
            """, unsafe_allow_html=True)

    with col3:
        use_gemini = st.checkbox(
            "**Google Gemini 2.0**",
            value=False,
            help="Strong analytical and technical capabilities"
        )
        if use_gemini:
            st.markdown("""
                <div style='background: rgba(13, 115, 119, 0.1); padding: 0.5rem; border-radius: 6px;
                            margin-top: 0.5rem; font-size: 0.75rem; color: rgba(255,255,255,0.7);'>
                    🔬 Analytical • ⚡ Fast
                </div>
            """, unsafe_allow_html=True)

    with col4:
        use_deepseek = st.checkbox(
            "**DeepSeek**",
            value=False,
            help="Cost-effective with good performance"
        )
        if use_deepseek:
            st.markdown("""
                <div style='background: rgba(184, 153, 90, 0.1); padding: 0.5rem; border-radius: 6px;
                            margin-top: 0.5rem; font-size: 0.75rem; color: rgba(255,255,255,0.7);'>
                    💰 Economical • ✅ Reliable
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Generation settings
    with st.expander("⚙️ Advanced Generation Settings", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            tone = st.select_slider(
                "Proposal Tone",
                options=["Conservative", "Balanced", "Aggressive"],
                value="Balanced",
                help="Adjust the competitive positioning of your bid"
            )

            include_pricing = st.checkbox("Include Pricing Strategy", value=True)
            include_timeline = st.checkbox("Include Project Timeline", value=True)

        with col2:
            creativity = st.slider(
                "Creativity Level",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values = more creative, lower = more conservative"
            )

            include_risks = st.checkbox("Include Risk Mitigation", value=True)
            include_value_adds = st.checkbox("Include Value Engineering", value=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Context from RAG
    st.markdown("""
        <div style='background: rgba(184, 153, 90, 0.1); border: 1px solid rgba(184, 153, 90, 0.3);
                    border-radius: 10px; padding: 1rem; margin-bottom: 1.5rem;'>
            <div style='color: #b8995a; font-weight: 600; margin-bottom: 0.5rem;'>
                📚 RAG Context Loaded
            </div>
            <div style='color: rgba(255,255,255,0.7); font-size: 0.85rem;'>
                ✓ 12 RFQ documents analyzed<br>
                ✓ 8 historical winning bids retrieved<br>
                ✓ 15,234 relevant context chunks indexed
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Generate button
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if st.button("🚀 Generate Bid Proposal", use_container_width=True, type="primary"):
            generate_bid(use_openai, use_anthropic, use_gemini, use_deepseek)

    with col2:
        if st.button("💾 Save Draft", use_container_width=True):
            st.success("✅ Draft saved!")

    with col3:
        if st.button("📥 Export", use_container_width=True):
            st.info("Export feature coming soon!")

    # Generated content display
    if st.session_state.get('generated_bid'):
        st.markdown("<br>", unsafe_allow_html=True)
        render_generated_bid()


def generate_bid(use_openai, use_anthropic, use_gemini, use_deepseek):
    """Simulate bid generation"""

    models_selected = sum([use_openai, use_anthropic, use_gemini, use_deepseek])

    if models_selected == 0:
        st.error("⚠️ Please select at least one AI model")
        return

    with st.spinner(f"🤖 Generating bid proposal using {models_selected} AI model(s)..."):
        progress_bar = st.progress(0)
        status_text = st.empty()

        steps = [
            "Loading project context...",
            "Retrieving similar winning bids...",
            "Analyzing RFQ requirements...",
            "Generating proposal structure...",
            "Writing executive summary...",
            "Detailing technical approach...",
            "Creating pricing breakdown...",
            "Finalizing document..."
        ]

        for i, step in enumerate(steps):
            status_text.text(step)
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.4)

        status_text.empty()
        progress_bar.empty()

    st.session_state.generated_bid = True
    st.success("✅ Bid proposal generated successfully!")
    st.balloons()


def render_generated_bid():
    """Render the generated bid proposal"""

    st.markdown(create_section_header("📄 Generated Bid Proposal"), unsafe_allow_html=True)

    # Proposal preview
    st.markdown("""
        <div style='background: #ffffff; color: #1a1a1a; border-radius: 12px;
                    padding: 3rem; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(0,0,0,0.3);'>

            <div style='text-align: center; margin-bottom: 3rem; padding-bottom: 2rem;
                        border-bottom: 3px solid #0d7377;'>
                <h1 style='color: #0d7377; margin: 0 0 0.5rem 0; font-size: 2.5rem;'>
                    BID PROPOSAL
                </h1>
                <h2 style='color: #b8995a; margin: 0; font-size: 1.8rem;'>
                    Dubai Marina Tower Complex
                </h2>
                <p style='color: #666; margin-top: 1rem;'>
                    Submitted to: Emirates Development Corp<br>
                    Date: December 7, 2025<br>
                    Project ID: PRJ-001
                </p>
            </div>

            <h3 style='color: #0d7377; margin-top: 2rem; border-bottom: 2px solid #b8995a; padding-bottom: 0.5rem;'>
                Executive Summary
            </h3>
            <p style='color: #333; line-height: 1.8; text-align: justify;'>
                We are pleased to submit this comprehensive proposal for the Dubai Marina Tower Complex project.
                With over 15 years of experience in premium high-rise construction across the GCC region and a
                proven track record of delivering landmark projects on time and within budget, we are uniquely
                positioned to bring your vision to life.
            </p>
            <p style='color: #333; line-height: 1.8; text-align: justify;'>
                Our approach combines cutting-edge construction methodologies with sustainable building practices,
                ensuring a structure that meets the highest standards of quality, safety, and environmental
                responsibility. This proposal outlines our technical approach, project timeline, pricing structure,
                and the unique value we bring to this prestigious development.
            </p>

            <h3 style='color: #0d7377; margin-top: 2.5rem; border-bottom: 2px solid #b8995a; padding-bottom: 0.5rem;'>
                Technical Approach
            </h3>
            <p style='color: #333; line-height: 1.8; text-align: justify;'>
                Our technical approach is built on three core pillars:
            </p>
            <ul style='color: #333; line-height: 1.8;'>
                <li><strong>Advanced Construction Technology:</strong> Utilization of BIM (Building Information Modeling)
                    for precise planning and coordination across all trades.</li>
                <li><strong>Quality Assurance:</strong> ISO 9001-certified quality management system with dedicated
                    quality control personnel on-site throughout the project lifecycle.</li>
                <li><strong>Safety Excellence:</strong> Zero-accident safety culture with OHSAS 18001 certification
                    and comprehensive site safety protocols.</li>
            </ul>

            <h3 style='color: #0d7377; margin-top: 2.5rem; border-bottom: 2px solid #b8995a; padding-bottom: 0.5rem;'>
                Project Timeline
            </h3>
            <table style='width: 100%; border-collapse: collapse; margin-top: 1rem;'>
                <tr style='background: #0d7377; color: white;'>
                    <th style='padding: 0.75rem; text-align: left; border: 1px solid #ddd;'>Phase</th>
                    <th style='padding: 0.75rem; text-align: left; border: 1px solid #ddd;'>Duration</th>
                    <th style='padding: 0.75rem; text-align: left; border: 1px solid #ddd;'>Key Milestones</th>
                </tr>
                <tr>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>Mobilization</td>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>4 weeks</td>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>Site setup, permits, team assembly</td>
                </tr>
                <tr style='background: #f5f5f5;'>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>Foundation</td>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>12 weeks</td>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>Excavation, piling, foundation completion</td>
                </tr>
                <tr>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>Superstructure</td>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>36 weeks</td>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>Frame erection, floor slabs, envelope</td>
                </tr>
                <tr style='background: #f5f5f5;'>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>Finishing</td>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>20 weeks</td>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>MEP, interiors, façade completion</td>
                </tr>
                <tr>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>Commissioning</td>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>4 weeks</td>
                    <td style='padding: 0.75rem; border: 1px solid #ddd;'>Testing, handover, documentation</td>
                </tr>
            </table>

            <h3 style='color: #0d7377; margin-top: 2.5rem; border-bottom: 2px solid #b8995a; padding-bottom: 0.5rem;'>
                Investment Summary
            </h3>
            <div style='background: linear-gradient(135deg, #0d7377 0%, #0a5a5d 100%);
                        color: white; padding: 2rem; border-radius: 10px; margin-top: 1rem;'>
                <div style='text-align: center;'>
                    <div style='font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem;'>
                        TOTAL PROJECT INVESTMENT
                    </div>
                    <div style='font-size: 3rem; font-weight: 700; color: #b8995a;'>
                        $12,500,000
                    </div>
                    <div style='font-size: 0.85rem; opacity: 0.8; margin-top: 0.5rem;'>
                        Inclusive of all materials, labor, equipment, and overhead
                    </div>
                </div>
            </div>

            <div style='margin-top: 3rem; padding-top: 2rem; border-top: 2px solid #ddd; text-align: center;'>
                <p style='color: #666; font-style: italic;'>
                    This proposal is valid for 90 days from the date of submission.<br>
                    We look forward to the opportunity to partner with you on this prestigious project.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Action buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("✏️ Edit in Chat", use_container_width=True, type="primary"):
            st.info("Switching to chat interface for refinement...")

    with col2:
        if st.button("📥 Export HTML", use_container_width=True):
            st.success("✅ HTML file downloaded!")

    with col3:
        if st.button("📄 Export PDF", use_container_width=True):
            st.success("✅ PDF file downloaded!")

    with col4:
        if st.button("📧 Email", use_container_width=True):
            st.info("Email feature coming soon!")


def render_chat_interface():
    """Render the AI chat interface for bid refinement"""

    st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(13, 115, 119, 0.15) 0%, rgba(26, 26, 26, 0.9) 100%);
                    border: 1px solid rgba(184, 153, 90, 0.3);
                    border-radius: 12px;
                    padding: 1.5rem;
                    margin-bottom: 2rem;'>
            <h4 style='color: #b8995a; margin: 0 0 0.5rem 0;'>
                💬 Iterative Bid Refinement
            </h4>
            <p style='color: rgba(255,255,255,0.7); margin: 0; font-size: 0.9rem;'>
                Chat with AI to refine and improve your bid proposal. Request changes, add sections, or adjust tone.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Chat history
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = [
            {
                'role': 'assistant',
                'content': "Hello! I'm your AI bid assistant. I've generated the initial proposal. How would you like to refine it?"
            }
        ]

    # Display chat messages
    for message in st.session_state.chat_messages:
        if message['role'] == 'user':
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #0d7377 0%, #0a5a5d 100%);
                            color: white; padding: 1rem; border-radius: 10px;
                            margin: 1rem 0; margin-left: 3rem;'>
                    <div style='font-weight: 600; margin-bottom: 0.5rem;'>👤 You</div>
                    <div>{message['content']}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='background: rgba(184, 153, 90, 0.15);
                            color: white; padding: 1rem; border-radius: 10px;
                            margin: 1rem 0; margin-right: 3rem; border: 1px solid rgba(184, 153, 90, 0.3);'>
                    <div style='font-weight: 600; margin-bottom: 0.5rem; color: #b8995a;'>🤖 AI Assistant</div>
                    <div>{message['content']}</div>
                </div>
            """, unsafe_allow_html=True)

    # Chat input
    user_input = st.text_input(
        "Type your refinement request...",
        placeholder="e.g., 'Make the executive summary more persuasive' or 'Add a section on sustainability'",
        key="chat_input"
    )

    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Send", use_container_width=True, type="primary"):
            if user_input:
                st.session_state.chat_messages.append({'role': 'user', 'content': user_input})
                # Simulate AI response
                st.session_state.chat_messages.append({
                    'role': 'assistant',
                    'content': f"I'll {user_input.lower()}. Let me update the proposal... ✅ Done! The changes have been applied."
                })
                st.rerun()

    # Quick action suggestions
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**💡 Quick Actions:**")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Make it more competitive", use_container_width=True):
            st.info("AI is adjusting the competitive positioning...")
    with col2:
        if st.button("Add sustainability section", use_container_width=True):
            st.info("AI is adding sustainability initiatives...")
    with col3:
        if st.button("Enhance technical details", use_container_width=True):
            st.info("AI is expanding technical specifications...")


def render_model_comparison():
    """Render side-by-side model comparison"""

    st.markdown("""
        <div style='background: rgba(184, 153, 90, 0.1); border: 1px solid rgba(184, 153, 90, 0.3);
                    border-radius: 10px; padding: 1rem; margin-bottom: 1.5rem;'>
            <div style='color: #b8995a; font-weight: 600;'>
                📊 Multi-Model Comparison
            </div>
            <div style='color: rgba(255,255,255,0.7); font-size: 0.85rem; margin-top: 0.5rem;'>
                Compare proposals generated by different AI models to choose the best approach
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(13, 115, 119, 0.05) 100%);
                        border: 1px solid rgba(184, 153, 90, 0.2);
                        border-radius: 12px;
                        padding: 1.5rem;'>
                <h4 style='color: #0d7377; margin: 0 0 1rem 0;'>OpenAI GPT-4o</h4>
                <div style='color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 1.6;'>
                    • Strong executive summary<br>
                    • Clear technical approach<br>
                    • Well-structured pricing<br>
                    • Professional tone throughout
                </div>
                <div style='margin-top: 1rem;'>
                    <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-bottom: 0.3rem;'>
                        Quality Score
                    </div>
                    <div style='background: rgba(184, 153, 90, 0.2); height: 8px; border-radius: 4px;'>
                        <div style='background: #4ade80; height: 100%; width: 92%; border-radius: 4px;'></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(26, 26, 26, 0.9) 0%, rgba(184, 153, 90, 0.05) 100%);
                        border: 1px solid rgba(13, 115, 119, 0.2);
                        border-radius: 12px;
                        padding: 1.5rem;'>
                <h4 style='color: #b8995a; margin: 0 0 1rem 0;'>Claude Sonnet 4.5</h4>
                <div style='color: rgba(255,255,255,0.8); font-size: 0.9rem; line-height: 1.6;'>
                    • Highly detailed analysis<br>
                    • Nuanced risk mitigation<br>
                    • Comprehensive approach<br>
                    • Excellent depth
                </div>
                <div style='margin-top: 1rem;'>
                    <div style='color: rgba(255,255,255,0.6); font-size: 0.8rem; margin-bottom: 0.3rem;'>
                        Quality Score
                    </div>
                    <div style='background: rgba(184, 153, 90, 0.2); height: 8px; border-radius: 4px;'>
                        <div style='background: #b8995a; height: 100%; width: 95%; border-radius: 4px;'></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.info("💡 Select multiple models during generation to enable this comparison feature")
