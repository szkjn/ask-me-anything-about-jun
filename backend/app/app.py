import logging
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from openai import OpenAI
import os
import json
import numpy as np
import faiss
from utils.config import OPENAI_API_KEY, INDEX_FILE, FILENAMES_FILE, DATA_FOLDER
from utils.prompts import SYSTEM_PROMPT

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(
    level=logging.INFO,
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
    for filename in filenames:
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


@app.route("/chat", methods=["POST"])
def chat():
    logging.info("Received a new chat message")
    data = request.json
    question = data.get("question", "")
    history = data.get("history", [])

    if not question:
        logging.warning("No question provided.")
        return jsonify({"error": "No question provided"}), 400

    try:
        # Append SYSTEM_PROMPT to the history at the beginning
        history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        
        # Generate embedding for the question
        response = client.embeddings.create(
            model="text-embedding-ada-002", input=question
        )
        query_embedding = np.array(response.data[0].embedding, dtype="float32").reshape(
            1, -1
        )

        # Perform similarity search
        distances, indices = index.search(query_embedding, k=3)  # Retrieve top 3 docs
        retrieved_docs = [filenames[idx] for idx in indices[0]]
        context = "\n\n".join(
            [document_map[doc] for doc in retrieved_docs if doc in document_map]
        )

        # Append context to chat history
        history.append(
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        )

        # Initialize an empty string to accumulate the assistant's response
        complete_answer = ""

        def generate():
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=history,
                max_tokens=1000,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content)
                    yield chunk.choices[0].delta.content

        print("Streaming response...")
        print(Response(generate(), content_type='text/event-stream'))
        # Run the generator
        return Response(generate(), content_type='text/event-stream', headers={"X-Complete-Answer": complete_answer})



        # # Generate answer using ChatCompletion with history
        # chat_response = client.beta.chat.completions.parse(
        #     model="gpt-4o-mini", messages=history, max_tokens=1000
        # )
        # answer = chat_response.choices[0].message.content.strip()

        # # Add assistant's response to the history
        # history.append({"role": "assistant", "content": answer})
        # logging.info("Chat response generated successfully.")
        # return jsonify({"answer": answer, "history": history})

    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}")
        return (
            jsonify({"error": "An error occurred while processing the request."}),
            500,
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
