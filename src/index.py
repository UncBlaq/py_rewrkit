# from langchain_openai import OpenAIEmbeddings
from fastapi import FastAPI, Request
from src.main import app
from sqlalchemy.sql import text
from src.tests import text2
import psycopg2
from src.database import db_dependency
from src.microservices_handler.handler import vector_to_pgvector
@app.get("/embed")
async def embed_data(request: Request, text: str):
    model = request.app.state.embedding_model
    embedding = model.encode([text])
    return embedding
# --- Embedding and DB logic using app.state.embedding_model ---

# def get_embedding_model():
#     for route in app.routes:
#         if isinstance(route, routing.APIRoute):
#             return app.state.embedding_model
#     return None

# Use the embedding model from app.state for offline scripts
def embed_and_store_texts():
    model = app.state.embedding_model
    if not model:
        print("Embedding model is not available.")
        return

    try:
        embedding_vectors = model.encode(text2)
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return

    conn = psycopg2.connect("dbname=vector_rewrkit user=postgres password=supersecret host=localhost port=5342")
    cur = conn.cursor()

    for i in range(len(embedding_vectors)):
        embedding_vector = embedding_vectors[i].tolist()
        content = text2[i]
        cur.execute(
            "INSERT INTO items (content, embedding) VALUES (%s, %s)",
            (content, embedding_vector)
        )

    conn.commit()
    cur.close()
    conn.close()



async def query_similar_texts(new_text, db):
    model = app.state.embedding_model
    if not model:
        print("Embedding model is not available.")
        return

    new_embedding = model.encode(new_text)
    new_embedding = new_embedding.tolist()
    pgvector_str = vector_to_pgvector(new_embedding)

    query = text("""
        SELECT id, content
        FROM items
        ORDER BY embedding <-> CAST(:embedding AS vector)
        LIMIT 5
    """)

    result = await db.execute(query, {"embedding": pgvector_str})
    rows = result.fetchall()

    for row in rows:
        print(row)


@app.post("/embed-and-store")
async def embed_and_store(request: Request):
    embed_and_store_texts()
    return {"status": "Embeddings stored in database."}


@app.get("/query-similar")
async def query_similar(request: Request, text: str, db : db_dependency):
    # This will print results to console; you can modify to return results
    await query_similar_texts(text, db)
    return {"status": "Query executed. Check server logs for output."}



"""
Prod Openai integration Below
"""


# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# if not OPENAI_API_KEY:
#     raise ValueError("No OPENAI_API_KEY set for OpenAI API")

# # # embeddings = None

# # try:
# #     from langchain_openai import OpenAIEmbeddings
# #     embedding = model.encode("your text here")
# #     # embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
# #     print(f"Embeddings loaded... {embeddings}")
    
# # except Exception as e:
# #     print(f"Embedding error: {e}")


# # # embeddings = OpenAIEmbeddings()
# # embedding_vectors = []
# # if embeddings is not None:
# #     for text in texts:
# #         embedding_vectors.append(embeddings.embed_query(text))
# #     print(len(embedding_vectors[0]))
# # else:
# #     print("Embeddings not initialized")

# # # app.include_router(user_router, prefix="/user", tags=["user"])