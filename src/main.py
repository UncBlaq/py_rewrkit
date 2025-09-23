from fastapi import FastAPI
from sentence-transformers import SentenceTransformer

from fastapi.middleware.cors import CORSMiddleware
from src.post.route import post_router
from src.jobs.route import job_router

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="rewrkit App",
    description="rewrkit API",
    version="0.0.1",
    contact={
        "name": "JM Adereti",
        "email": "michealadereti484@gmail.com",
    }
)
# Configure CORS
# Fix security if server gets called from an unknown source, should only be called ny known microservice
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(post_router)
app.include_router(job_router)

@app.on_event("startup")
async def on_startup():
    app.state.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


          







