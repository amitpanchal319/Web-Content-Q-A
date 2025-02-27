import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import newspaper
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
import gc
from bs4 import BeautifulSoup

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to Web Content Q&A API 🚀"}

@app.head("/")
async def health_check():
    return {"status": "Healthy"}

# Load NLP model
qa_pipeline = pipeline(
    "question-answering",
    model="distilbert/distilbert-base-cased-distilled-squad",
    revision="564e9b5",
    device=-1  # Force CPU
)

# Global variable to store ingested content
ingested_content = ""

# Request Models
class URLInput(BaseModel):
    url: str

class QuestionInput(BaseModel):
    question: str

# Clean HTML content
def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

# Ingest URL content
@app.post("/ingest/")
async def ingest_url(data: URLInput):
    global ingested_content
    try:
        article = newspaper.Article(data.url)
        article.download()
        article.parse()
        ingested_content = clean_html(article.text)
        
        if not ingested_content.strip():
            raise HTTPException(status_code=400, detail="No content found at the URL.")
        
        return {"message": "URL content ingested successfully"}
    except Exception as e:
        print(f"Error in URL ingestion: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Answer Questions
@app.post("/ask/")
async def ask_question(data: QuestionInput):
    global ingested_content
    if not ingested_content:
        raise HTTPException(status_code=400, detail="No content ingested. Please ingest a URL first.")
    
    try:
        if not data.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
        result = qa_pipeline(question=data.question, context=ingested_content)
        
        if not result["answer"]:
            raise HTTPException(status_code=404, detail="No answer found for the question.")
        
        # Clear Memory
        gc.collect()
        
        return {"answer": result["answer"]}
    
    except Exception as e:
        print(f"Error in question-answering: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    import uvicorn
    print(f"Starting FastAPI on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
