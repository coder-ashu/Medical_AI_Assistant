from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
# ---- Load API key ----
load_dotenv()

app = FastAPI()

# ---- Enable CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Embeddings ----
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.environ["GEMINI_API_KEY"]
)

# ---- Load Chroma DB ----
vectorstore = Chroma(
    collection_name="pdf_summaries",  # must match what you used in training
    embedding_function=embeddings,
    persist_directory="./chroma_store"
)

# ---- LLM (Gemini) ----
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",   # <-- use correct model name
    google_api_key=os.environ["GEMINI_API_KEY"],
    function_calling_mode="NONE"
)


# ---- Load mappings ----
with open("id_to_summary.json", "r") as f:
    id_to_summary = json.load(f)

with open("id_to_fulltext.json", "r") as f:
    id_to_fulltext = json.load(f)

# ---- Request schema ----
class QueryRequest(BaseModel):
    query: str
    k: int = 3


# ---- Health Check ----
@app.get("/")
def hello():
    return {"hello": "welcome, I am a medical AI assistant"}


# ---- Search + LLM Endpoint ----
@app.post("/query")
async def search_docs(request: QueryRequest):
    try:
        # Step 1: similarity search
        results = vectorstore.similarity_search(request.query, k=request.k)

        # Step 2: collect context
        context_docs, output = [], []
        for doc in results:
            doc_id = doc.metadata.get("source_id", "N/A")
            summary = id_to_summary.get(doc_id, "N/A")
            full_text = id_to_fulltext.get(doc_id, "N/A")

            output.append({
                "id": doc_id,
                "summary": summary,
                "full_text": full_text
            })

            context_docs.append(full_text)

        context = "\n\n".join(context_docs)

        # Step 3: build prompt
        prompt = f"""You are a helpful medical AI assistant.
Answer the user query using the following retrieved context.
You should ask for more symptoms if you feel information is insuffiecient but this should be done at max 3 times,
You should tell the possible disease and it's cure in seperate lines so that it is user friendly.

User query: {request.query}

Context:
{context}
"""

        # Step 4: call Gemini
        gemini_response = await llm.ainvoke(prompt)

        return {
            "query": request.query,
            "results": output,
            "answer": str(gemini_response.content)  # ensure JSON safe
        }

    except Exception as e:
        # catch errors so /docs never hangs
        return {
            "query": request.query,
            "results": [],
            "answer": None,
            "error": str(e)
        }
