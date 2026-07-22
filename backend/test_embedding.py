from app.vectorstore.embedding_service import create_embedding

embedding = create_embedding(
    "Database connection timeout"
)

print(type(embedding))
print(len(embedding))
print(embedding[:5])