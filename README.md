# 🏦 HCLTech Financial Intelligence — RAG

> An AI-powered financial research assistant for analyzing HCLTech quarterly financial reports using Retrieval-Augmented Generation (RAG).

---

## 📌 Overview

**HCLTech Financial Intelligence** is a Retrieval-Augmented Generation (RAG) application that answers financial questions using HCLTech's quarterly financial reports.

The application retrieves relevant information from uploaded PDF documents using **ChromaDB** and generates grounded answers using **Llama 3.1 8B** running locally through **Ollama**.

The system is designed to:

- 🔍 Answer questions using uploaded financial reports
- 📊 Compare financial metrics across quarters
- 📄 Provide source PDF and page references
- 🛡️ Reduce hallucinations through strict grounding
- 🤖 Run the LLM locally without an external API key
- 🖥️ Provide an interactive Streamlit interface

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔎 RAG | Retrieves relevant financial information before generating answers |
| 🧠 Local LLM | Uses Llama 3.1 8B through Ollama |
| 🧩 Embeddings | Uses `nomic-embed-text` |
| 🗄️ Vector Database | ChromaDB for document retrieval |
| 📄 Citations | Displays source PDF and page number |
| 📊 Comparisons | Supports quarterly financial comparisons |
| 🛡️ Guardrails | Refuses unsupported questions |
| 🖥️ UI | Interactive Streamlit dashboard |

---

## 🛠️ Technology Stack

- **Python**
- **Streamlit**
- **ChromaDB**
- **Ollama**
- **Llama 3.1 8B**
- **nomic-embed-text**
- **PyPDF**

---

## 🏗️ System Architecture

```text
             HCLTech Quarterly Reports
                       │
                       ▼
                PDF Extraction
                       │
                       ▼
                  Text Chunking
                       │
                       ▼
             nomic-embed-text
                  Embeddings
                       │
                       ▼
                   ChromaDB
                Vector Storage
                       │
                       ▼
                  User Query
                       │
                       ▼
              Query Embedding
                       │
                       ▼
              Relevant Chunks
                  Retrieved
                       │
                       ▼
                Llama 3.1 8B
                       │
                       ▼
              Grounded Answer
                       │
                       ▼
             📄 Source + Page
```

---

## 📂 Project Structure

```text
HCLTech-Financial-RAG/
│
├── 📄 app.py
├── 📄 rag.py
├── 📄 ingest.py
├── 📄 requirements.txt
├── 📄 README.md
├── 📄 LICENSE
├── 📄 .gitignore
│
└── 📁 data/
    ├── Q1.pdf
    ├── Q2.pdf
    ├── Q3.pdf
    └── Q4.pdf
```

---

## ⚙️ How It Works

### 1️⃣ Document Ingestion

The quarterly HCLTech reports are placed inside the `data/` folder.

`ingest.py`:

- Extracts text from PDFs
- Splits the content into chunks
- Generates embeddings
- Stores embeddings and metadata in ChromaDB

### 2️⃣ Query Processing

When a user enters a financial question:

```text
User Question
      ↓
Embedding Generation
      ↓
ChromaDB Similarity Search
      ↓
Relevant Financial Chunks
```

### 3️⃣ Answer Generation

The retrieved context is provided to Llama 3.1 8B.

The model is instructed to:

- Use only retrieved information
- Avoid outside knowledge
- Avoid inventing financial values
- Identify the source and page
- Refuse unsupported questions

---

