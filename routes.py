# Import APIRouter to create modular API routes
from fastapi import APIRouter

# Import Note model for data validation
from models import Note

# bson -> binary JSON (used to work with MongoDB ObjectId)
from bson import ObjectId

# Import MongoDB collection to store and fetch notes
from database import notes_collection

# Import text summarization service
from services.hf_summarizer import summarize_text_hf

# Create router object to define API endpoints
router = APIRouter()

# POST API to create a new note
# note → incoming JSON data
# Note → Pydantic model for data validation
@router.post("/notes")
def create_note(note: Note):
    # Convert note object into dictionary and insert into MongoDB
    # JSON → Note object → dict → MongoDB
    notes_collection.insert_one(note.dict())

    # Send success message to frontend
    return {
        "success": True,
        "message": "Note added successfully"
    }

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
        # Convert MongoDB ObjectId into string before sending to frontend
        notes.append(
            {
                "title": note["title"],
                "content": note["content"],
                "id": str(note["_id"])
            }
        )

    # Return list of notes to frontend
    return notes

# PUT API to update an existing note
@router.put("/notes/{note_id}")
def update_note(note_id: str, note: Note):
    # Print ID received from frontend (debug purpose)
    print("ID coming from frontend:", note_id)
    print("Type of ID:", type(note_id))

    # Update note by matching MongoDB _id
    result = notes_collection.update_one(
        {"_id": ObjectId(note_id)},
        {
            "$set": {
                "title": note.title,
                "content": note.content
            }
        }
    )

    # If a document was matched and updated
    if result.matched_count == 1:
        return {
            "success": True,
            "message": "Note updated successfully"
        }

    # If no matching document was found
    return {
        "success": False,
        "message": "Note not found"
    }

# DELETE API to delete a note
@router.delete("/notes/{note_id}")
def delete_note(note_id: str):
    # Delete note using MongoDB ObjectId
    result = notes_collection.delete_one({"_id": ObjectId(note_id)})

    # If note was successfully deleted
    if result.deleted_count == 1:
        return {
            "success": True,
            "message": "Note deleted successfully"
        }

    # If note was not found
    return {
        "success": False,
        "message": "Note not found"
    }

# POST API to summarize a note using LLM
@router.post("/notes/{note_id}/summarize-llm")
def summarize_note_llm(note_id: str):
    note = notes_collection.find_one({"_id": ObjectId(note_id)})

    if not note:
        return {"error": "Note not found"}

    summary = summarize_text_hf(note["content"])

    notes_collection.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": {"summary": summary}}
    )

    return {"summary": summary}

@router.post("/summarize-text")
def summarize_text_api(payload: dict):
    text = payload.get("text", "")
    note_id = payload.get("note_id")

    summary = summarize_text_hf(text)

    # Save summary if note_id is provided
    if note_id:
        notes_collection.update_one(
            {"_id": ObjectId(note_id)},
            {"$set": {"summary": summary}}
        )

    return {"summary": summary}

