from utils.logging import setup_logging

# Set up logging before importing other modules
setup_logging()

from flask import Flask
from flask_cors import CORS
from routes.chat import chat_bp

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Register Blueprints
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
