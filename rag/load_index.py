import chromadb

from llama_index.core import (
    VectorStoreIndex
)

from llama_index.vector_stores.chroma import (
    ChromaVectorStore
)

from rag.embedder import (
    get_embed_model
)


def load_index(
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

    return VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=get_embed_model()
    )