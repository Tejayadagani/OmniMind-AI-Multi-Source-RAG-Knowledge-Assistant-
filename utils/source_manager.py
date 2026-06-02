from llama_index.core import (
    Document
)

from rag.vector_store import (
    create_index
)


def add_text_to_kb(
    text,
    source_type,
    source_name
):

    document = Document(

        text=text,

        metadata={

            "source_type": source_type,

            "source_name": source_name

        }
    )

    create_index(
        [document],
        source_type
    )