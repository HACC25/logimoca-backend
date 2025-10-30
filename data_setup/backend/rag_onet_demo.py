# backend/rag_onet_demo.py
"""
RAG pipeline using O*NET skills and Hawai‘i Career Pathways corpus.
"""

import os, requests
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate

DATA_DIR = Path("data/processed")
VECTOR_DIR = "data/embeddings"

# --- 1. External skill lookup ---
def get_onet_skills(job_title: str, onet_api_key: str) -> list[str]:
    """Fetch or mock O*NET skills"""
    try:
        r = requests.get(
            f"https://services.onetcenter.org/ws/mnm/careers/{job_title}",
            auth=(onet_api_key, ""),
            timeout=10,
        )
        if r.status_code == 200:
            return [s["name"] for s in r.json().get("skills", [])][:10]
    except Exception as e:
        print("O*NET unavailable, using mock:", e)
    mock_skills = {
        "AI Engineer": ["Python", "Machine Learning", "Statistics", "Neural Networks"],
        "Hospitality Manager": ["Customer Service", "Operations", "Budgeting"]
    }
    return mock_skills.get(job_title, ["Communication", "Problem Solving", "Teamwork"])

# --- 2. Corpus embedding ---
def build_vector_store():
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = []
    for path in DATA_DIR.glob("*.txt"):
        text = path.read_text(encoding="utf-8")
        meta = {"source": path.name}
        for chunk in splitter.split_text(text):
            docs.append(Document(page_content=chunk, metadata=meta))
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(docs, embedding=embeddings, persist_directory=VECTOR_DIR)
    vectordb.persist()
    print(f"Embedded {len(docs)} chunks to {VECTOR_DIR}")
    return vectordb

# --- 3. Chain assembly (modern) ---
def make_retrieval_chain(vectordb):
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    system_prompt = """You are an educational advisor. 
Use the provided context from Hawai‘i Career Pathways to suggest relevant UH pathways or degrees.
If you are unsure, respond with 'I need more information.'
Context: {context}
Skills: {skills}
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{skills}")
    ])

    combine_docs = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, combine_docs)
    return chain

# --- 4. Main flow ---
def recommend_pathway(job_title: str):
    if not Path(VECTOR_DIR).exists():
        build_vector_store()
    vectordb = Chroma(persist_directory=VECTOR_DIR, embedding_function=OpenAIEmbeddings())
    chain = make_retrieval_chain(vectordb)
    skills = get_onet_skills(job_title, os.getenv("ONET_API_KEY", "demo"))
    print("\n🧭 Skills identified:", skills)
    result = chain.invoke({"skills": ", ".join(skills)})
    print("\n🎓 Recommended UH Pathways:\n")
    print(result["answer"])
    print("\n📚 Sources:", [doc.metadata["source"] for doc in result["context"]])

if __name__ == "__main__":
    recommend_pathway("AI Engineer")
