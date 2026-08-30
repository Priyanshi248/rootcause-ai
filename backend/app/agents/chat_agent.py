from app.agents.ai_client import client
from app.core.config import settings


async def ask_question(
    context: str,
    question: str,
):

    prompt = f"""
You are a Senior Site Reliability Engineer.

Answer ONLY using the provided incident history.

If the answer cannot be determined from the incidents,
clearly say that.

=========================
INCIDENT HISTORY
=========================

{context}

=========================
QUESTION
=========================

{question}

Provide:

1. Direct answer

2. Reasoning

3. Recommended action (if applicable)

4. Mention which incidents helped you.
"""

    response = client.chat.completions.create(
        model=settings.AI_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content