from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env variables

# Securely load Mongo URI
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client.userUploads
fs = GridFS(db)

db.fs.files.create_index([("location", "2dsphere")])
