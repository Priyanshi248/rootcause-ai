from app.agents.chat_agent import ask_question
from app.vectorstore.retrieval_service import RetrievalService


class AIService:

    def __init__(self):

        self.retrieval = RetrievalService()

    async def chat(
        self,
        question: str,
    ):

        similar = self.retrieval.search(
            question
        )

        context = "\n\n".join(
            similar
        )

        answer = await ask_question(
            context,
            question,
        )

        return {
            "response": answer,
            "sources": similar,
        }