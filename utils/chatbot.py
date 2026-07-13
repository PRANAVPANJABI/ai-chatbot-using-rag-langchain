from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="""
You are a helpful AI assistant.

Answer the user's question ONLY using the provided context.

If the answer is not present in the context, reply:
"I couldn't find this information in the uploaded PDF."

Context:
{context}

Question:
{question}

Answer:
""",
    input_variables=["context", "question"]
)


def ask_pdf(question, retriever, client):
    """
    Retrieves relevant document chunks and generates
    an answer using Google Gemini.
    """

    # Retrieve relevant chunks
    results = retriever.invoke(question)

    # If no relevant chunks are found
    if not results:
        return "I couldn't find this information in the uploaded PDF."

    # Combine retrieved chunks into one context
    context = "\n\n".join(
        doc.page_content for doc in results
    )

    # Create the final prompt
    final_prompt = prompt.format(
        context=context,
        question=question
    )

    # Generate answer using Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=final_prompt
    )

    return response.text