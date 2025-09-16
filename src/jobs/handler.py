from sqlalchemy.sql import text
from src.microservices_handler.handler import vector_to_pgvector

async def create_job(job,request, db):
    industry = job.industry
    skills = job.skills
    industry_string = ', '.join(industry)
    skills_string = ', '.join(skills)
    model = request.app.state.embedding_model
    embedding = model.encode(f"{job.title} {job.description} {skills_string} {industry_string}")

    query = text("""
        INSERT INTO jobs (title, description, industry, skills, created_by, status, embedding)
        VALUES (:title, :description, :industry, :skills, :created_by, :status, :embedding)
        RETURNING id, title, description, industry, skills, created_by
    """)
    result = await db.execute(query, {
        "title": job.title,
        "description": job.description,
        "industry": job.industry,
        "skills": job.skills,
        "created_by": job.createdBy,
        "status": "open",
        "embedding": vector_to_pgvector(embedding)
    })
    await db.commit()
    job_record = result.fetchone()
    return 'Job and embeddings Successfully created'


async def query_suggested_jobs(payload, request, db):
    recent_interest = ', '.join(payload.recentInterests)
    industry_string = ', '.join(payload.industry)
    skills_string = ', '.join(payload.skills)

    model = request.app.state.embedding_model
    new_embedding = model.encode(f"{recent_interest} {industry_string} {skills_string} {payload.location}")

    new_embedding = new_embedding.tolist()
    pgvector_str = vector_to_pgvector(new_embedding)

    query = text("""
                 SELECT id, budget, title, description, industry, skills, tags, location, job_type, category
                 FROM jobs                 
                 ORDER BY embedding <-> CAST(:embedding AS vector)
                 LIMIT 10
                 """)
    # Fix when there is enough data in db
                # WHERE id NOT IN (
                #   SELECT job_id FROM user_seen_jobs WHERE user_id = :user_id
                # )
    result = await db.execute(query, {"embedding": pgvector_str})
    rows = result.fetchall()

    jobs = []
    for row in rows:
        job = {
            "id": row[0],
            "budget" : row[1],
            "title" : row[2],
            "description": row[3],
            "industry" : row[4],
            "skills" : row[5],
            "tags" : row[6],
            "location" : row[7],
            "job_type": row[8],
            "category" : row[9]
        }
        jobs.append(job)
    return {
        "status" : 200,
        "jobs": jobs
        }

 