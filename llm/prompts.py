def rag_prompt(
    context,
    question
):

    return f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
say:

"I couldn't find that information in the uploaded sources."

Context:
{context}

Question:
{question}
"""


def notes_prompt(
    context
):

    return f"""
Create structured revision notes.

CONTENT:
{context}

FORMAT:

# Topic Overview

Brief explanation.

# Key Concepts

- Concept 1
- Concept 2
- Concept 3

# Important Points

- Point 1
- Point 2
- Point 3

# Quick Revision

Provide a 5-line revision summary.

Use markdown formatting.
"""
def mcq_prompt(
    context
):

    return f"""
Generate 10 high-quality MCQs.

CONTENT:
{context}

FORMAT:

## Question 1

Question text

A. Option

B. Option

C. Option

D. Option

✅ Answer: B

📖 Explanation:
Short explanation.

Repeat for all 10 questions.

Use markdown.
"""


def flashcard_prompt(
    context
):

    return f"""
Create flashcards from the content.

CONTENT:
{context}

FORMAT:

## Flashcard 1

Q: Question

A: Answer

---

## Flashcard 2

Q: Question

A: Answer

Generate at least 15 flashcards.

Use markdown.
"""

def interview_prompt(
    context
):

    return f"""
Generate interview questions and answers.

CONTENT:
{context}

FORMAT:

## Question 1

Question

### Answer

Detailed answer.

### Follow Up

Possible follow-up question.

Generate 10 interview questions.

Use markdown formatting.
"""