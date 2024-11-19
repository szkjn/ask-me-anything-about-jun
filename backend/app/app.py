import logging
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from openai import OpenAI
import os
import json
import numpy as np
import faiss
import xml.etree.ElementTree as ET

from utils.config import (
    OPENAI_API_KEY,
    INDEX_FILE,
    FILENAMES_FILE,
    DATA_FOLDER,
    AnswerPath,
)
from utils.prompts import SYSTEM_PROMPT, ANSWER_PATH_ASSESSMENT_PROMPT

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Load recent activities from RSS feed
recent_activities = []
try:
    tree = ET.parse(os.path.join(DATA_FOLDER, "rss_feed.xml"))
    root = tree.getroot()

    # Assuming the RSS feed follows standard structure
    for item in root.findall("./channel/item"):
        activity = {
            "title": item.find("title").text,
            "description": item.find("description").text,
            "link": item.find("link").text,
            "pubDate": item.find("pubDate").text,
        }
        recent_activities.append(activity)

    logging.info("Recent activities loaded successfully from RSS feed.")
except Exception as e:
    logging.error(f"Failed to load recent activities: {e}")

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
    uploaded_recent_activities = False

    if not question:
        logging.warning("No question provided.")
        return jsonify({"error": "No question provided"}), 400

    try:
        # Append SYSTEM_PROMPT to the history at the beginning
        history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})

        # Quick assessment for recent activities
        assessment_message = ANSWER_PATH_ASSESSMENT_PROMPT + question

        assessment_response = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": assessment_message}],
            max_tokens=40,
            response_format=AnswerPath,
        )
        assessment_answer = assessment_response.choices[0].message.parsed
        logging.info(f"Answer Path Assessment: {assessment_answer.answer_path}")

        # Determine if the question is about recent activities
        if assessment_answer.answer_path == 1:

            context = "\n\n".join(
                activity["description"] for activity in recent_activities
            )

            if uploaded_recent_activities == False:
                prompt = f"Context: {context}\n\nQuestion: {question}"
            else:
                prompt = f"Refer to the context (recent activities) previously shared. Question: {question}"

            history.append({"role": "user", "content": prompt})

            uploaded_recent_activities = True
        else:
            # Generate embedding for the user question for document search
            response = client.embeddings.create(
                model="text-embedding-ada-002", input=question
            )
            query_embedding = np.array(
                response.data[0].embedding, dtype="float32"
            ).reshape(1, -1)

            # Perform similarity search for document embeddings
            distances, indices = index.search(
                query_embedding, k=3
            )  # Retrieve top 3 docs
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
                model="gpt-4o-mini", messages=history, max_tokens=1000, stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        return Response(
            generate(),
            content_type="text/event-stream",
            headers={"X-Complete-Answer": complete_answer},
        )

    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}")
        return (
            jsonify({"error": "An error occurred while processing the request."}),
            500,
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
