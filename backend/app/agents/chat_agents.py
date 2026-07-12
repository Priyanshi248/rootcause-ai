from app.agents.gemini_client import client
from app.core.config import settings


async def ask_question(
    context: str,
    question: str,
):

    prompt = f"""
You are an expert Site Reliability Engineer.

Incident Context:

{context}

User Question:

{question}

Answer clearly.
"""

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
    )

    return response.text