import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from src.config.db import init_db
from src.routes.cart_routes import cart_routes

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://frontend-url"])

app.register_blueprint(cart_routes)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))