import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Load environment and config
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_ID = "gemini-2.5-flash-lite"

# --- 1. PAGE CONFIGURATION ---
# Setting layout to "wide" uses the full screen width, perfect for code comparison
st.set_page_config(page_title="AI Code Reviewer", page_icon="🕵️‍♂️", layout="wide")

# --- 2. SIDEBAR ---
# Keeps the main screen clean by moving info to the side
with st.sidebar:
    st.header("⚙️ About the Agents")
    st.write("This system uses two distinct AI personas:")
    st.markdown("- **🔍 Agent 1 (Reviewer):** Acts as a Senior QA. Strictly looks for bugs, edge cases, and security risks.")
    st.markdown("- **🛠️ Agent 2 (Fixer):** Acts as a Senior Developer. Takes the QA report and refactors the code without complaining.")
    st.divider()
    st.caption("Powered by Gemini 2.5 Flash Lite")

# --- 3. MAIN HEADER ---
st.title("🕵️‍♂️ Multi-Agent Code Optimizer")
st.markdown("Paste your code below to get an expert review and a refactored version.")

# --- 4. INPUT SECTION ---
user_code = st.text_area("Source Code", height=250, placeholder="Paste your code here (e.g., Python, C++, JS)...")

# Primary button makes it stand out visually
if st.button("🚀 Analyze & Fix Code", type="primary"):
    if not user_code:
        st.warning("⚠️ Please enter some code to analyze.")
    else:
        # --- 5. LOADING UI ---
        with st.status("Initializing AI Agents...", expanded=True) as status:
            
            # Agent 1 
            status.update(label="🔍 Agent 1: Inspecting code for vulnerabilities...", state="running")
            sys_msg_1 = "You are a Senior QA Engineer. Analyze code for bugs and security risks. Be concise. Bullet points only."
            
            try:
                response_1 = client.models.generate_content(
                    model=MODEL_ID,
                    config={'system_instruction': sys_msg_1},
                    contents=user_code
                )
                review_feedback = response_1.text
                
                # Agent 2
                status.update(label="🛠️ Agent 2: Writing optimized code based on QA report...", state="running")
                sys_msg_2 = "You are an Expert Developer. Provide the corrected code in a block and a 1-sentence summary. DO NOT repeat the review."
                prompt_2 = f"Original Code:\n{user_code}\n\nReviewer Feedback:\n{review_feedback}"
                
                response_2 = client.models.generate_content(
                    model=MODEL_ID,
                    config={'system_instruction': sys_msg_2},
                    contents=prompt_2
                )
                fixed_code = response_2.text
                
                status.update(label="✅ Analysis Complete!", state="complete")
            
            except Exception as e:
                status.update(label="❌ An error occurred.", state="error")
                st.error(f"API Error: {e}")
                st.stop() # Stops execution if the API fails

        # --- 6. RESULTS PRESENTATION ---
        st.divider()
        
        # Expander: Hides the text-heavy review so it doesn't clutter the screen
        with st.expander("📋 View Detailed QA Review Findings", expanded=False):
            st.markdown(review_feedback)
        
        # Columns: Side-by-side comparison of old vs. new code
        st.subheader("⚖️ Code Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔴 Original Code")
            # Uses st.code for syntax highlighting
            st.code(user_code) 
            
        with col2:
            st.markdown("### 🟢 Optimized Code")
            # The AI naturally outputs markdown code blocks, which render perfectly here
            st.markdown(fixed_code)