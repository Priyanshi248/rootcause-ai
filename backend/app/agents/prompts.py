ROOT_CAUSE_PROMPT = """
You are a Senior Site Reliability Engineer.

Analyze the following production logs.

Return ONLY valid JSON.

Format:

{{
    "summary": "...",
    "root_cause": "...",
    "suggested_fix": "...",
    "follow_up_actions": "..."
}}

Logs:

{logs}
"""