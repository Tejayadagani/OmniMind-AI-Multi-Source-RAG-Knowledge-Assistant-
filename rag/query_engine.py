from llm.groq_client import (
    get_response
)

from llm.prompts import (
    rag_prompt
)


def query_documents(
    index,
    question
):

    retriever = (
        index.as_retriever(
            similarity_top_k=5
        )
    )

    nodes = (
        retriever.retrieve(
            question
        )
    )

    context = "\n\n".join(
        node.text
        for node in nodes
    )

    prompt = rag_prompt(
        context,
        question
    )

    answer = (
        get_response(
            prompt
        )
    )

    return answer, nodes