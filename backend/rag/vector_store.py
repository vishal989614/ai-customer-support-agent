import os

from langchain_chroma import Chroma
from langchain_core.documents import Document

from .documents import SUPPORT_DOCUMENTS
from .embeddings import get_embedding_model

CHROMA_PATH = "../chroma_db"


def create_vector_store():
    embedding_model = get_embedding_model()

    vector_store = Chroma(
        collection_name="support_knowledge",
        embedding_function=embedding_model,
        persist_directory=CHROMA_PATH
    )

    existing_ids = vector_store.get()["ids"]

    documents = []
    ids = []

    for item in SUPPORT_DOCUMENTS:

        if item["id"] in existing_ids:
            continue

        documents.append(
            Document(
                page_content=item["content"],
                metadata={
                    "title": item["title"],
                    "document_id": item["id"]
                }
            )
        )

        ids.append(item["id"])

    if documents:
        vector_store.add_documents(
            documents=documents,
            ids=ids
        )

    return vector_store