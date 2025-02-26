from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chatbot.app.routes import index, query, cleanup, learn

app = FastAPI(title="Chatbot with FAISS & Persistent LLM")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(index.router)
app.include_router(query.router)
app.include_router(learn.router)
app.include_router(cleanup.router)

@app.get("/")
def home():
    return {"message": "Welcome to the AI Chatbot API"}

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}
