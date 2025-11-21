"""
NLP Question-and-Answering System - Web GUI Application
Part B: Flask Web Application
"""

from flask import Flask, render_template, request, jsonify
import re
import string
from groq import Groq
import os

app = Flask(__name__)

# Get API key from environment variable
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

def preprocess_text(text):
    """
    Apply basic NLP preprocessing:
    - Lowercasing
    - Tokenization
    - Punctuation removal
    """
    # Lowercasing
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenization (split into words)
    tokens = text.split()
    
    # Join tokens back
    processed_text = ' '.join(tokens)
    
    return processed_text, tokens

def query_llm(question, api_key):
    """
    Send question to Groq LLM API and get response
    """
    try:
        client = Groq(api_key=api_key)
        
        # Create chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides clear and accurate answers to questions."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            model="llama3-8b-8192",  # Using Llama 3 model on Groq
            temperature=0.7,
            max_tokens=1024,
        )
        
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    """
    Render the main page
    """
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    """
    Handle question submission and return answer
    """
    data = request.get_json()
    question = data.get('question', '').strip()
    api_key = data.get('api_key', GROQ_API_KEY).strip()
    
    if not question:
        return jsonify({
            'error': 'Please enter a valid question.'
        }), 400
    
    if not api_key:
        return jsonify({
            'error': 'API key is required. Please set GROQ_API_KEY environment variable or provide it in the form.'
        }), 400
    
    # Preprocess the question
    processed_question, tokens = preprocess_text(question)
    
    # Query the LLM
    answer = query_llm(question, api_key)
    
    return jsonify({
        'original_question': question,
        'processed_question': processed_question,
        'tokens': tokens,
        'answer': answer
    })

if __name__ == '__main__':
    # Run the Flask app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
