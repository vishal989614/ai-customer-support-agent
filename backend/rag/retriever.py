from .embeddings import get_embedding_model
from langchain_chroma import Chroma


CHROMA_PATH = "../chroma_db"


def get_vector_store():

    embedding_model = get_embedding_model()

    return Chroma(
        collection_name="support_knowledge",
        embedding_function=embedding_model,
        persist_directory=CHROMA_PATH
    )


def search_knowledge(query: str, k: int = 3):

    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        query,
        k=k
    )

    return results