# Import APIRouter to create modular API routes
from fastapi import APIRouter

# Import Note model for data validation
from models import Note

# bson -> binary JSON
from bson import ObjectId

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
    for note in notes_collection.find():
        # Add each note into list
        notes.append(
            {
                "title": note["title"],
                "content": note["content"],
                "id": str(note["_id"])
            }
        )
    return notes


@router.put("/notes/{note_id}")
def update_note(note_id: str, note: Note):
    # Convert note object into dictionary and insert into MongoDB JSON → Note object → dict → MongoDB
    print("ID coming from frontend:", note_id)
    print("Type of ID:", type(note_id))

    result = notes_collection.update_one(
        {"_id": ObjectId(note_id)},
        {
            "$set": {
                "title": note.title,
                "content": note.content
            }
        }
    )
    return {"message": "Note updated"}

@router.delete("/notes/{note_id}")
def delete_note(note_id: str):
    result = notes_collection.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 1:
        return {"message": "Note deleted"}
    else:
        return {"message": "Note not found"}