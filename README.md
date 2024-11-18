## README: Ask Me Anything

## Overview

Ask Me Anything is a web-based application that enables users to ask questions about myself (Jun) and receive contextually accurate responses using a Retrieval-Augmented Generation (RAG) pipeline powered by OpenAI's API.

The app comprises a frontend (built with Svelte) and a backend (built with Flask). It uses FAISS for similarity search and OpenAI’s embedding and chat models to generate responses.

## Features

1. Question Submission:
   - Users can input a question and press Enter or click Submit to send their query.
2. Dynamic Answer Generation:
   - The app retrieves relevant information from pre-uploaded documents about Jun and generates a natural language answer.
3. RAG Workflow:
   - Uses FAISS to retrieve the most relevant document snippets and passes them as context to OpenAI’s chat model.

## Architecture

### Backend

The backend is a Flask-based application responsible for:

- Document Preprocessing:

  - Converts `.md` files into embeddings using OpenAI’s embedding model.
  - Stores embeddings in a FAISS index for efficient similarity search.

- Question Processing:
  - Generates embeddings for the user’s question.
  - Retrieves relevant documents using FAISS.
  - Uses OpenAI’s chat model to generate answers based on the retrieved context.

**Key Components:**

1. Preprocessing:

   - Converts `.md` files into embeddings and stores them in `embeddings.index`.
   - Mapping between filenames and embeddings is stored in `filenames.json`.

2. RAG Pipeline:
   - Embeddings for the question are matched with the FAISS index to retrieve relevant documents.
   - Retrieved content is combined into context for OpenAI’s GPT model.
3. Logging:
   - Detailed logs for debugging and tracing user queries and backend responses.

**Directory Structure**

```
backend/
│
├── app/                        # Application folder
│   ├── app.py                  # Main Flask app
│   ├── models/                 # Embeddings and mappings
│   │   ├── embeddings.index    # FAISS index file
│   │   └── filenames.json      # Mapping of document filenames
│   └── utils/                  # Utility functions and constants
│       └── config.py           # Configurations for API keys, paths, etc.
│
├── preprocessing/              # Preprocessing scripts
│   ├── index_embeddings.py     # Script to generate FAISS index
│   └── upload_files.py         # Script to upload documents
│
└── data/                       # Documents for context
    └── cv.md                   # My CV

```