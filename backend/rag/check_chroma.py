from .vector_store import create_vector_store


vector_store = create_vector_store()

data = vector_store.get()

print("Number of documents:", len(data["ids"]))

for i in range(len(data["ids"])):

    print("\n" + "=" * 60)

    print("ID:")
    print(data["ids"][i])

    print("\nDOCUMENT:")
    print(data["documents"][i])

    print("\nMETADATA:")
    print(data["metadatas"][i])