import streamlit as st
import time
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🔬",
    layout="centered"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

* { font-family: 'DM Mono', monospace; }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

/* Dark background */
.stApp {
    background-color: #0a0a0f;
    color: #e8e8e8;
}

/* Main container */
.block-container {
    padding-top: 3rem;
    max-width: 780px;
}

/* Heading */
.main-heading {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00f5c4 0%, #0088ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
    margin-bottom: 0.2rem;
}

.sub-heading {
    color: #555;
    font-size: 0.78rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* Input box */
.stTextArea textarea {
    background-color: #111118 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 10px !important;
    color: #e8e8e8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 14px !important;
    transition: border 0.2s;
}
.stTextArea textarea:focus {
    border: 1px solid #00f5c4 !important;
    box-shadow: 0 0 0 2px rgba(0,245,196,0.08) !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #00f5c4, #0088ff);
    color: #0a0a0f;
    border: none;
    border-radius: 8px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    padding: 0.6rem 2rem;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.1s;
    width: 100%;
}
.stButton > button:hover {
    opacity: 0.88;
    transform: translateY(-1px);
}
.stButton > button:active {
    transform: translateY(0px);
}

/* Stage card */
.stage-card {
    background: #111118;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: border 0.3s;
}
.stage-card.active {
    border-color: #00f5c4;
    box-shadow: 0 0 16px rgba(0,245,196,0.08);
}
.stage-card.done {
    border-color: #1a3a2a;
}
.stage-card.pending {
    opacity: 0.4;
}

.stage-icon { font-size: 1.4rem; min-width: 32px; text-align: center; }
.stage-label { font-family: 'Syne', sans-serif; font-weight: 600; font-size: 0.95rem; }
.stage-desc { font-size: 0.72rem; color: #555; margin-top: 2px; }
.stage-status {
    margin-left: auto;
    font-size: 0.7rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.status-active { color: #00f5c4; }
.status-done { color: #2a7a5a; }
.status-pending { color: #333; }

/* Result box */
.result-box {
    background: #0d0d15;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 1.4rem;
    margin-top: 0.6rem;
    font-size: 0.85rem;
    line-height: 1.7;
    color: #ccc;
    white-space: pre-wrap;
    max-height: 320px;
    overflow-y: auto;
}

/* Section label */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #444;
    margin: 1.8rem 0 0.8rem;
}

/* Divider */
hr { border-color: #1a1a2e; margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-heading">ResearchMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-heading">Multi-Agent Research Pipeline</div>', unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
topic = st.text_area(
    "Research Topic",
    placeholder="e.g. Latest breakthroughs in quantum computing 2025...",
    height=100,
    label_visibility="collapsed"
)

run_btn = st.button("⚡  Run Research Pipeline")

# ── Pipeline stages definition ─────────────────────────────────────────────────
STAGES = [
    ("🔍", "Search Agent",   "Finding recent, reliable information across the web"),
    ("📄", "Reader Agent",   "Scraping top resources for deeper content"),
    ("✍️",  "Writer Agent",   "Drafting a comprehensive research report"),
    ("🧠", "Critic Agent",   "Reviewing & refining the final report"),
]


def render_stages(current: int, done_set: set):
    for i, (icon, label, desc) in enumerate(STAGES):
        if i in done_set:
            css = "done"
            status_css = "status-done"
            status_txt = "✓ Done"
        elif i == current:
            css = "active"
            status_css = "status-active"
            status_txt = "● Running"
        else:
            css = "pending"
            status_css = "status-pending"
            status_txt = "○ Waiting"

        st.markdown(f"""
        <div class="stage-card {css}">
            <div class="stage-icon">{icon}</div>
            <div>
                <div class="stage-label">{label}</div>
                <div class="stage-desc">{desc}</div>
            </div>
            <div class="stage-status {status_css}">{status_txt}</div>
        </div>
        """, unsafe_allow_html=True)


# ── Run pipeline ───────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.markdown('<div class="section-label">Pipeline Progress</div>', unsafe_allow_html=True)
        stage_placeholder = st.empty()
        done = set()

        # ── Stage 1: Search ──────────────────────────────────────────────────
        with stage_placeholder.container():
            render_stages(0, done)

        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        search_results = search_result['messages'][-1].content
        done.add(0)

        # ── Stage 2: Reader ──────────────────────────────────────────────────
        with stage_placeholder.container():
            render_stages(1, done)

        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{search_results[:800]}"
            )]
        })
        scraped_content = reader_result['messages'][-1].content
        done.add(1)

        # ── Stage 3: Writer ──────────────────────────────────────────────────
        with stage_placeholder.container():
            render_stages(2, done)

        research_combined = (
            f"SEARCH RESULTS:\n{search_results}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{scraped_content}"
        )
        report = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })
        done.add(2)

        # ── Stage 4: Critic ──────────────────────────────────────────────────
        with stage_placeholder.container():
            render_stages(3, done)

        feedback = critic_chain.invoke({"report": report})
        done.add(3)

        # All done
        with stage_placeholder.container():
            render_stages(-1, done)

        # ── Results ──────────────────────────────────────────────────────────
        st.markdown('<hr>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Research Report</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box">{report}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label">Critic Feedback</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box">{feedback}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label">Raw Search Results</div>', unsafe_allow_html=True)
        with st.expander("View search results"):
            st.markdown(f'<div class="result-box">{search_results}</div>', unsafe_allow_html=True)

        with st.expander("View scraped content"):
            st.markdown(f'<div class="result-box">{scraped_content}</div>', unsafe_allow_html=True)