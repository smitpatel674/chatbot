import requests
import os
import json
from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import PyPDF2
import io

app = Flask(__name__)

# Configuration
GEMINI_API_KEY = 
GEMINI_URL = 

# Initialize sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Global variables for RAG
knowledge_base = []
knowledge_embeddings = None
faiss_index = None

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks"""
    chunks = []
    words = text.split()
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

def create_knowledge_base(pdf_path):
    """Create knowledge base from PDF"""
    global knowledge_base, knowledge_embeddings, faiss_index
    
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    if not text:
        return False
    
    # Split into chunks
    chunks = chunk_text(text)
    knowledge_base = chunks
    
    # Create embeddings
    embeddings = model.encode(chunks)
    knowledge_embeddings = embeddings
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    faiss_index = faiss.IndexFlatIP(dimension)
    faiss_index.add(embeddings.astype('float32'))
    
    print(f"Knowledge base created with {len(chunks)} chunks")
    return True

def search_knowledge_base(query, top_k=3):
    """Search knowledge base for relevant information"""
    if faiss_index is None or knowledge_base is None:
        return []
    
    # Encode query
    query_embedding = model.encode([query])
    
    # Search
    scores, indices = faiss_index.search(query_embedding.astype('float32'), top_k)
    
    # Return relevant chunks
    relevant_chunks = []
    for idx in indices[0]:
        if idx < len(knowledge_base):
            relevant_chunks.append(knowledge_base[idx])
    
    return relevant_chunks

# Initialize knowledge base
pdf_path = "Pokar Greens.pdf"
if os.path.exists(pdf_path):
    create_knowledge_base(pdf_path)
else:
    print(f"PDF file {pdf_path} not found")

BOT_CONTEXT = """
You are a helpful, polite customer support assistant for Pokar Greens, an online store for fresh fruits and vegetables.
The website is https://pokargreens.com/
The store is located at G39 Shaligram Suqare, Gota, Ahmedabad, 382481.
For orders, customers can use the website or contact via WhatsApp at 9586901881.
For support, contact info@pokargreens.com
Delivery is available in Gota, Ahmedabad.
Answer in Gujarati, Hindi, or English depending on the customer's language.
Keep replies short and helpful.
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    user_lang = request.json.get("language", "English")
    
    # Search knowledge base for relevant information
    relevant_info = search_knowledge_base(user_msg)
    context_info = ""
    if relevant_info:
        context_info = "\n\nRelevant information from our knowledge base:\n" + "\n".join(relevant_info)
    
    lang_map = {"English": "en", "Hindi": "hi", "Gujarati": "gu"}
    lang_code = lang_map.get(user_lang, "en")
    lang_instruction = (
        f"IMPORTANT: Reply ONLY in {user_lang} (language code: {lang_code}). "
        f"Do not use any other language. "
        f"Do not explain your choice. "
        f"Just answer the user's question in {user_lang}."
    )
    
    if user_lang == "Hindi":
        example = (
            "Example:\n"
            "Customer: आप क्या बेचते हैं?\n"
            "Bot: हम ताजे फल और सब्जियाँ बेचते हैं।\n"
        )
    elif user_lang == "Gujarati":
        example = (
            "Example:\n"
            "Customer: તમે શું વેચો છો?\n"
            "Bot: અમે તાજા ફળો અને શાકભાજી વેચીએ છીએ.\n"
        )
    else:
        example = ""
    
    full_msg = (
        lang_instruction + "\n"
        + example +
        BOT_CONTEXT + 
        context_info + "\n"
        + "Customer: " + user_msg
    )
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_msg}
                ]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            try:
                reply = data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                reply = "Sorry, I couldn't understand the response from Gemini."
        else:
            reply = "Sorry, there was an error contacting Gemini."
    except Exception as e:
        reply = f"Sorry, there was an error: {str(e)}"
    
    return jsonify({"reply": reply})

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "knowledge_base_size": len(knowledge_base) if knowledge_base else 0,
        "faiss_index_ready": faiss_index is not None
    })

if __name__ == "__main__":
    app.run(debug=True)
