import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_ID = "gemini-2.5-flash"

st.set_page_config(page_title="AI Code Reviewer", page_icon="🕵️‍♂️", layout="wide")

# --- ADDED: Custom CSS and HTML injection to create a fixed, sticky header ---
st.markdown(
    """
    <style>
    .sticky-header {
        position: fixed;
        top: 0;
        left: 21rem; /* Aligns past the default expanded sidebar */
        right: 0;
        background-color: #0e1117; /* Streamlit dark mode background */
        padding: 3rem 2rem 1rem 0rem;
        z-index: 990;
    }
    /* Pushes the main app content down so it doesn't hide behind the sticky header */
    .block-container {
        padding-top: 10rem !important;
    }
    /* Ensures the Deploy/GitHub top-right menu stays clickable above our background */
    [data-testid="stHeader"] {
        background-color: transparent;
        z-index: 1000;
    }
    /* Adjusts for mobile screens when the sidebar collapses */
    @media (max-width: 768px) {
        .sticky-header {
            left: 2rem;
        }
    }
    </style>
    <div class="sticky-header">
        <h1 style="margin: 0;">🕵️‍♂️ RepoReviewer</h1>
    </div>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("⚙️ About the System")
    st.write("This tool uses two distinct AI personas:")
    st.markdown("- **🔍 Agent 1 (Reviewer):** Acts as a Senior QA.")
    st.markdown("- **🛠️ Agent 2 (Fixer):** Acts as a Senior Developer.")
    st.divider()
    st.caption(f"Powered by {MODEL_ID}")

st.markdown("Paste your code below to get an expert review and a refactored version.")

user_code = st.text_area("Source Code", height=250, placeholder="Paste your code here...")

if "review_feedback" not in st.session_state:
    st.session_state.review_feedback = None
if "fixed_code" not in st.session_state:
    st.session_state.fixed_code = None

if st.button("🚀 Analyze & Fix Code", type="primary"):
    if not user_code:
        st.warning("⚠️ Please enter some code to analyze.")
    else:
        with st.spinner("Agents are reviewing and fixing your code..."):
            try:
                sys_msg_1 = "You are a Senior QA Engineer. Analyze code for bugs and security risks. Be concise. Bullet points only."
                response_1 = client.models.generate_content(
                    model=MODEL_ID,
                    config={'system_instruction': sys_msg_1},
                    contents=user_code
                )
                st.session_state.review_feedback = response_1.text

                sys_msg_2 = "You are an Expert Developer. Provide the corrected code in a block and a 1-sentence summary. DO NOT repeat the review."
                prompt_2 = f"Original Code:\n{user_code}\n\nReviewer Feedback:\n{st.session_state.review_feedback}"
                response_2 = client.models.generate_content(
                    model=MODEL_ID,
                    config={'system_instruction': sys_msg_2},
                    contents=prompt_2
                )
                st.session_state.fixed_code = response_2.text
                
            except Exception as e:
                st.error(f"❌ API Error: {e}")
                st.stop()
        
        st.success("✅ Analysis Complete!")

if st.session_state.review_feedback and st.session_state.fixed_code:
    st.divider()
    
    with st.expander("📋 View Detailed QA Review Findings", expanded=False):
        st.markdown(st.session_state.review_feedback)
    
    st.subheader("⚖️ Code Comparison")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔴 Original Code")
        st.code(user_code) 
        
    with col2:
        st.markdown("### 🟢 Optimized Code")
        st.markdown(st.session_state.fixed_code)