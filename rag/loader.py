from llama_index.core import (
    SimpleDirectoryReader
)


def load_documents():

    documents = SimpleDirectoryReader(
        "data/uploads"
    ).load_data()

    return documents