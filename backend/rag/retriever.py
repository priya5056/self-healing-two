import faiss
import pickle
import numpy as np

from rag.embedder import get_model


def retrieve_chunks(query, top_k=5):

    # Load FAISS index
    index = faiss.read_index("data/faiss_index/index.bin")

    # Load stored chunks
    with open("data/chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    # Load embedding model
    model = get_model()

    # Create query embedding
    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    # Search in FAISS index
    distances, indices = index.search(query_embedding, top_k)

    retrieved_chunks = []

    for i in indices[0]:
        if i != -1:
            retrieved_chunks.append(chunks[i])

    return retrieved_chunks