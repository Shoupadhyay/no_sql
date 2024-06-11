from chroma_integration import ChromaDBIntegration

import logging

from flask import Flask, render_template, session
from flask_session import Session
from gunicorn.app.base import BaseApplication

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app_init import app

from abilities import llm_prompt
from flask import request, jsonify
import os
from langchain_integration import LangChainIntegration
from sentence_transformers import SentenceTransformer
import pinecone
from langchain import LangChain

@app.route("/")
def root_route():
    return render_template("template.html")
from app import *
@app.route("/send_message", methods=['POST'])
def send_message():
    user_message = request.json['message']
    # Implementing conversation history handling
    if 'history' not in session:
        session['history'] = []
    session['history'].append({"user": user_message})
    # Limit conversation history to the last 10 messages (5 user, 5 chatbot)
    if len(session['history']) > 10:
        session['history'] = session['history'][-10:]
    conversation_history = " ".join([f"user: {msg.get('user', '')} bot: {msg.get('bot', '')}" for msg in session['history']])
    
    # Initialize LangChainIntegration and SentenceTransformer
    langchain_integration = LangChainIntegration()
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # Vectorize the user message
    user_vector = model.encode(user_message)
    
    # Retrieve the nearest vector from Pinecone
    # Initialize ChromaDB
    chromadb_client = ChromaDBIntegration()
    query_response = chromadb_client.query_collection(user_message)
    
    if query_response['results']:
        nearest_vector = query_response['results'][0]['vector']
        nearest_text = query_response['results'][0]['metadata']['text']
        response = langchain_integration.ask_question(nearest_text)
    else:
        response = "No relevant information found."
    
    session['history'].append({"bot": response})
    return jsonify({"message": response})


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


# Do not remove the main function while updating the app.
def initialize():
    pass
