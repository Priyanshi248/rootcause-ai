from app.ai.response_parser import AIResponseParser


def test_valid_json():

    text = """
    {
        "summary": "Database failure",
        "root_cause": "Connection pool exhausted"
    }
    """

    result = AIResponseParser.parse(text)

    assert result["summary"] == "Database failure"
    assert result["root_cause"] == "Connection pool exhausted"


def test_markdown_json():

    text = """
    ```json
    {
        "summary": "Database failure",
        "root_cause": "Connection pool exhausted"
    }
    ```
    """

    result = AIResponseParser.parse(text)

    assert result["summary"] == "Database failure"