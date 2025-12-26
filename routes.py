# Import APIRouter to create modular API routes
from fastapi import APIRouter

# Import Note model for data validation
from models import Note

# Import MongoDB collection to store and fetch notes
from database import notes_collection

# Create router object to define API endpoints
router = APIRouter()

# POST API to create a new note
# note → incoming JSON data
# Note → Pydantic model for data validation
@router.post("/notes")
def create_note(note: Note):
    # Convert note object into dictionary and insert into MongoDB JSON → Note object → dict → MongoDB
    notes_collection.insert_one(note.dict())
    return {"message": "Note created"}

# GET API to fetch all notes
@router.get("/notes")
def get_notes():
    # Create empty list to store notes
    notes = []
        # Fetch all documents from MongoDB
    # {} means fetch all records
    # {"_id": 0} removes MongoDB auto-generated _id field
    for note in notes_collection.find({}, {"_id": 0}):
        # Add each note into list
        notes.append(note)
    return notes
