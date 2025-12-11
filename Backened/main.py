from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Embedding model (MiniLM) ----------------
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(MODEL_NAME)

# --------------- Load FAISS index + ID mapping ---------------
faiss_index = faiss.read_index("medical_faiss.index")

with open("faiss_id_mapping.json", "r") as f:
    faiss_ids = json.load(f)

# --------------- Load Chroma DB (same as in Colab) ---------------
# vectorstore = Chroma(
#     collection_name="pdf_summaries",
#     embedding_function=SentenceTransformerEmbeddings(model_name=MODEL_NAME),
#     persist_directory="./medical_chroma"
# )

# --------------- Load text mappings ---------------
with open("id_to_summary.json", "r") as f:
    id_to_summary = json.load(f)

with open("id_to_fulltext.json", "r") as f:
    id_to_fulltext = json.load(f)

# --------------- LLM (Gemini) ---------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.environ["GEMINI_API_KEY"],
    function_calling_mode="NONE",
)


class QueryRequest(BaseModel):
    query: str
    k: int = 3


@app.get("/")
def root():
    return {"message": "FAISS + MiniLM Medical Assistant Running!"}


@app.post("/query")
async def query_text(request: QueryRequest):
    try:
        # 1) Embed query with MiniLM
        query_embedding = embedding_model.encode(
            [request.query],
            convert_to_numpy=True
        ).astype("float32")

        faiss.normalize_L2(query_embedding)

        # 2) FAISS search
        D, I = faiss_index.search(query_embedding, request.k)
        retrieved_ids = [faiss_ids[i] for i in I[0]]

        results = []
        context_chunks = []

        for doc_id in retrieved_ids:
            summary = id_to_summary.get(doc_id, "")
            full_text = id_to_fulltext.get(doc_id, "")
            results.append(
                {
                    "id": doc_id,
                    "summary": summary,
                    "full_text": full_text,
                }
            )
            context_chunks.append(full_text)

        context = "\n\n".join(context_chunks)

        prompt = f"""
You are a medical assistant.
Use ONLY the following medical context to answer the user query.

Answer in two sections:
1) Possible Condition
2) Suggested Treatment

User Query:
{request.query}

Relevant Medical Context:
{context}
"""

        answer = await llm.ainvoke(prompt)

        return {
            "query": request.query,
            "results": results,
            "answer": str(answer.content),
        }

    except Exception as e:
        return {
            "query": request.query,
            "results": [],
            "answer": None,
            "error": str(e),
        }
