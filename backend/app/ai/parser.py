def parse_analysis(text: str):

    data = {}

    current = None

    for line in text.splitlines():

        if line.startswith("Summary:"):
            current = "summary"
            data[current] = line.replace(
                "Summary:",
                "",
            ).strip()

        elif line.startswith("Root Cause:"):
            current = "root_cause"
            data[current] = line.replace(
                "Root Cause:",
                "",
            ).strip()

        elif line.startswith("Suggested Fix:"):
            current = "suggested_fix"
            data[current] = line.replace(
                "Suggested Fix:",
                "",
            ).strip()

        elif line.startswith("Follow-up Actions:"):
            current = "follow_up_actions"
            data[current] = line.replace(
                "Follow-up Actions:",
                "",
            ).strip()

        elif current:
            data[current] += "\n" + line

    return data