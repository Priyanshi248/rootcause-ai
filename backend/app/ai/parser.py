import re


class LogParser:

    ERROR_PATTERN = r"(ERROR.*|Exception.*|Traceback.*)"
    WARNING_PATTERN = r"(WARN.*|WARNING.*)"

    EXCEPTION_PATTERN = (
        r"\b("
        r"NullPointerException|"
        r"IllegalArgumentException|"
        r"RuntimeException|"
        r"IOException|"
        r"SQLException|"
        r"TimeoutException|"
        r"ValueError|"
        r"KeyError|"
        r"TypeError|"
        r"IndexError|"
        r"ConnectionError"
        r")\b"
    )

    HTTP_STATUS_PATTERN = r"\b(400|401|403|404|408|429|500|502|503|504)\b"

    DATABASE_PATTERN = (
        r"(deadlock|"
        r"duplicate key|"
        r"connection refused|"
        r"too many connections|"
        r"connection timeout|"
        r"SQLSTATE.*|"
        r"database.*error)"
    )

    URL_PATTERN = r"(GET|POST|PUT|DELETE|PATCH)\s+(/[A-Za-z0-9_\-/{}]*)"

    STACKTRACE_PATTERN = r"File \".*?\", line \d+.*"

    CONTAINER_PATTERN = (
        r"\b("
        r"postgres|"
        r"redis|"
        r"nginx|"
        r"backend|"
        r"frontend|"
        r"worker|"
        r"rabbitmq|"
        r"kafka|"
        r"mongodb|"
        r"mysql"
        r")\b"
    )

    SERVICE_PATTERN = r"service[:= ]([A-Za-z0-9_-]+)"

    TIMESTAMP_PATTERN = (
        r"\d{4}-\d{2}-\d{2}"
        r"[ T]"
        r"\d{2}:\d{2}:\d{2}"
    )

    @staticmethod
    def _unique(items):

        return sorted(
            set(
                item.strip()
                for item in items
                if item
            )
        )

    @staticmethod
    def parse(
        log_text: str,
    ) -> dict:

        errors = re.findall(
            LogParser.ERROR_PATTERN,
            log_text,
            re.MULTILINE,
        )

        warnings = re.findall(
            LogParser.WARNING_PATTERN,
            log_text,
            re.MULTILINE,
        )

        exceptions = re.findall(
            LogParser.EXCEPTION_PATTERN,
            log_text,
            re.IGNORECASE,
        )

        http_status = re.findall(
            LogParser.HTTP_STATUS_PATTERN,
            log_text,
        )

        database_errors = re.findall(
            LogParser.DATABASE_PATTERN,
            log_text,
            re.IGNORECASE,
        )

        urls = [
            f"{method} {path}"
            for method, path in re.findall(
                LogParser.URL_PATTERN,
                log_text,
            )
        ]

        stack_traces = re.findall(
            LogParser.STACKTRACE_PATTERN,
            log_text,
            re.MULTILINE,
        )

        timestamps = re.findall(
            LogParser.TIMESTAMP_PATTERN,
            log_text,
        )

        services = re.findall(
            LogParser.SERVICE_PATTERN,
            log_text,
            re.IGNORECASE,
        )

        containers = re.findall(
            LogParser.CONTAINER_PATTERN,
            log_text,
            re.IGNORECASE,
        )

        return {

            "errors":
                LogParser._unique(errors),

            "warnings":
                LogParser._unique(warnings),

            "exceptions":
                LogParser._unique(exceptions),

            "http_status":
                LogParser._unique(http_status),

            "database_errors":
                LogParser._unique(database_errors),

            "services":
                LogParser._unique(services),

            "containers":
                LogParser._unique(containers),

            "urls":
                LogParser._unique(urls),

            "stack_traces":
                LogParser._unique(stack_traces),

            "timestamps":
                LogParser._unique(timestamps),
        }