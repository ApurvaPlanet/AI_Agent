import re

def split_text_into_chunks(text, chunk_size=500, overlap=50):
    """Splits text into overlapping chunks for better retrieval."""
    
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap  # Overlapping chunks improve retrieval

    return chunks
