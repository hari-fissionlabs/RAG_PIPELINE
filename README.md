# RAG Pipeline PDF Extractor

Simple RAG system that extracts text from PDFs, creates embeddings with chunk overlap, and generates AI responses.

## Quick Start

### 1. Setup & Run
```bash
# Setup PostgreSQL with PGVector
docker run -d --name pgvector-db -p 5433:5432 -e POSTGRES_PASSWORD=3485 ankane/pgvector

# Install dependencies
pip install -r requirements.txt

# Configure environment (copy .env.sample to .env and add your API keys)
cp .env.sample .env

# Run application
cd rag_pipeline_pdf_extractor
python app.py
```

## Features

- **PDF/TXT Processing**: Extract text with 1024-char chunks (20% overlap)
- **Vector Storage**: Store embeddings in PGVector database
- **AI Responses**: Generate answers using Bedrock Nova Lite
- **Auto Cleanup**: Clear database after each session

## Requirements

- Docker (for PostgreSQL + PGVector)
- Python 3.8+
- API keys: Flotorch and Google AI

## Usage

1. **Start**: Run `python app.py`
2. **Input**: Enter PDF/TXT file path
3. **Process**: System creates embeddings and stores in database
4. **Query**: Ask questions about the document
5. **Exit**: Type 'quit' - database auto-cleans



## Configuration

- **Chunk Size**: 1024 characters
- **Overlap**: 20%
- **Database**: PostgreSQL (port 5433)
- **LLM Model**: bedrock/us.amazon.nova-lite-v1:0

## Files

- `app.py` - Main application orchestrator
- `database_setup.py` - PostgreSQL + PGVector connection
- `text_processor.py` - PDF/TXT processing with chunk overlap
- `embedding_generator.py` - Google API embeddings generation
- `vector_store.py` - Store embeddings in PGVector database
- `retriever.py` - Vector similarity search and retrieval
- `generator.py` - LLM response generation using Flotorch Gateway
