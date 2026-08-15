import chromadb
import ollama

CHROMA_DIR = "chroma_db"

LLM_MODEL = "llama3.1:8b"
EMBEDDING_MODEL = "nomic-embed-text"

# Connect to persistent ChromaDB
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection("hcltech_finance")


def embed_query(question):
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=question
    )
    return response["embeddings"][0]


def retrieve(question, top_k=5):

    quarter_queries = {
        "Q1": (
            "Q1 FY2025-26 profit for the period",
            "Q1.pdf"
        ),
        "Q2": (
            "Q2 FY2025-26 profit for the period",
            "Q2.pdf"
        ),
        "Q3": (
            "Q3 FY2025-26 profit for the period",
            "Q3.pdf"
        ),
        "Q4": (
            "Q4 FY2025-26 profit for the period",
            "Q4.pdf"
        )
    }

    all_documents = []
    all_metadatas = []

    # Multi-quarter comparison
    if all(q in question for q in ["Q1", "Q2", "Q3", "Q4"]):

        for quarter, (query, pdf) in quarter_queries.items():

            response = ollama.embed(
                model=EMBEDDING_MODEL,
                input=query
            )

            query_embedding = response["embeddings"][0]

            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where={"source": pdf}
            )

            all_documents.extend(results["documents"][0])
            all_metadatas.extend(results["metadatas"][0])

    else:
        # Normal single-question retrieval
        response = ollama.embed(
            model=EMBEDDING_MODEL,
            input=question
        )

        query_embedding = response["embeddings"][0]

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        all_documents.extend(results["documents"][0])
        all_metadatas.extend(results["metadatas"][0])

    # Remove duplicate pages
    seen = set()
    documents = []
    metadatas = []

    for doc, meta in zip(all_documents, all_metadatas):

        key = (meta["source"], meta["page"])

        if key not in seen:
            seen.add(key)
            documents.append(doc)
            metadatas.append(meta)

    return {
        "documents": [documents],
        "metadatas": [metadatas]
    }


def ask_question(question):
    results = retrieve(question)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # Build context
    context_parts = []

    for i, document in enumerate(documents):
        source = metadatas[i]["source"]
        page = metadatas[i]["page"]

        context_parts.append(
            f"[Source: {source}, Page: {page}]\n{document}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an HCLTech financial research assistant.

Answer the user's question ONLY using the information
provided in the context below.

IMPORTANT RULES:

1. Use ONLY information in the CONTEXT.
2. Never invent numbers.
3. Never mix financial periods or columns.
4. "Q1 FY2025-26" means the three-month quarter ended June 30, 2025.
5. "Q2 FY2025-26" means the three-month quarter ended September 30, 2025.
6. "Q3 FY2025-26" means the three-month quarter ended December 31, 2025.
7. "Q4 FY2025-26" means the three-month quarter ended March 31, 2026.

8. When a table contains multiple columns such as:
   - current quarter
   - previous quarter
   - same quarter previous year
   - year-to-date
   - previous year
   ALWAYS select the column corresponding to the requested quarter.

9. For Q1-Q4 FY2025-26 net profit comparison, use:
   "Profit for the period" for the THREE-MONTH quarter,
   NOT nine-month/year-to-date figures.

10. Do NOT use a previous-year figure when answering the current-year quarter.

11. For Q3 FY2025-26 specifically:
    use the 31 December 2025 three-month value.
    Do NOT use the 31 December 2024 value.

12. For Q2 FY2025-26 specifically:
    use the 30 September 2025 three-month value.
    Do NOT use the six-month/year-to-date value.

13. If the required quarter/value cannot be identified unambiguously,
    say:
    "The information is not available in the uploaded documents."

14. For comparisons, list each quarter and value before deciding
    which is highest.

15. Cite the source file and page for each figure.
16. NEVER assign a financial value to a quarter unless the
    retrieved source explicitly supports that quarter.

17. The source file name alone does not determine the quarter.
    Verify the reporting date and financial-period column.

18. If a source says "three months ended September 30, 2025",
    treat it as Q2 FY2025-26.

19. If a source says "three months ended December 31, 2025",
    treat it as Q3 FY2025-26.

20. If retrieved sources conflict, do not guess. State that
    the information is ambiguous or unavailable.

USER QUESTION:
{question}

CONTEXT:
{context}

ANSWER:
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    return answer, metadatas


if __name__ == "__main__":
    question = input("\nAsk an HCLTech question: ")

    answer, sources = ask_question(question)

    print("\n================ ANSWER ================\n")
    print(answer)

    print("\n================ SOURCES ================\n")

    seen = set()

    for source in sources:
        key = (source["source"], source["page"])

        if key not in seen:
            print(f"- {source['source']} — Page {source['page']}")
            seen.add(key)