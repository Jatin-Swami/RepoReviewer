import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_ID = "gemini-2.5-flash-lite"

st.set_page_config(page_title="AI Code Reviewer", page_icon="🔍")
st.title("🚀 Multi-Agent Code Fixer")

user_code = st.text_area("Paste your code here:", height=200, placeholder="void main() { ... }")

if st.button("Analyze & Fix"):
    if not user_code:
        st.warning("Please enter some code first!")
    else:
        with st.status("🔍 Agent 1: Reviewing code...", expanded=True) as status:
            sys_msg_1 = "You are a Senior QA Engineer. Analyze code for bugs and security risks. Be concise. Bullet points only."
            response_1 = client.models.generate_content(
                model=MODEL_ID,
                config={'system_instruction': sys_msg_1},
                contents=user_code
            )
            review_feedback = response_1.text
            st.markdown("### 📋 Review Findings")
            st.write(review_feedback)
            
            status.update(label="🛠️ Agent 2: Generating fixes...", state="running")
            sys_msg_2 = "You are an Expert Developer. Provide the corrected code in a block and a 1-sentence summary."
            prompt_2 = f"Original Code:\n{user_code}\n\nReviewer Feedback:\n{review_feedback}"
            
            response_2 = client.models.generate_content(
                model=MODEL_ID,
                config={'system_instruction': sys_msg_2},
                contents=prompt_2
            )
            status.update(label="✅ Process Complete!", state="complete")
        
        st.divider()
        st.subheader("✅ Final Version")
        st.markdown(response_2.text)