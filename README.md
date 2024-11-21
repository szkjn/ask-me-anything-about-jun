## README: Ask Me Anything

## Overview

Ask Me Anything is a web-based application that enables users to ask questions about myself (Jun) and receive contextually accurate responses using a Retrieval-Augmented Generation (RAG) pipeline powered by OpenAI's API.

The app comprises a frontend (built with Svelte) and a backend (built with Flask). It uses FAISS for similarity search and OpenAI’s embedding and chat models to generate responses.

## Features

1. **Question Submission:**
   - Users can input a question and press Enter or click Submit to send their query.
2. **Dynamic Answer Generation:**
   - The app retrieves relevant information from pre-uploaded documents about Jun and generates a natural language answer.
3. **General Information Responses:**
   - If users ask general questions, the app provides an answer based on Jun's CV.
4. **Recent Activities Context:**
   - If users inquire about recent activities, the app includes an RSS feed context to deliver the latest news about Jun's activities.
5. **Relevant Questions Suggestion:**
   - The application suggests relevant questions based on the context of the latest question and answer interaction.
6. **RAG Workflow:**
   - Uses FAISS to retrieve the most relevant document snippets and passes them as context to OpenAI’s chat model.

## Architecture

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

### Frontend

The frontend is a Svelte-based application that provides a user-friendly interface for submitting questions and receiving answers.

- **User Input:**

  - A single input field for users to ask questions.

- **Dynamic Updates:**

  - Displays the response from the backend in real-time.

- **Keyboard Submission:**
  - Supports pressing Enter for question submission.

**Key Components:**

1. **App.svelte:**

   - The main Svelte component handling user input, API calls, and response rendering.

2. **Question Suggestions:**

Suggests relevant follow-up questions based on the latest interaction.

3. **API Integration:**
   - Sends user queries to the `/ask` endpoint in the backend.

**Directory Structure:**

```
frontend/
│
├── public/                 # Publicly served assets
│
├── src/                    # Source files
│   ├── App.svelte          # Main Svelte application
│   └── main.js             # Entry point for the Svelte app
│
└── package.json            # Project dependencies

```

## Setup

### Prerequisites

1. Python 3.10.9 (backend)
2. FAISS (for similarity search)
3. OpenAI API Key (for embeddings and GPT responses)
4. Node.js 20.10+ (frontend)

### Clone repository

```bash
git clone git@github.com:szkjn/ask-me-anything-about-jun.git
```

### Backend Setup

1. Navigate to the Backend Folder:

```bash
cd ask-me-anything-about-jun
cd backend
```

2. Create a Virtual Environment:

```bash
python -m venv venv
venv\Scripts\activate  # source venv/bin/activate on Unix or MacOS
```

3. Install Dependencies:

```bash
pip install -r requirements.txt
```

4. Configure OpenAI API Key: Open `backend/app/utils/config.py` and set your OpenAI API key:

```bash
OPENAI_API_KEY = os.environ.get([insert-your-key])
```

4. Generate Embeddings: Run the preprocessing script to generate embeddings and the FAISS index.

```bash
python -m preprocessing.upload_files
python -m preprocessing.index_embeddings
```

5. Run the Flask Application from `app/` folder:

```bash
cd app/
python app.py
```

### Frontend Setup

1. Navigate to the Frontend Folder:

```bash
cd frontend
```

2. Install Dependencies:

```bash
npm install
```

3. Start the Development Server:

```bash
npm run dev
```

4. Access the App: Open your browser and go to http://localhost:8080

## Usage

1. Start both the backend and frontend servers.
2. Open the app in your browser.
3. Type a question about Jun and press Enter or click Submit.
4. View the response dynamically generated based on Jun's documents.

## Improvements

- **Tests**: Add unit tests for backend services and frontend components to ensure functionality and reliability.
- **CI/CD**: Add GitHub Actions for continuous integration and deployment to automate the testing and deployment process.
- **Error Handling:** Implement more robust error handling for API calls and edge cases.
- **UI/UX Enhancements:** Improve the user interface and user experience, such as adding loading indicators and better styling.
