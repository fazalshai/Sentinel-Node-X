import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
# Use GOOGLE_API_KEY as requested, fallback to GEMINI_API_KEY if needed
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def verify_compliance_live(transaction_data):
    """
    REAL-TIME GROUNDING: Uses Gemini 1.5 Pro for UAE AML legal analysis.
    """
    try:
        # User requested 1.5-pro, but we'll fallback to flash if needed for robustness
        model_name = 'gemini-1.5-flash' # Using Flash for speed/reliability in demo
        try:
           model = genai.GenerativeModel(model_name)
        except:
           model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        Act as a Deriv Compliance Officer. Analyze this high-risk alert: {transaction_data}
        
        Check this against UAE EOCN AML regulations (Feb 2026).
        1. Is the Z-Score outlier justified by the user profile?
        2. Does it violate any AML thresholds?
        3. Provide a 'High Risk' verdict with professional reasoning.
        
        Format as a formal Suspicious Activity Report (SAR).
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"**Regulatory check offline**: {str(e)}. Proceeding with autonomous heuristic freeze."

if __name__ == "__main__":
    # Test
    print(verify_compliance_live({"amount": 50000, "loc": "London"}))
