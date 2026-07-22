from app.vectorstore.retrieval_service import RetrievalService

retrieval = RetrievalService()

results = retrieval.search(
    "postgres database timeout"
)

results = retrieval_service.search(query)

print(f"\nFound {len(results)} similar incidents:\n")

for i, result in enumerate(results, 1):
    print(f"========== Incident {i} ==========")
    print(result)
    print()