from app.agents.gemini_client import client
from app.core.config import settings


async def ask_ai(
    context: str,
    task: str,
    question: str | None,
):

    prompt = f"""
You are an expert Site Reliability Engineer.

Incident Context

{context}

Task

{task}

Question

{question}

Return a professional answer.
"""

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
    )

    return response.text