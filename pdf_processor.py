import PyPDF2
import os
import json

def extract_and_save_pdf_text(pdf_path, output_path="extracted_text.txt"):
    """Extract text from PDF and save to file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            print(f"Processing PDF with {len(pdf_reader.pages)} pages...")
            
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                text += f"\n--- Page {i+1} ---\n"
                text += page_text
                text += "\n"
                print(f"Processed page {i+1}")
            
            # Save to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"Text extracted and saved to {output_path}")
            print(f"Total characters: {len(text)}")
            
            return text
            
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

def analyze_pdf_content(text):
    """Analyze the content of extracted text"""
    if not text:
        return
    
    lines = text.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    
    print(f"\n=== PDF Content Analysis ===")
    print(f"Total lines: {len(lines)}")
    print(f"Non-empty lines: {len(non_empty_lines)}")
    print(f"Total words: {len(text.split())}")
    
    # Show first few lines
    print(f"\n=== First 10 non-empty lines ===")
    for i, line in enumerate(non_empty_lines[:10]):
        print(f"{i+1}: {line[:100]}...")
    
    # Look for key information
    keywords = ['pokar', 'greens', 'address', 'phone', 'email', 'website', 'delivery', 'order']
    found_keywords = []
    
    for keyword in keywords:
        if keyword.lower() in text.lower():
            found_keywords.append(keyword)
    
    print(f"\n=== Found Keywords ===")
    print(f"Keywords found: {', '.join(found_keywords)}")

def chunk_text_for_rag(text, chunk_size=500, overlap=50):
    """Split text into chunks for RAG"""
    chunks = []
    words = text.split()
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    print(f"\n=== RAG Chunking ===")
    print(f"Created {len(chunks)} chunks")
    print(f"Average chunk size: {sum(len(chunk.split()) for chunk in chunks) / len(chunks):.1f} words")
    
    # Show first few chunks
    print(f"\n=== First 3 chunks ===")
    for i, chunk in enumerate(chunks[:3]):
        print(f"Chunk {i+1}: {chunk[:200]}...")
    
    return chunks

def save_chunks_to_json(chunks, output_path="knowledge_chunks.json"):
    """Save chunks to JSON file for later use"""
    data = {
        "chunks": chunks,
        "metadata": {
            "total_chunks": len(chunks),
            "chunk_size": 500,
            "overlap": 50
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Chunks saved to {output_path}")

if __name__ == "__main__":
    pdf_path = "Pokar Greens.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"PDF file {pdf_path} not found!")
        exit(1)
    
    # Extract text
    text = extract_and_save_pdf_text(pdf_path)
    
    if text:
        # Analyze content
        analyze_pdf_content(text)
        
        # Create chunks
        chunks = chunk_text_for_rag(text)
        
        # Save chunks
        save_chunks_to_json(chunks)
        
        print(f"\n=== Processing Complete ===")
        print(f"You can now use the RAG-enabled chatbot with the processed PDF data.")
    else:
        print("Failed to extract text from PDF")
