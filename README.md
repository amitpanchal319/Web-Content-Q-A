# WebQNA - Web Content Q&A System

🚀 **WebQNA** is an AI-Powered Q&A System that allows users to fetch content from any website URL and ask questions about the content. This system is built using FastAPI, Transformers, and Newspaper3k with real-time content analysis and question-answering capabilities.

## 🔑 Key Features

- Fetches Website Content via URL
- Extracts Full Article Text Automatically
- Answers Questions based on Ingested Content
- Uses **DistilBERT** Model from Hugging Face for NLP Q&A
- Live API hosted on **Render**
- CORS Enabled for Frontend Integration
- Detailed Logging for Debugging

---

## 🎯 Tech Stack

| Technology     | Purpose               |
|---------------|---------------------|
| FastAPI       | Backend API         |
| Uvicorn       | ASGI Server        |
| Newspaper3k   | Content Extraction |
| Transformers  | Question Answering Model |
| DistilBERT    | Pre-trained NLP Model |
| Render        | Cloud Deployment |

---

## 🤖 Model Used

### **DistilBERT

 (distilbert-base-cased-distilled-squad)**
DistilBERT is a smaller, faster version of BERT model trained on **SQuAD Dataset**.

| Feature           | Description               |
|----------------|--------------------------|
| Model Name     | distilbert-base-cased-distilled-squad |
| Size           | 66M Parameters         |
| Speed         | 60% faster than BERT   |
| Accuracy      | 95% SQuAD Performance  |
| Use Case      | Question Answering System |

#### How it Works?

1. User enters a URL.
2. The backend extracts the full article content using **Newspaper3k**.
3. The content is stored in memory.
4. The user asks a question about the content.
5. The **DistilBERT QA Model** generates the answer from the content.

## 🚀 Live Demo

✅ Frontend API Hosted Link:  

👉 https://web-content-qa-frontend.onrender.com/

### How to Test?

1. Go to `/` Endpoint to check server status.
2. Use `/ingest` to extract content.
3. Use `/ask` to ask questions on the content.

## Installation & Run Locally

### 1. Clone Repo

```bash
git clone https://github.com/amitpanchalofficial/WebQNA.git
cd WebQNA
```

### 2. Create Virtual Environment

```bash
python -m venv webqna
source webqna/bin/activate (Linux)
webqna\Scripts\activate (Windows)
```

### 3. Install Requirements

```bash
pip install -r backend/requirements.txt
```

### 4. Run Backend

```bash
uvicorn backend:app --reload
```

## 🙌 Amit Panchal 🚀

### Connect with Me

- LinkedIn: [Amit Panchal] https://www.linkedin.com/in/amit-panchal0319

### If you like this project, don't forget to ⭐ this repo
