from app.vectorstore.chroma_client import collection


print("==============================")
print("RAG / CHROMA TEST")
print("==============================")

print("Collection name:")
print(collection.name)

print("Number of stored documents:")
print(collection.count())

print("\nStored data:")

if collection.count() > 0:

    data = collection.get(
        include=[
            "documents",
            "metadatas",
        ]
    )

    print("IDs:")
    print(data["ids"])

    print("\nDocuments:")

    for document in data["documents"]:
        print("------------------------------")
        print(document)

else:
    print("Chroma collection is EMPTY.")