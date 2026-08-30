import json

from app.agents.ai_client import generate_response
from app.agents.prompts import ROOT_CAUSE_PROMPT


async def analyze_logs(
    logs: str,
    context: str,
    parsed_logs: dict,
):

    prompt = ROOT_CAUSE_PROMPT.format(
        logs=logs,
        context=context,

        errors="\n".join(
            parsed_logs.get("errors", [])
        ),

        warnings="\n".join(
            parsed_logs.get("warnings", [])
        ),

        exceptions="\n".join(
            parsed_logs.get("exceptions", [])
        ),

        http_status="\n".join(
            parsed_logs.get("http_status", [])
        ),

        database_errors="\n".join(
            parsed_logs.get("database_errors", [])
        ),

        services=", ".join(
            parsed_logs.get("services", [])
        ),

        containers=", ".join(
            parsed_logs.get("containers", [])
        ),

        urls="\n".join(
            parsed_logs.get("urls", [])
        ),

        stack_traces="\n".join(
            parsed_logs.get("stack_traces", [])
        ),

        timestamps=", ".join(
            parsed_logs.get("timestamps", [])
        ),
    )

    text = generate_response(
        prompt,
        temperature=0.2,
    )

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)
        text = text.replace("```", "", 1)
        text = text.strip()

    return json.loads(text)