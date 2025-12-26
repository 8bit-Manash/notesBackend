# Import BaseModel from pydantic for data validation
from pydantic import BaseModel

from typing import Optional

class Note(BaseModel):
    # Title of the note (string)
    title: str
    # Content of the note (string)
    content: str
    # AI-generated summary of the note (string)
    summary: Optional[str] = None
