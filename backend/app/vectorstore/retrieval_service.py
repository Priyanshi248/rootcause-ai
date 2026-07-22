from app.vectorstore.chroma_client import collection
from app.vectorstore.embedding_service import create_embedding


class RetrievalService:

    def add_incident(
        self,
        incident_id,
        title,
        description,
        service_name,
    ):

        document = f"""
Title:
{title}

Service:
{service_name}

Description:
{description}
"""

        embedding = create_embedding(
            document
        )

        collection.add(
            ids=[str(incident_id)],
            embeddings=[embedding],
            documents=[document],
            metadatas=[
                {
                    "service": service_name,
                    "title": title,
                }
            ],
        )

    def update_incident_knowledge(
        self,
        incident_id,
        title,
        description,
        service_name,
        summary,
        root_cause,
        suggested_fix,
        follow_up_actions,
    ):

        document = f"""
    Title:
    {title}

    Service:
    {service_name}

    Description:
    {description}

    Summary:
    {summary}

    Root Cause:
    {root_cause}

    Suggested Fix:
    {suggested_fix}

    Follow Up:
    {follow_up_actions}
    """

        embedding = create_embedding(document)

        collection.update(
            ids=[str(incident_id)],
            embeddings=[embedding],
            documents=[document],
            metadatas=[
                {
                    "title": title,
                    "service": service_name,
                    "has_analysis": True,
                }
            ],
        )

    def search(
        self,
        query,
        n_results=5,
    ):

        embedding = create_embedding(
            query
        )

        results = collection.query(
            query_embeddings=[
                embedding
            ],
            n_results=n_results,
        )

        return results["documents"][0]