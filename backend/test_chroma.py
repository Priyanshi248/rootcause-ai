from app.vectorstore.retrieval_service import RetrievalService


def test_retrieval_service_creation():

    retrieval_service = RetrievalService()

    assert retrieval_service is not None