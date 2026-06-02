from llm.groq_client import (
    get_response
)

from llm.prompts import (
    notes_prompt,
    mcq_prompt,
    flashcard_prompt,
    interview_prompt
)


def generate_study_material(
    index,
    topic,
    mode
):

    retriever = (
        index.as_retriever(
            similarity_top_k=5
        )
    )

    nodes = (
        retriever.retrieve(
            topic
        )
    )

    context = "\n\n".join(
        node.text
        for node in nodes
    )

    if mode == "Notes":

        prompt = notes_prompt(
            context
        )

    elif mode == "MCQs":

        prompt = mcq_prompt(
            context
        )

    elif mode == "Flashcards":

        prompt = flashcard_prompt(
            context
        )

    else:

        prompt = interview_prompt(
            context
        )

    return get_response(
        prompt
    )