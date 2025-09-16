from pydantic import BaseModel
from typing import List, Optional


class JobCreate(BaseModel):
    title : str
    description : str
    skills : List
    industry : List
    createdBy : str


class QueryJobs(BaseModel):
    recentInterests : Optional[List[str]] = None
    location: str
    industry: Optional[List[str]] = None
    skills : Optional[List[str]]
