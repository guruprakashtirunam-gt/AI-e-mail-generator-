import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Initialize the model (using gemini-pro/gemini-1.5-flash for text generation)
try:
    # Use flash as it's efficient for this task
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    model = None
    print(f"Failed to initialize Gemini model: {e}")

def generate_email_content(prompt):
    """
    Calls the Gemini API to generate the email based on the prompt.
    Returns the generated text.
    """
    if not model:
        return "Error: Gemini model not initialized. Please ensure GEMINI_API_KEY is set in your .env file."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during generation: {str(e)}"
