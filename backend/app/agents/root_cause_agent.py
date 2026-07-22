import json

from app.agents.ai_client import client
from app.agents.prompts import ROOT_CAUSE_PROMPT
from app.core.config import settings


async def analyze_logs(
    logs: str,
    context: str,
):

    prompt = ROOT_CAUSE_PROMPT.format(
        logs=logs,
        context=context,
    )

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

    text = response.choices[0].message.content.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)