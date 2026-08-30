from app.vectorstore.retrieval_service import RetrievalService


print("==============================")
print("RAG SIMILARITY SEARCH TEST")
print("==============================")

retrieval = RetrievalService()

query = """
API Gateway Redis connection timeout.
Redis connection pool exhausted.
Requests are returning HTTP 502 errors.
"""

print("\nQUERY:")
print(query)

results = retrieval.search(
    query,
    n_results=5,
)

print("\n==============================")
print("RESULTS")
print("==============================")

print("Number of results:", len(results))

for i, result in enumerate(results, start=1):

    print("\n------------------------------")
    print(f"RESULT {i}")
    print("------------------------------")

    print(result)