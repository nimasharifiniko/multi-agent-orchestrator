"""
Streamlit Dashboard for Multi-Agent Orchestration System.
Visualizes Researcher, Writer, and Reviewer agents in real-time with feedback loop tracking.

Built by: Nima Sharifi Niko
"""

import streamlit as st
import os
from dotenv import load_dotenv

from src.orchestrator import Orchestrator
from src.models import WorkflowStatus

load_dotenv()

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Multi-Agent Orchestrator · Nima Sharifi Niko",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM STYLING: PURPLE / WHITE THEME ---
st.markdown(
    """
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(180deg, #1a0b2e 0%, #2d1b4e 100%);
        color: #ffffff;
    }
    
    /* Sidebar Background */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0620 0%, #1a0b2e 100%);
        border-right: 1px solid #6a3aa8;
    }
    
    /* Sidebar text color */
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Profile image styling */
    section[data-testid="stSidebar"] img {
        border-radius: 50%;
        border: 3px solid #a855f7;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.5);
    }
    
    /* Header Titles */
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a855f7 0%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #c4b5fd;
        font-size: 1rem;
        margin-bottom: 0.4rem;
    }
    .brand-tag {
        color: #a855f7;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 1.5rem;
    }
    
    /* Primary Button Styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #7c3aed 0%, #a855f7 100%);
        color: white;
        border: none;
        font-weight: 700;
        padding: 0.6rem;
        border-radius: 10px;
        transition: transform 0.2s;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background-color: #2d1b4e !important;
        color: #ffffff !important;
        border: 1px solid #6a3aa8 !important;
        border-radius: 8px !important;
    }
    
    /* Slider */
    .stSlider [data-baseweb="slider"] > div > div {
        background: #a855f7 !important;
    }
    
    /* Agent Section Headers */
    h3 {
        color: #c4b5fd !important;
        border-bottom: 2px solid #6a3aa8;
        padding-bottom: 8px;
    }
    
    /* Alerts / Info boxes background alignment */
    div[data-testid="stAlert"] {
        border-radius: 10px;
        border-left: 4px solid #a855f7;
    }
    
    /* Expander */
    div[data-testid="stExpander"] {
        background-color: rgba(168, 85, 247, 0.08);
        border: 1px solid #6a3aa8;
        border-radius: 10px;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #a855f7 !important;
        font-weight: 800;
    }
    
    /* Footer Brand */
    .footer-brand {
        text-align: center;
        color: #a855f7;
        font-size: 0.85rem;
        padding: 1rem;
        margin-top: 2rem;
        border-top: 1px solid #6a3aa8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    # Profile Photo
    try:
        st.image("5935982297767153284 (2).jpg", width=140)
    except Exception:
        pass

    st.markdown("### 👨‍💻 Nima Sharifi Niko")
    st.caption("Python Developer · AI Engineer")
    st.markdown("[🔗 github.com/nimasharifiniko](https://github.com/nimasharifiniko)")
    st.markdown("---")
    
    st.title("⚙️ Orchestrator Config")
    
    st.subheader("Model Configuration")
    st.text_input("LLM Model", value=os.getenv("LLM_MODEL", "qwen2.5-coder:7b"), disabled=True)
    st.text_input("Provider", value="Local Ollama Server", disabled=True)
    
    st.markdown("---")
    st.subheader("Workflow Parameters")
    quality_threshold = st.slider("Quality Threshold (1-10)", min_value=5, max_value=10, value=7, help="Minimum Reviewer score required for approval.")
    max_iterations = st.slider("Max Iterations", min_value=1, max_value=5, value=3, help="Maximum revision attempts.")
    
    st.markdown("---")
    st.caption("⚡ Built with Python, Ollama & Multi-Agent Architecture")

# --- HEADER ---
st.markdown('<div class="main-title">🤖 Multi-Agent Orchestration System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Autonomous multi-agent research, drafting, and iterative peer review workflow</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-tag">CRAFTED BY NIMA SHARIFI NIKO</div>', unsafe_allow_html=True)

# --- INPUT SECTION ---
default_topic = "How AI Agents are changing software development"
topic_input = st.text_input("🎯 Enter Research Topic:", value=default_topic, placeholder="e.g., The Future of Quantum Computing in Security")

run_button = st.button("🚀 Run Multi-Agent Workflow", type="primary", use_container_width=True)

# --- WORKFLOW EXECUTION ---
if run_button:
    if not topic_input or not topic_input.strip():
        st.error("Please enter a valid topic before running the workflow.")
    else:
        orchestrator = Orchestrator(max_iterations=max_iterations, quality_threshold=quality_threshold)
        
        # Progress UI placeholders
        st.markdown("### 🔄 Live Agent Execution Pipeline")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🔍 Researcher")
            research_status = st.empty()
            research_status.info("🟡 Status: Waiting...")
            research_output = st.empty()
            
        with col2:
            st.subheader("✍️ Writer")
            writer_status = st.empty()
            writer_status.info("🟡 Status: Waiting...")
            writer_output = st.empty()
            
        with col3:
            st.subheader("🧐 Reviewer")
            reviewer_status = st.empty()
            reviewer_status.info("🟡 Status: Waiting...")
            reviewer_output = st.empty()

        feedback_banner = st.empty()
        
        # === EXECUTE WORKFLOW ===
        research_status.warning("⏳ Status: Researching...")
        with st.spinner("Multi-Agent pipeline in execution..."):
            state = orchestrator.run(topic_input.strip())
            
        # === UPDATE UI POST-EXECUTION ===
        if state.research:
            research_status.success("✅ Status: Completed")
            with research_output.expander("View Research Findings", expanded=False):
                st.write(f"**Summary:** {state.research.summary}")
                st.write("**Key Findings:**")
                for finding in state.research.key_findings:
                    st.markdown(f"- {finding}")
                    
        if state.draft:
            writer_status.success("✅ Status: Completed")
            with writer_output.expander("View Draft Structure", expanded=False):
                st.write(f"**Title:** {state.draft.title}")
                st.write(f"**Key Points Count:** {len(state.draft.key_points)}")
                
        if state.review:
            reviewer_status.success(f"✅ Status: Evaluated ({state.review.quality_score}/10)")
            with reviewer_output.expander("View Reviewer Feedback", expanded=False):
                st.metric(label="Quality Score", value=f"{state.review.quality_score} / 10")
                st.write(f"**Approval Status:** {'Approved ✅' if state.review.approved else 'Needs Revision ⚠️'}")
                st.info(f"**Feedback:** {state.review.feedback}")
                if state.review.issues:
                    st.write("**Identified Issues:**")
                    for issue in state.review.issues:
                        st.markdown(f"- {issue}")

        # === ITERATION / FEEDBACK LOOP STATUS ===
        if state.iteration > 1:
            feedback_banner.warning(f"🔁 **Feedback Loop Activated:** Report underwent **{state.iteration} iterations** before meeting the quality threshold ({quality_threshold}/10).")
        else:
            feedback_banner.success(f"🎯 **First-Pass Approval:** Draft passed quality threshold ({quality_threshold}/10) on the first iteration!")

        # === FINAL OUTPUT DISPLAY ===
        st.markdown("---")
        st.markdown("### 📄 Generated Final Report")
        
        if state.final_output:
            st.markdown(state.final_output)
            
            # Download button
            st.download_button(
                label="📥 Download Report as Markdown",
                data=state.final_output,
                file_name=f"{topic_input.strip().lower().replace(' ', '_')}_report.md",
                mime="text/markdown",
                use_container_width=True,
            )
        else:
            st.error(f"Workflow failed to generate final report: {state.error}")

# --- FOOTER ---
st.markdown('<div class="footer-brand">© 2025 · Multi-Agent Orchestration System · Developed by Nima Sharifi Niko</div>', unsafe_allow_html=True)