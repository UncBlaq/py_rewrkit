import os
from fastapi import APIRouter, status, Header, HTTPException, Request
from src.post.schema import PostCreate 
from src.database import db_dependency

post_router = APIRouter(prefix="/post", tags=["POST"])

from src.post.handler import create_post as handle_create_post

@post_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, 
                      request: Request, 
                      db: db_dependency, 
                      x_api_key: str = Header(None)):
    if x_api_key != os.getenv("RECOMMENDER_API_KEY"):
        raise HTTPException(status_code=403, detail="Forbidden")
    
    return await handle_create_post(post, request, db)

    


