# Import BaseModel from pydantic for data validation
from pydantic import BaseModel

class Note(BaseModel):
    # Title of the note (string)
    title: str
    # Content of the note (string)
    content: str
