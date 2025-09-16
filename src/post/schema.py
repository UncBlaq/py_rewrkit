from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class PostCreate(BaseModel):
    content: str
    location: Optional[str] = None
    tags: Optional[List[str]] = None
    visibility: Optional[str] = None
    isCommentable: Optional[bool] = None
    language: Optional[str] = None
    createdBy: UUID  # ✅ UUID instead of str
    parentPostId: Optional[UUID] = None  # optional UUID if needed
    mediaUrls: Optional[List[str]] = None



