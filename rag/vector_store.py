import chromadb

from llama_index.core import (
    VectorStoreIndex,
    StorageContext
)

from llama_index.vector_stores.chroma import (
    ChromaVectorStore
)

from rag.embedder import (
    get_embed_model
)


def create_index(
    documents,
    collection_name
):

    client = chromadb.PersistentClient(
        path="data/chroma_db"
    )

    collection = (
        client.get_or_create_collection(
            collection_name
        )
    )

    vector_store = (
        ChromaVectorStore(
            chroma_collection=collection
        )
    )

    storage_context = (
        StorageContext.from_defaults(
            vector_store=vector_store
        )
    )

    return VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=get_embed_model()
    )