import json


class AIResponseParser:

    @staticmethod
    def parse(text: str) -> dict:

        text = text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "")

        text = text.replace("```", "")

        start = text.find("{")

        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                "AI did not return JSON."
            )

        cleaned = text[start:end + 1]

        return json.loads(cleaned)