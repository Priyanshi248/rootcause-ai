from fastembed import TextEmbedding

embedding_model = TextEmbedding()

text = "Database connection timeout while connecting to PostgreSQL"

embedding = next(embedding_model.embed([text]))

print(type(embedding))
print(len(embedding))
print(embedding[:10])