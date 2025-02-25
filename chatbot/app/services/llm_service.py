import openai
import pickle
import os
from chatbot.app.config import OPENAI_API_KEY
from chatbot.app.services.faiss_service import retrieve_vectors
from chatbot.app.services.embedding_service import generate_embeddings


LLM_MODEL_PATH = "storage/llm_model.pkl"
MAX_CONTEXT_TOKENS = 5000
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def load_llm_memory():
    """Loads LLM memory from disk."""
    return pickle.load(open(LLM_MODEL_PATH, "rb")) if os.path.exists(LLM_MODEL_PATH) else {}


def save_llm_memory(memory):
    """Saves LLM memory to disk."""
    with open(LLM_MODEL_PATH, "wb") as f:
        pickle.dump(memory, f)


def update_llm_memory(input_text, answer, department):
    """Updates LLM memory with new knowledge."""
    memory = load_llm_memory()
    memory.setdefault(department, {})[input_text.lower()] = answer
    save_llm_memory(memory)


def train_llm(data):
    """Trains the LLM and stores data."""
    with open(LLM_MODEL_PATH, "wb") as f:
        pickle.dump({"data": data}, f)
    return {"data": data}


def query_llm(input_text, department):
    """Queries the LLM using FAISS-retrieved context."""
    memory = load_llm_memory()
    
    # Check if the answer is already stored
    if department in memory and input_text.lower() in memory[department]:
        return {"answer": memory[department][input_text.lower()]}

    # Retrieve relevant document chunks
    relevant_chunks = retrieve_vectors(input_text, department, top_k=5)
    if not relevant_chunks:
        return {"answer": "Sorry, no relevant data found."}

    # Build context from retrieved documents
    context = "\n\n".join(chunk["content"][:MAX_CONTEXT_TOKENS] for chunk in relevant_chunks)

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use the provided documents to answer accurately."},
        {"role": "user", "content": f"Here is relevant context:\n{context}\n\nQuestion: {input_text}\nAnswer:"}
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return {"answer": response.choices[0].message.content.strip()}

    except openai.BadRequestError as e:
        return {"answer": f"OpenAI API Error: {str(e)}"}
