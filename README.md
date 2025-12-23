# RAG Retrieval System – Mental Health FAQ

## Overview
This project implements the **retrieval component of a Retrieval-Augmented Generation (RAG) system**.  
It allows users to submit natural language queries and retrieves the most relevant context chunks from a small mental health FAQ dataset using vector similarity.

No LLM-based generation is used, as required by the assignment.

---

## Dataset

- **Source**: Kaggle – Mental Health FAQ dataset  
- **Type**: Structured FAQ (Question–Answer pairs)  
- **Size Used**: First 50 rows  

### Why This Dataset?
The dataset was chosen because it contains short, high-quality question–answer pairs related to mental health.  
This structure makes it ideal for evaluating a retrieval-based system, where user queries are matched to semantically similar questions and their corresponding answers.

Additionally, the topic is one I explored in my final project, so I am familiar with it and feel a personal connection to it.  
This made it easier to understand the dataset and work effectively on a short, time-constrained project.

### Expected User Questions
- “Where can I find mental health support?”
- “How can I manage anxiety?”
- “What types of mental health professionals exist?”

---

## Architecture

### Embeddings
- **Model**: `text-embedding-3-small` (OpenAI)  
- Low-cost and suitable for semantic similarity on small datasets

### Vector Database
- **MongoDB**  
- Used to store embeddings together with chunk metadata

---

### Chunking Strategy
- **Chunk size**: 300 characters  
- **Overlap**: 50 characters  

Chunking was implemented to demonstrate a standard RAG pipeline.  
Although the dataset consists of short FAQ entries, this strategy balances semantic completeness with retrieval precision.

---

### Retrieval Parameters
- **Similarity metric**: Cosine similarity  
- **Top-K results**: 3  
- **Minimum similarity threshold**: 0.6  

During testing, a similarity threshold of 0.75 proved too restrictive for short and general user queries (e.g., “How to deal with anxiety?”), resulting in no retrieved results.  
Therefore, the threshold was adjusted to 0.6 to improve recall while maintaining acceptable relevance.

---

## Setup

### Installation
```bash
pip install -r requirements.txt
```

### Environment Variables
#### Create a .env file:
```bash
OPENAI_API_KEY=your_openai_api_key
MONGODB_URI=your_mongodb_uri
MONGODB_DB=your_database_name
```

#### Ingest Data:
```bash
python ingest.py
```

#### Run Server:
```bash
python app.py
```

### Usage
**1.** Enter a natural language query in the input field
**2.** Submit the query
**3.** The system retrieves and displays:
- Relevant context chunks
- Similarity scores
- Chunk identifiers (Question ID, Chunk ID)

**Example Queries:**
- "Where can I go to find therapy and mental health treatment options?" ,
- “What causes mental health problems and how can they be prevented?” , 
- “How can I maintain social connections if I feel lonely?”

### Notes:
Short or very general queries may result in lower similarity scores.