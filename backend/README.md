### Backend

The backend is a Flask-based application responsible for:

- **Document Preprocessing:**

  - Converts `.md` files into embeddings using OpenAI’s embedding model.
  - Stores embeddings in a FAISS index for efficient similarity search.

- **Question Processing:**
  - Generates embeddings for the user’s question.
  - Retrieves relevant documents using FAISS.
  - Uses OpenAI’s chat model to generate answers based on the retrieved context.

**Key Components:**

1. **Preprocessing:**

   - Converts `.md` files into embeddings and stores them in `embeddings.index`.
   - Mapping between filenames and embeddings is stored in `filenames.json`.

2. **RAG Pipeline:**

   - Embeddings for the question are matched with the FAISS index to retrieve relevant documents.
   - Retrieved content is combined into context for OpenAI’s GPT model.

3. **Query Handling:**

   - The backend determines whether to respond with general information from the CV or recent activities from the RSS feed based on the user's question.

4. **Logging:**
   - Detailed logs for debugging and tracing user queries and backend responses.

**Directory Structure**

```bash
backend/
│
├── app/                        # Application folder
│   ├── app.py                  # Main Flask app
│   ├── models/                 # Embeddings and mappings
│   │   ├── embeddings.index    # FAISS index file
│   │   └── filenames.json      # Mapping of document filenames
│   ├── routes/                 # Blueprint for handling routes
│   │   └── chat.py             # Endpoint for handling chat requests
│   ├── services/               # Modularized services
│   │   ├── faiss_service.py    # Service for FAISS-related tasks
│   │   ├── rss_service.py      # Service for RSS feed-related tasks
│   │   └── openai_service.py   # Service for OpenAI-related tasks
│   └── utils/                  # Utility functions and constants
│       ├── config.py           # Configurations for API keys, paths, etc.
│       ├── logging.py          # Setup for logging
│       ├── schemas.py          # Pydantic schemas for data validation
│       └── prompts.py          # Prompts used in the app
│
├── embeddings/                 # Preprocessing scripts
|   └── embeddings.json         # Embeddings for documents
│
├── preprocessing/              # Preprocessing scripts
│   ├── index_embeddings.py     # Script to generate FAISS index
│   └── upload_files.py         # Script to upload documents
│
└── data/                       # Documents for context
    ├── rss_feed.xml            # Recent activities
    └── cv.md                   # My CV

```
