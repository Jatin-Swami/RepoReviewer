import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_ID = "gemini-2.5-flash"

st.set_page_config(page_title="AI Code Reviewer", page_icon="🕵️‍♂️", layout="wide")

with st.sidebar:
    st.header("⚙️ About the System")
    st.write("This tool uses two distinct AI personas:")
    st.markdown("- **🔍 Agent 1 (Reviewer):** Acts as a Senior QA.")
    st.markdown("- **🛠️ Agent 2 (Fixer):** Acts as a Senior Developer.")
    st.divider()
    st.caption(f"Powered by {MODEL_ID}")

st.title("🕵️‍♂️ Multi-Agent Code Optimizer")
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
        # Replaced st.status with st.spinner here to completely remove the blank dropdown box issue while keeping 2 agents
        with st.spinner("🤖 Agents are reviewing and fixing your code..."):
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