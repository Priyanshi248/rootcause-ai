import json
from app.core.config import settings
from app.agents.gemini_client import client
from app.agents.prompts import ROOT_CAUSE_PROMPT


async def analyze_logs(logs: str):

    prompt = ROOT_CAUSE_PROMPT.format(
        logs=logs
    )

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)