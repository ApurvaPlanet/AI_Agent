import openai
import numpy as np
from chatbot.app.config import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_embeddings(texts):
    """Generates embeddings for a list of texts in a single API call."""
    response = client.embeddings.create(model="text-embedding-ada-002", input=texts)
    
    # Extract all embeddings at once
    return np.array([item.embedding for item in response.data], dtype="float32")
