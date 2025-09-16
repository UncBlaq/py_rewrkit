import os
from fastapi import APIRouter, status, Header, HTTPException, Request
from src.jobs.validation import JobCreate, QueryJobs
from src.database import db_dependency
from src.jobs.handler import query_suggested_jobs

job_router = APIRouter(prefix="/job", tags=["JOB"])

from src.jobs.handler import create_job as handle_create_job

@job_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_job(job: JobCreate, 
                      request: Request, 
                      db: db_dependency, 
                      x_api_key: str = Header(None)):
    if x_api_key != os.getenv("RECOMMENDER_API_KEY"):
        raise HTTPException(status_code=403, detail="Forbidden")
    
    return await handle_create_job(job, request, db)

@job_router.post('/jobs-suggested')
async def query_jobs(payload : QueryJobs,
                     request : Request,
                     db : db_dependency,
                     x_api_key: str = Header(None)
                     ):
    if x_api_key != os.getenv("RECOMMENDER_API_KEY"):
        raise HTTPException(status_code=403, detail="Forbidden")

    return await query_suggested_jobs(payload, request, db)