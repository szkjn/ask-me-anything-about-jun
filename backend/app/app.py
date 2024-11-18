import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import json
import numpy as np
import faiss
from utils.config import OPENAI_API_KEY, INDEX_FILE, FILENAMES_FILE, DATA_FOLDER

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize OpenAI client
try:
    client = OpenAI(api_key=OPENAI_API_KEY)
    logging.info("OpenAI client initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize OpenAI client: {e}")
    raise e

# Load FAISS index
try:
    index = faiss.read_index(INDEX_FILE)
    logging.info("FAISS index loaded successfully")
except Exception as e:
    logging.error(f"Failed to load FAISS index: {e}")
    raise e

# Load filenames mapping and document content
try:
    with open(FILENAMES_FILE, "r") as f:
        filenames = json.load(f)
    logging.info("Filenames mapping loaded successfully.")

    # Load all documents into a dictionary for mapping filenames to content
    document_map = {}
    for filename in filenames:  # filenames is from filenames.json
        file_path = os.path.join(DATA_FOLDER, filename)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                document_map[filename] = file.read()
        else:
            logging.warning(f"Document {filename} does not exist in {DATA_FOLDER}.")

    logging.info("Document content loaded successfully.")

except Exception as e:
    logging.error(f"Failed to load filenames or document content: {e}")
    raise e


@app.route("/ask", methods=["POST"])
def ask():
    logging.info("Received a new question")
    data = request.json
    question = data.get("question", "")

    if not question:
        logging.warning("No question provided.")
        return jsonify({"error": "No question provided"}), 400

    try:
        # Generate embedding for the question
        logging.debug("Generating embedding for the question...")
        response = client.embeddings.create(
            model="text-embedding-ada-002", input=question
        )
        query_embedding = np.array(response.data[0].embedding, dtype="float32").reshape(
            1, -1
        )
        logging.debug("Query embedding generated successfully.")

        # Perform similarity search
        logging.debug("Performing FAISS similarity search.")
        distances, indices = index.search(query_embedding, k=1)
        retrieved_docs = [filenames[idx] for idx in indices[0]]
        logging.info(f"Retrieved document(s): {retrieved_docs}")

        # Combine retrieved document(s) into context
        context = context = "\n\n".join(
            [document_map[doc] for doc in retrieved_docs if doc in document_map]
        )

        # Construct messages for OpenAI ChatCompletion
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant with access to Jun's documents. Keep your answers below 500 tokens.",
            },
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"},
        ]

        # Generate answer using ChatCompletion
        chat_response = client.beta.chat.completions.parse(
            model="gpt-4o-mini", messages=messages, max_tokens=1000
        )
        answer = chat_response.choices[0].message.content.strip()
        logging.info("Answer generated successfully.")
        return jsonify({"answer": answer})

    except Exception as e:
        logging.error(f"Error in /ask endpoint: {e}")
        return (
            jsonify({"error": "An error occurred while processing the request."}),
            500,
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
