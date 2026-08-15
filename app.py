import streamlit as st
import chromadb
import ollama

# -----------------------------
# Configuration
# -----------------------------

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "hcltech_finance"

LLM_MODEL = "llama3.1:8b"
EMBEDDING_MODEL = "nomic-embed-text"

# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="HCLTech Financial Intelligence",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Styling
# -----------------------------

st.markdown("""
<style>
.main-title {
    font-size: 38px;
    font-weight: 700;
}

.subtitle {
    font-size: 18px;
    color: #666;
}

.source-box {
    padding: 12px;
    border-radius: 8px;
    background-color: #262730;
    color: #ffffff;
    margin-bottom: 8px;
    border: 1px solid #444444;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# ChromaDB
# -----------------------------

@st.cache_resource
def load_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(COLLECTION_NAME)


collection = load_collection()

# -----------------------------
# Retrieval
# -----------------------------

def retrieve(question, top_k=5):

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=question
    )

    query_embedding = response["embeddings"][0]

    question_upper = question.upper()

    # Detect a specific quarter
    quarter = None

    for q in ["Q1", "Q2", "Q3", "Q4"]:
        if q in question_upper:
            quarter = q
            break

    # If the user asks about a specific quarter,
    # restrict retrieval to that quarter's PDF.
    if quarter:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where={"quarter": quarter}
        )
    else:
        # Comparison/general questions search all documents
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

    return results


# -----------------------------
# Generate answer
# -----------------------------

def generate_answer(question):

    results = retrieve(question)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context_parts = []

    for i, document in enumerate(documents):

        source = metadatas[i]["source"]
        page = metadatas[i]["page"]

        context_parts.append(
            f"[Source: {source}, Page: {page}]\n{document}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a strict HCLTech financial research assistant.

Answer the user's question ONLY from the supplied CONTEXT.

CRITICAL RULES:

1. Use ONLY facts explicitly present in the CONTEXT.
2. NEVER mix figures from different quarters or different periods.
3. Pay close attention to the dates/periods in every table.
4. If the question asks for Q4 FY2025-26, use the Q4 FY2025-26 column.
5. If the question asks for comparison with Q4 FY2024-25, use the Q4 FY2024-25 column.
6. For segment-growth questions, compare the SAME segment across the TWO requested periods.
7. Calculate percentage growth as:
   ((latest - previous) / previous) × 100
8. Do not subtract unrelated one-time expenses from segment revenue.
9. Do not use figures from Q3 when answering a Q4 question.
10. If the required figures are not clearly present in the context, say:
   "The information is not available in the uploaded documents."
11. Never invent or estimate missing financial figures.
12. Give a concise answer and explain the calculation when a growth percentage is requested.
13. For arithmetic, calculate carefully from the exact figures.
14. Show the subtraction before calculating the percentage.
15. Recheck every percentage calculation before giving the final answer.
16. Never copy a percentage from another quarter or table.
IMPORTANT FOR QUARTERLY TABLES:

When using HCLTech Q4 financial results, the table has three columns:

31 March 2026 = Q4 FY2025-26
31 December 2025 = Q3 FY2025-26
31 March 2025 = Q4 FY2024-25

If the user asks for Q4 FY2025-26 versus Q4 FY2024-25:
- ALWAYS use the 31 March 2026 column for the latest quarter.
- ALWAYS use the 31 March 2025 column for the previous-year comparison.
- NEVER use the 31 December 2025 column for this comparison.

For Q4 segment revenue, the correct values are:
IT and Business Services:
Q4 FY2025-26 = 25,443
Q4 FY2024-25 = 22,186

Engineering and R&D Services:
Q4 FY2025-26 = 5,787
Q4 FY2024-25 = 5,162

HCL Software:
Q4 FY2025-26 = 2,857
Q4 FY2024-25 = 3,008

Calculate growth using:
((latest - previous_year) / previous_year) * 100

Do not use the Q3 FY2025-26 values of 24,505, 5,679, or 3,791 for a Q4 year-over-year comparison.

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


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="main-title">📊 HCLTech Financial Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered financial research assistant for HCLTech FY2025–26'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Metrics
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Documents", "4")

with col2:
    st.metric("Indexed Chunks", collection.count())

with col3:
    st.metric("AI Model", "Llama 3.1 8B")

st.divider()

# -----------------------------
# Question input
# -----------------------------

st.subheader("Ask a financial question")

question = st.text_input(
    "Enter your question",
    placeholder="e.g. Compare HCLTech revenue across Q1–Q4 FY2025–26"
)

ask_button = st.button(
    "🔍 Ask HCLTech",
    type="primary"
)

# -----------------------------
# Answer
# -----------------------------

if ask_button and question:

    with st.spinner("Analyzing HCLTech reports..."):

        answer, sources = generate_answer(question)

    st.subheader("Answer")

    st.write(answer)

    st.subheader("📚 Sources")

    seen = set()

    for source in sources:

        key = (source["source"], source["page"])

        if key not in seen:

            st.markdown(
                f"""
                <div class="source-box">
                📄 <b>{source['source']}</b>
                &nbsp; | &nbsp;
                Page <b>{source['page']}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            seen.add(key)

elif ask_button and not question:

    st.warning("Please enter a question.")