# Import MongoClient to connect to MongoDB
from pymongo import MongoClient

# Import os to access environment variables
import os

# Import certifi for secure SSL connection
import certifi

# Import load_dotenv to load .env file
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


# Create MongoDB client (connects FastAPI to MongoDB)
client = MongoClient(
    os.getenv("MONGODB_URL"),  # Get DB URL from .env
    tls=True,                 # Enable secure connection
    tlsCAFile=certifi.where() # SSL certificate
)


# Select database named 'notesdb'
db = client["notesdb"]

# Select collection named 'notes'
notes_collection = db["notes"]

