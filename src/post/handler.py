from sqlalchemy.sql import text
from src.microservices_handler.handler import vector_to_pgvector

async def create_post(post, request, db):
    tags = post.tags
    tags = ', '.join(tags)
    model = request.app.state.embedding_model
    embedding = model.encode(f" {post.content} {tags} {post.language}")

    # Remember media url insertion and embeddings for later

    query = text("""
        INSERT INTO posts (content, tags, visibility, created_by, is_commentable, embedding)
        VALUES (:content, :tags, :visibility, :created_by, :is_commentable, :embedding)
        RETURNING content, tags, visibility, is_commentable, created_by
    """)

    result = await db.execute(query, {
        "content": "This is the content of the post.",
        "tags": ["tag1", "tag2"],  # should map to ARRAY
        "visibility": "public",
        "created_by": "74ccbede-980f-4eee-8576-09453493148b",
        "is_commentable": True,
        "embedding": vector_to_pgvector(embedding)
    })

    await db.commit()
    post_record = result.fetchone()

    return {"message": "Post and embeddings successfully created"}
    