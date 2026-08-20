import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Read API Key
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Load model
model = genai.GenerativeModel("gemini-3.6-flash")


def get_category(complaint):

    prompt = f"""
You are a complaint classifier.

Classify the complaint into ONLY one category from:

- Payment
- Delivery
- Technical
- Product
- Service
- Other

Complaint:
{complaint}

Return only the category name.
"""

    response = model.generate_content(prompt)

    return response.text.strip()