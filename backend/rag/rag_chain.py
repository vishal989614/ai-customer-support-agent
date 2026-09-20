from .retriever import search_knowledge
from .llm import generate_answer
from .prompts import RAG_PROMPT


def answer_question(
    question: str,
    k: int = 3
) -> str:

    # 1. Retrieve relevant documents
    documents = search_knowledge(
        question,
        k=k
    )

    # 2. Convert documents into context
    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # 3. Create prompt
    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    # 4. Ask LLM
    answer = generate_answer(prompt)

    return answer