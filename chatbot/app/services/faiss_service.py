import faiss
import pickle
import os
import numpy as np
import time 
from chatbot.app.services.embedding_service import generate_embeddings

FAISS_INDEX_PATH = "storage/faiss_index.bin"
VECTOR_METADATA_PATH = "storage/faiss_metadata.pkl"
vector_store = {"index": None, "data": []}  # Global vector store
THRESHOLD = 4.0  # Distance threshold for similarity search


def load_faiss_index():
    """Loads FAISS index and metadata if available."""
    global vector_store

    if vector_store["index"] is None:
        if not os.path.exists(FAISS_INDEX_PATH) or not os.path.exists(VECTOR_METADATA_PATH):
            raise Exception("FAISS index or metadata not found. Please index data first.")

        print("📥 Loading FAISS index from disk...")
        vector_store["index"] = faiss.read_index(FAISS_INDEX_PATH)

        with open(VECTOR_METADATA_PATH, "rb") as f:
            vector_store["data"] = pickle.load(f)

        print("✅ FAISS index and metadata loaded successfully!")



def store_vectors(data, batch_size=100):
    """Indexes data in FAISS and stores the index on disk."""
    global vector_store

    if not data:
        raise ValueError("No data provided for indexing.")

    print(f"📌 Received {len(data)} documents for FAISS indexing...")

    texts = [doc["content"] for doc in data]
    
    # Process in batches
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        print(f"📌 Processing batch {i//batch_size + 1}/{len(texts)//batch_size + 1}...")
        start_time = time.time()
        
        batch_embeddings = generate_embeddings(batch)  # Use new batch function
        embeddings.extend(batch_embeddings)

        print(f"✅ Batch {i//batch_size + 1} done in {time.time() - start_time:.2f} sec")

    embeddings = np.array(embeddings).astype("float32")
    print(f"📌 Generated {embeddings.shape[0]} embeddings.")

    if vector_store["index"] is None:
        vector_store["index"] = faiss.IndexFlatL2(embeddings.shape[1])
        print("📌 Initialized new FAISS index.")

    vector_store["index"].add(embeddings)
    vector_store["data"].extend(data)

    print(f"📌 Saving FAISS index to {FAISS_INDEX_PATH}...")
    faiss.write_index(vector_store["index"], FAISS_INDEX_PATH)

    with open(VECTOR_METADATA_PATH, "wb") as f:
        pickle.dump(vector_store["data"], f)

    print("✅ FAISS index stored successfully!")

def retrieve_vectors(input_text, department, top_k=5):
    """Retrieves the most relevant vectors from FAISS index."""
    
    if vector_store["index"] is None:
        try:
            load_faiss_index()  # Load FAISS index if not initialized
        except Exception as e:
            raise ValueError(f"FAISS index is not initialized. {str(e)}")

    if vector_store["index"] is None or vector_store["index"].ntotal == 0:
        raise ValueError("FAISS index is empty. Please index data first.")

    print(f"🔍 Retrieving top {top_k} relevant vectors for department: {department}...")

    query_embedding = generate_embeddings([input_text])  # Wrap input in a list for batch processing
    query_embedding = np.array(query_embedding, dtype="float32").reshape(1, -1)

    # 🔹 Perform FAISS search
    distances, indices = vector_store["index"].search(query_embedding, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx == -1 or distances[0][i] > THRESHOLD:  # Ignore invalid or distant results
            continue
        results.append(vector_store["data"][idx])

    if not results:
        raise ValueError("No relevant results found in FAISS index.")

    return results
