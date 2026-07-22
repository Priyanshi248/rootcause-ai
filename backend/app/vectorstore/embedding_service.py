from fastembed import TextEmbedding

# Load the model only once when the application starts
embedding_model = TextEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)


def create_embedding(text: str) -> list[float]:
    """
    Generate embeddings for a piece of text.
    """

    embedding = next(embedding_model.embed([text]))

    return embedding.tolist()