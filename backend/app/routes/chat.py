from flask import Blueprint, request, jsonify, Response
from utils.prompts import SYSTEM_PROMPT
from services.openai_service import OpenAIService
from services.faiss_service import FaissService
from services.rss_service import RssService
import logging

chat_bp = Blueprint("chat", __name__)
openai_service = OpenAIService()
faiss_service = FaissService()
rss_service = RssService()


@chat_bp.route("/chat", methods=["POST"])
def chat() -> Response:
    """  
    Endpoint for handling chat requests. 
    
    Accepts a JSON payload with a question and optional history.
    
    Returns:
        Response: A streamed response from OpenAI based on the question and context.
    """
    logging.info("Received a new chat message")
    data = request.json
    question = data.get("question", "")
    history = data.get("history", [])

    if not question:
        logging.warning("No question provided.")
        return jsonify({"error": "No question provided"}), 400

    # Append SYSTEM_PROMPT to the history at the beginning
    history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})

    # Assess the 'Answer Path'
    assessment_answer = openai_service.assess_question(question)

    if assessment_answer == 1:
        context = "\n\n".join(
            activity["description"] for activity in rss_service.recent_activities
        )
    else:
        # Search for relevant documents using Faiss
        context = faiss_service.search_documents(question)

    history.append(
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
    )

    def generate() -> Response:
        """
        Generates a streamed response from OpenAI based on the question and context.

        Returns:
            Response: A streamed response from OpenAI.
        """
        stream = openai_service.generate_chat_response(history)
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    return Response(generate(), content_type="text/event-stream")
