import hashlib
from pathlib import Path

import chromadb
import ollama
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Paths
DATA_DIR = Path("data")
CHROMA_DIR = Path("chroma_db")

# Ollama models
EMBEDDING_MODEL = "nomic-embed-text"

# ChromaDB
chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

# Remove old collection if it exists
try:
    chroma_client.delete_collection("hcltech_finance")
except Exception:
    pass

collection = chroma_client.create_collection(
    name="hcltech_finance"
)

# Assignment requirement:
# chunk size 800–1200 characters
# overlap 100–200 characters
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)


def get_chunks():
    documents = []
    metadatas = []
    ids = []

    for pdf_path in sorted(DATA_DIR.glob("*.pdf")):
        print(f"Reading: {pdf_path.name}")

        reader = PdfReader(str(pdf_path))

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()

            if not text or not text.strip():
                continue

            chunks = splitter.split_text(text)

            for chunk_number, chunk in enumerate(chunks):
                chunk = chunk.strip()

                if not chunk:
                    continue

                doc_id = hashlib.md5(
                    f"{pdf_path.name}-{page_number}-{chunk_number}".encode()
                ).hexdigest()

                documents.append(chunk)

                metadatas.append({
                    "source": pdf_path.name,
                    "page": page_number,
                    "quarter": pdf_path.stem
                })

                ids.append(doc_id)

    return documents, metadatas, ids


def create_embeddings(texts):
    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=texts
    )

    return response["embeddings"]


def main():
    documents, metadatas, ids = get_chunks()

    if not documents:
        print("No text found in the PDFs.")
        return

    print(f"\nTotal chunks: {len(documents)}")
    print("Creating Ollama embeddings...")

    batch_size = 50

    for start in range(0, len(documents), batch_size):
        end = min(start + batch_size, len(documents))

        batch_docs = documents[start:end]
        batch_metadata = metadatas[start:end]
        batch_ids = ids[start:end]

        embeddings = create_embeddings(batch_docs)

        collection.add(
            documents=batch_docs,
            metadatas=batch_metadata,
            embeddings=embeddings,
            ids=batch_ids
        )

        print(f"Stored {end}/{len(documents)} chunks")

    print("\n================================")
    print("HCLTech Finance RAG ingestion complete!")
    print(f"Documents: {len(list(DATA_DIR.glob('*.pdf')))}")
    print(f"Chunks stored: {collection.count()}")
    print("Embedding model: nomic-embed-text")
    print("ChromaDB: chroma_db/")
    print("================================")


if __name__ == "__main__":
    main()