from openai import OpenAI

from app.core.config import settings

client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)


def generate_response(
    prompt: str,
    temperature: float = 0.2,
):

    response = client.chat.completions.create(
        model=settings.AI_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=temperature,
    )

    return response.choices[0].message.content