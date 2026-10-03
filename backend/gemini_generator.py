import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please check your .env file."
    )

client = genai.Client(api_key=API_KEY)


def generate_legal_document(
    document_type: str,
    parties: str,
    terms: str,
    effective_date: str
) -> str:

    prompt = f"""
You are an AI legal document drafting assistant.

Generate a professional draft legal document based on the
information provided below.

Document Type:
{document_type}

Parties:
{parties}

Terms and Conditions:
{terms}

Effective Date:
{effective_date}

Requirements:

1. Create a clear professional legal document.
2. Include an appropriate title.
3. Include the parties involved.
4. Include the effective date.
5. Organize the terms into appropriate sections.
6. Include standard legal clauses where appropriate.
7. Do not invent specific personal information.
8. Use placeholders when information is missing.
9. Return only the document text.
10. Clearly state that this is an AI-generated draft
    and should be reviewed by a qualified legal professional.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text