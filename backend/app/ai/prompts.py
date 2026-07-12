ROOT_CAUSE_PROMPT = """
You are an expert Site Reliability Engineer.

Analyze the following logs.

Return your answer in exactly this format.

Summary:
...

Root Cause:
...

Suggested Fix:
...

Follow_up_actions: [
    "...",
    "...",
    "...",
    "..."
  ]

Logs:

{logs}
"""