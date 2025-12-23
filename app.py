from flask import Flask, request, jsonify, render_template
from db_utils import collection, openai
from ingest import create_embedding
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def retrieve_documents(query, top_k=3, min_similarity=0.6):
    query_emb = create_embedding(query)
    
    docs = list(collection.find({}))
    embeddings = [doc["embedding"] for doc in docs]
    
    similarities = cosine_similarity([query_emb], embeddings)[0]
    
    results = [
        (doc, score)
        for doc, score in zip(docs, similarities)
        if score >= min_similarity
    ]

    results = sorted(results, key=lambda x: x[1], reverse=True)[:top_k]
    
    return results

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_query = data.get("query", "")
    if not user_query:
        return jsonify({"error": "Empty query"}), 400

    results = retrieve_documents(user_query)
    
    return jsonify([
        {
            "question_id": doc["question_id"],
            "chunk_id": doc["chunk_id"],
            "text": doc["text"],
            "score": float(score)
        }
        for doc, score in results
    ])

if __name__ == "__main__":
    app.run(debug=True)