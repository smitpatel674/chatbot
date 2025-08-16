# Pokar Greens Chatbot

A smart AI-powered chatbot for Pokar Greens that provides information and assistance using Retrieval-Augmented Generation (RAG) with Gemini API.

## Features

- Interactive chat interface with multi-language support
- Document processing for PDF files
- Context-aware responses using RAG (Retrieval-Augmented Generation)
- Responsive design for various screen sizes
- Support for English, Hindi, and Gujarati languages

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Google Gemini API key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Chatbot-Pokar
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   .\env\Scripts\activate  # On Windows
   source env/bin/activate  # On macOS/Linux
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

## Usage

1. Process PDF files (first time setup):
   ```bash
   python pdf_processor.py
   ```
   This will create:
   - `extracted_text.txt`: Raw text from the PDF
   - `knowledge_chunks.json`: Processed text chunks for the knowledge base

2. Start the Flask development server:
   ```bash
   python app.py
   ```

3. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Project Structure

```
Chatbot-Pokar/
├── app.py                # Main Flask application
├── pdf_processor.py      # PDF processing utilities
├── requirements.txt      # Python dependencies
├── static/
│   └── style.css         # Styles for the web interface
├── templates/
│   └── index.html        # Chat interface
├── extracted_text.txt    # Extracted text from PDF
└── knowledge_chunks.json # Processed text chunks for RAG
```

## Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key
- `PORT`: Port to run the Flask app (default: 5000)

### PDF Processing
Place your PDF files in the project root directory. The default file name is `Pokar Greens.pdf`.

## Customization

### Adding New Documents
1. Place your PDF file in the project root
2. Update `pdf_path` in `app.py` to point to your file
3. Run `python pdf_processor.py` to process the new document
4. Restart the Flask application

### Modifying the Interface
- Edit `templates/index.html` for HTML structure
- Modify `static/style.css` for styling
- Update language options in the JavaScript section of `index.html`

## Troubleshooting

- **PDF Processing Issues**: Ensure the PDF is not password protected
- **API Errors**: Verify your Gemini API key is valid and has sufficient quota
- **Module Not Found**: Run `pip install -r requirements.txt` to install dependencies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Flask and Gemini API
- Uses SentenceTransformers for text embeddings
- FAISS for efficient similarity search
