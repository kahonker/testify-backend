from flask import Flask
from flask_cors import CORS
from config import Config

app = Flask(__name__)

CORS(app, origins=["http://localhost:5173"])

app.config.from_object(Config)

from app import routes

