import os
import pandas as pd
from db_utils import collection 
import openai

# Load dataset
df = pd.read_csv("data/Mental_Health_FAQ.csv")

# Use a small subset to keep the project lightweight
df = df.head(50)

def create_embedding(text: str):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def chunk_text(text, chunk_size=300, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks

def ingest_documents():
    collection.delete_many({})

    for _, row in df.iterrows():
        combined_text = f"Question: {row['Questions']}\nAnswer: {row['Answers']}"

        chunks = chunk_text(combined_text)

        for idx, chunk in enumerate(chunks):
            embedding = create_embedding(chunk)

            document = {
                "question_id": int(row["Question_ID"]),
                "chunk_id": idx,
                "text": chunk,
                "embedding": embedding
            }

            collection.insert_one(document)

    print("Ingestion completed successfully.")

if __name__ == "__main__":
    ingest_documents()
