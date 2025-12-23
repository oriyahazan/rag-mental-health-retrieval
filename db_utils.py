import os
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