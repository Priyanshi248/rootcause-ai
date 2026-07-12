from google.genai import types

from app.ai.gemini_client import client
from app.ai.prompts import ROOT_CAUSE_PROMPT


async def analyze_logs(logs: str):

    prompt = ROOT_CAUSE_PROMPT.format(
        logs=logs
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
        ),
    )

    return response.text