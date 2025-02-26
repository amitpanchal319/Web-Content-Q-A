import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import newspaper
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or specify your frontend URL)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "FastAPI is running successfully!"}

# Load NLP model
qa_pipeline = pipeline(
    "question-answering",
    model="distilbert/distilbert-base-cased-distilled-squad",
    revision="564e9b5"
)

# Global variable to store ingested content
ingested_content = ""

# Request Models
class URLInput(BaseModel):
    url: str

class QuestionInput(BaseModel):
    question: str

# Ingest URL content
@app.post("/ingest")
async def ingest_url(data: URLInput):
    global ingested_content
    try:
        print(f"Ingesting URL: {data.url}")  # Log the URL
        article = newspaper.Article(data.url)
        article.download()
        article.parse()
        ingested_content = article.text
        print(f"Ingested Content: {ingested_content[:500]}")  # Log the first 500 characters
        return {"message": "Content ingested successfully!", "preview": ingested_content[:500]}
    except Exception as e:
        print(f"Error ingesting URL: {e}")  # Log the error
        raise HTTPException(status_code=400, detail=str(e))

# Answer questions
@app.post("/ask")
async def ask_question(data: QuestionInput):
    global ingested_content
    if not ingested_content:
        raise HTTPException(status_code=400, detail="No content ingested. Please ingest a URL first.")
    try:
        print(f"Question: {data.question}")  # Log the question
        result = qa_pipeline(question=data.question, context=ingested_content)
        print(f"Answer: {result}")  # Log the answer
        return {"answer": result["answer"]}
    except Exception as e:
        print(f"Error in question-answering: {e}")  # Log the error
        raise HTTPException(status_code=500, detail=str(e))

# Run the app using Uvicorn (if executed directly)
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    import uvicorn
    print(f"Starting FastAPI on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)