# Medical AI Assistant (RAG-Based Chatbot)

A Retrieval-Augmented Generation (RAG) Medical Chatbot built using:

- **FastAPI** (Backend API)
- **ChromaDB** (Vector Database)
- **Google Generative AI – Gemini** (Embedding + LLM)
- **LangChain** (RAG Pipeline)
- **React + Vite** (Frontend UI)

You can ask medical-related questions, and the system retrieves relevant medical text chunks and generates accurate answers using AI.

---

# Features

- 🔍 **Semantic Search** using ChromaDB embeddings
- 🧬 **Google Gemini API** for text generation
- 🔄 **RAG pipeline** via LangChain
- ⚡ **FastAPI backend** for efficient querying
- 💬 **React-based chat UI**
- ☁️ Ready for **Docker** + **EC2 Deployment**

---

# 📂 Project Structure

Medical_AI_Assistant/
│
├── Backened/
│ ├── main.py # FastAPI backend
│ ├── chroma_store/ # Stored embedding vectors
│ ├── id_to_fulltext.json # Full-length text mapping
│ ├── id_to_summary.json # Summary mapping
│ ├── requirements.txt # Backend dependencies
│ └── .env # Environment variables (not committed)
│
└── Frontened/
├── src/ # React components
├── package.json
├── vite.config.js
└── README.md

# 1. Backend Setup (FastAPI)

## **Step 1 — Create Conda Environment (Python 3.10 recommended)**

'''bash

conda create -n medai python=3.10 -y
conda activate medai
pip install -r requirements.txt

## backened

cd Backened
uvicorn main:app --reload --host 0.0.0.0 --port 8000

## Frontened

cd Frontened
npm install 
npm run dev
