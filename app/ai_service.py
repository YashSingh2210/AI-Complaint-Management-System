import os
from dotenv import load_dotenv
import google.generativeai as genai
# Load .env file
load_dotenv()
# Read API Key
API_KEY = os.getenv("GEMINI_API_KEY")
COMPANY_NAME = os.getenv("COMPANY_NAME")
# Configure Gemini
genai.configure(api_key=API_KEY)
# Load model
model = genai.GenerativeModel("gemini-3.6-flash")

#For category:-
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

# For complaint getting priority:-
def get_priority(complaint):

    prompt = f"""
You are a complaint priority classifier.

Choose ONLY one:
High
Medium
Low

Complaint:
{complaint}
Return only the priority.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

# AI reply function:-
def generate_reply(customer_name,complaint):

    prompt = f"""
Write a short professional customer support reply.

Customer Name:{customer_name}
Complaint:
{complaint}
Start the reply with:
Dear {customer_name},

With Regards,
{COMPANY_NAME} Support Team

Return only the reply.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

# AI changes reply according to status:-
def generate_status_reply(customer_name, complaint, status):

    prompt = f"""
Customer Name: {customer_name}

Complaint:
{complaint}

Current Status:
{status}

Write a short professional email reply to the customer.

Rules:
- Address the customer by their name.
- If status is Resolved, tell them the issue has been resolved.
- If status is In Progress, tell them the team is working on it.
- If status is Rejected, politely explain that the complaint could not be verified.
- Do not use markdown.

With Regards,
{COMPANY_NAME} Support Team

- Return only the email text.
"""
    response = model.generate_content(prompt)
    return response.text.strip()