import os
import sys
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors


load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


MODEL_ID = "gemini-2.5-flash-lite" 

class CodeSystem:
    @staticmethod
    def get_reviewer_response(code):
        """Agent 1: Strict, concise reviewer."""
        
        sys_msg = "You are a Senior QA Engineer. Analyze code for bugs and security risks. Be concise. Bullet points only."
        
        print("\n🔍 [Agent 1] Reviewing code...")
        response = client.models.generate_content(
            model=MODEL_ID,
            config={'system_instruction': sys_msg},
            contents=code
        )
        return response.text

    @staticmethod
    def get_fixer_response(original_code, review_feedback):
        """Agent 2: Focused developer. Only outputs code and a tiny summary."""
        sys_msg = """
        You are an Expert Developer. 
        Your ONLY job is to provide the corrected code. 
        Do NOT repeat the reviewer's comments. 
        Do NOT explain simple things. 
        Format: [Fixed Code Block] then a 1-sentence summary.
        """
        
        prompt = f"Original Code:\n{original_code}\n\nReviewer Feedback:\n{review_feedback}"
        
        print("\n\n🛠️ [Agent 2] Generating fixes...")
        response = client.models.generate_content(
            model=MODEL_ID,
            config={'system_instruction': sys_msg},
            contents=prompt
        )
        return response.text

def get_input():
    print("\n" + "="*50)
    print("PASTE CODE (Press Ctrl+Z/D + Enter to finish)")
    print("="*50)
    return sys.stdin.read().strip()

if __name__ == "__main__":
    user_code = get_input()
    
    if not user_code:
        print("No code provided. Exiting.")
        sys.exit()

    try:
        review = CodeSystem.get_reviewer_response(user_code)
        print(f"\n--- 📋 REVIEW FINDINGS ---\n{review}")
        time.sleep(10)
        fixed = CodeSystem.get_fixer_response(user_code, review)
        print(f"\n--- ✅ FINAL VERSION ---\n{fixed}")

    except Exception as e:
        print(f"\n❌ Pipeline Error: {e}")
"""
void main() {
   char str[] = {'H', 'E', 'L', 'L', 'O'};
   printf("%s", str);
}
"""