from sentence_transformers import SentenceTransformer

embedding_model = None
embedding_vectors = []
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def vector_to_pgvector(vec):
    # Converts Python list of floats to pgvector string format: '[x1,x2,x3,...]'
    return "[" + ",".join(map(str, vec)) + "]"