# 🚀 Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/Sarvesh-0206/HCLTech-Financial-RAG.git
cd HCLTech-Financial-RAG
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```powershell
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🤖 Ollama Setup

This project uses **Ollama** for local AI inference.

No external LLM API key is required.

### Pull Llama 3.1

```bash
ollama pull llama3.1:8b
```

### Pull Embedding Model

```bash
ollama pull nomic-embed-text
```

### Start Ollama

```bash
ollama serve
```

---

# 📚 Build the Vector Database

Place the quarterly reports inside:

```text
data/
├── Q1.pdf
├── Q2.pdf
├── Q3.pdf
└── Q4.pdf
```

Run:

```bash
python ingest.py
```

The documents are processed and stored in ChromaDB.

---

# 🖥️ Run the Application

Start Streamlit:

```bash
python -m streamlit run app.py
```

The application will open in your browser.

---

# 📊 Evaluation Questions

The following questions were used to evaluate the financial RAG application.

---

## 1. Total Revenue

### Question

> What was HCLTech's total revenue in Q4 FY2025-26?

### Application Answer

> The total revenue in Q4 FY2025-26 was **₹33,981 crores**.

📄 **Source:** `Q4.pdf` — Page 3

---

## 2. Net Profit Comparison

### Question

> Compare HCLTech's net profit across Q1-Q4 FY2025-26. Which quarter was highest?

### Application Answer

> Q1 FY2025-26: ₹3,844 crores  
> Q2 FY2025-26: ₹4,309 crores  
> Q3 FY2025-26: ₹4,259 crores  
> Q4 FY2025-26: ₹4,490 crores  
>
> The highest net profit was in **Q4 FY2025-26**, at **₹4,490 crores**.

📄 **Sources:** Q1.pdf, Q3.pdf, Q4.pdf

---

## 3. Latest Quarter vs Previous Year

### Question

> How did HCLTech's revenue in Q4 FY2025-26 compare with Q4 FY2024-25?

### Application Answer

> The total revenue for Q4 FY2025-26 is 33,981 crores and for Q4 FY2024-25 is 30,246 crores.
To calculate the growth percentage: ((33,981 - 30,246) / 30,246) × 100 = (3,735 / 30,246) × 100 = 12.35%
Therefore, HCLTech's revenue in Q4 FY2025-26 compared to Q4 FY2024-25 grew by 12.35%.

📄 **Source:** `Q4.pdf`
<img width="1497" height="819" alt="image" src="https://github.com/user-attachments/assets/60952558-22e9-440f-baa4-c0f23a4e4452" />

---

## 4. Management Outlook

### Question

> What did HCLTech management say about the demand outlook or business environment?

### Application Answer

> The information is not available in the uploaded documents.

📄 **Source:** HCLTech quarterly reports

---

## 5. Fastest-Growing Segment

### Question

> Which HCLTech business segment grew fastest in Q4 FY2025-26, and by how much compared with Q4 FY2024-25?

### Application Answer

> IT and Business Services: 14.66%
> Engineering and R&D Services: 12.08%
> HCL Software: -5.02%

📄 **Source:** `Q4.pdf`

---

## 6. Operating Margin

### Question

> What was HCLTech's operating margin in each quarter of FY2025-26, and is the trend rising or falling?

### Application Answer

> Based on the provided context, I'll answer your question about HCLTech's operating margin in each quarter of FY2025-26. Unfortunately, the operating margin for each quarter is not explicitly mentioned in the context. However, the provided tables show the profit before tax and tax expense for each quarter. To calculate the operating margin, we need the operating profit (which is not directly available) and the revenue. Since the revenue for Q1, Q2, and Q3 FY2025-26 is not provided, I'll focus on the information available for Q4 FY2025-26 and Q4 FY2024-25. From the tables, we can see the operating profit for Q4 FY2025-26 and Q4 FY2024-25:

Q4 FY2025-26: Profit before tax (5,702) and tax expense (1,466) = Operating profit = 4,236 Q4 FY2024-25: Profit before tax (5,687) and tax expense (1,450) = Operating profit = 4,237
📄 **Sources:** Q1.pdf, Q2.pdf, Q3.pdf, Q4.pdf

---

## 7. Dividend

### Question

> Was any dividend declared? State the amount per share and the record date.

### Application Answer

> The Board of Directors at its meeting held on 21 April 2026 has declared an interim dividend of 124 per share. The record date for the payment of the aforesaid interim dividend shall be April 25, 2026.

📄 **Source:** HCLTech quarterly reports

---

## 8. Risks & Challenges

### Question

> What risks, headwinds, or challenges are mentioned in the HCLTech financial documents?

### Application Answer

> Based on the provided context, there are no mentions of risks, headwinds, or challenges in HCLTech's quarterly documents. The context only contains information about the company's financial results and segment revenues, but does not mention any potential risks or challenges.



📄 **Sources:** HCLTech quarterly reports

---

## 9. Client Email Summary

### Question

> Give me a three-line summary of the latest quarter for a client email.

### Application Answer

> Here is a three-line summary of HCLTech's Q4 FY2025-26: HCLTech's Q4 FY2025-26 revenue from external customers was ₹33,981 crore. Segment revenues for IT and Business Services were ₹25,443 crore. HCL Software segment revenue was ₹2,857 crore.

---

# 🛡️ 10. Deliberate Trap Question

### Question

> What is the CEO's personal shareholding in 2015?

### Expected Behaviour

The requested information is **not contained in the uploaded documents**.

The application should therefore **not invent a number**.

### Application Answer

> The information is not available in the uploaded documents.

This demonstrates the application's hallucination-prevention behaviour.


<img width="1791" height="880" alt="image" src="https://github.com/user-attachments/assets/685fb58b-4af5-46d5-a300-ec759373bd4a" />

---

# 🛡️ Hallucination Prevention

The application uses strict grounding instructions for the LLM.

The model is instructed to:

1. Use only information contained in the retrieved context.
2. Never invent financial numbers or facts.
3. Never use outside knowledge.
4. Refuse questions when the required information is unavailable.
5. Provide source file and page information.
6. Clearly identify quarters during financial comparisons.

The deliberate trap question demonstrates the application's ability to refuse unsupported requests rather than hallucinating an answer.

---

# 🗃️ Source Metadata

Each retrieved document chunk contains metadata such as:

```text
source
page
quarter
```

This metadata is used to associate retrieved information with the original financial report.

---

# 🧠 Local AI Implementation

### Language Model

```text
Llama 3.1 8B
```

### Embedding Model

```text
nomic-embed-text
```

### Vector Database

```text
ChromaDB
```

### Interface

```text
Streamlit
```

The complete AI pipeline can run locally without requiring an external LLM API key.

---

# 🔐 Security

No API keys or secrets are required for the local Ollama implementation.

Sensitive files and generated vector databases should not be committed to the repository.

The `.gitignore` file excludes local environment files and generated data.

---

# 📌 Limitations

- The quality of answers depends on the retrieved document chunks.
- Complex financial tables can sometimes be difficult for a small local LLM to interpret correctly.
- Arithmetic-heavy comparisons may require additional deterministic calculation logic.
- The system only knows information contained in the uploaded quarterly reports.
- It does not use external financial databases or live market information.

---

# 🎯 Conclusion

**HCLTech Financial Intelligence** demonstrates how Retrieval-Augmented Generation can be applied to financial document analysis.

The project combines:

**PDF Processing → Embeddings → Vector Search → Local LLM → Grounded Financial Answers → Source Attribution**

The goal is to provide a transparent and auditable financial research assistant while reducing unsupported or hallucinated answers.

---

## 👨‍💻 Author

**Sarvesh B.V.**

Electronics & Communication Engineering  
RMK Engineering College

---

## 🔗 Repository

[GitHub Repository](https://github.com/Sarvesh-0206/HCLTech-Financial-RAG)
