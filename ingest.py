import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db.documents

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

def ingest_documents():
    collection.delete_many({})  # Clean previous data (for development)

    for _, row in df.iterrows():
        combined_text = f"Question: {row['Questions']}\nAnswer: {row['Answers']}"

        embedding = create_embedding(combined_text)

        document = {
            "question_id": int(row["Question_ID"]),
            "text": combined_text,
            "embedding": embedding
        }

        collection.insert_one(document)

    print("Ingestion completed successfully.")

if __name__ == "__main__":
    ingest_documents()
