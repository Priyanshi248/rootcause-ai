from app.models import (
    Incident,
    Log,
    Analysis,
    TimelineEvent,
    User,
    AuditLog,
)


def test_models_import():

    assert Incident is not None
    assert Log is not None
    assert Analysis is not None
    assert TimelineEvent is not None
    assert User is not None
    assert AuditLog is not None