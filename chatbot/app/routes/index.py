from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import requests
from urllib.parse import urljoin
from chatbot.app.services.llm_service import train_llm
from chatbot.app.services.faiss_service import store_vectors
from chatbot.app.utils.file_parser import extract_text_from_folder
from bs4 import BeautifulSoup


router = APIRouter(prefix="/index", tags=["Indexing"])

class FolderMetadata(BaseModel):
    folder_name: str
    department: str

class IndexRequest(BaseModel):
    folder_path: Optional[str] = None
    remote_url: Optional[str] = None
    folder_metadata: List[FolderMetadata]

@router.post("/")
async def index_data(request: IndexRequest):
    if not request.folder_path and not request.remote_url:
        raise HTTPException(status_code=400, detail="Provide either folder_path or remote_url")

    if request.remote_url:
        request.folder_path = download_remote_files(request.remote_url)

    if not os.path.exists(request.folder_path):
        raise HTTPException(status_code=400, detail="Invalid directory path")

    extracted_data = []
    for metadata in request.folder_metadata:
        folder_data = extract_text_from_folder(os.path.join(request.folder_path, metadata.folder_name), metadata.department)
        extracted_data.extend(folder_data)

    # Train LLM but don't pass it to FAISS (they are separate!)
    train_llm(extracted_data)

    # Store FAISS Vectors
    store_vectors(extracted_data)  # ✅ Pass raw extracted data

    return {"message": "Files indexed successfully"}



def download_remote_files(remote_url: str, save_dir="storage/remote_files"):
    """Downloads all files from a remote directory and saves them locally."""
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        response = requests.get(remote_url)
        if response.status_code != 200:
            raise Exception("Failed to fetch remote files.")

        # Parse links in the remote folder (assuming an HTML directory listing)
        soup = BeautifulSoup(response.text, "html.parser")
        links = [urljoin(remote_url, a["href"]) for a in soup.find_all("a", href=True)]

        downloaded_files = []
        for link in links:
            filename = os.path.basename(link)
            file_path = os.path.join(save_dir, filename)

            file_response = requests.get(link)
            if file_response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(file_response.content)
                downloaded_files.append(file_path)

        return save_dir  # Return path to the downloaded files
    
    except Exception as e:
        raise Exception(f"Error downloading remote files: {str(e)}")
