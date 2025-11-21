"""
NLP Question-and-Answering System - Web GUI Application
Part B: Flask Web Application
"""

from flask import Flask, render_template, request, jsonify
import re
import string
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get API token from environment variable
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN', '')

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

def query_llm(question, api_token):
    """
    Send question to HuggingFace Inference API using Qwen/Qwen2.5-0.5B-Instruct model
    """
    import time
    
    # Try multiple models as fallback
    models = [
        "Qwen/Qwen2.5-0.5B-Instruct",
        "tiiuae/falcon-7b-instruct",
        "HuggingFaceH4/zephyr-7b-beta"
    ]
    
    for model in models:
        try:
            API_URL = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": f"Bearer {api_token}"}
            
            payload = {
                "inputs": question,
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.7,
                    "do_sample": True
                },
                "options": {"wait_for_model": True}
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            # If we get a 503, the model might be loading
            if response.status_code == 503:
                result = response.json()
                if 'estimated_time' in result:
                    wait_time = min(result['estimated_time'], 20)
                    time.sleep(wait_time)
                    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            # Skip this model if it returns 410
            if response.status_code == 410:
                continue
                
            response.raise_for_status()
            result = response.json()
            
            # Handle the response format
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get('generated_text', '')
                # Clean up the response - remove the input question if it's repeated
                if text.startswith(question):
                    text = text[len(question):].strip()
                return text if text else str(result)
            elif isinstance(result, dict):
                if 'error' in result:
                    continue
                return result.get('generated_text', str(result))
            else:
                return str(result)
                
        except requests.exceptions.RequestException:
            continue
    
    return "Error: Unable to get response from any available models. Please check your API token or try again later."

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
    
    if not question:
        return jsonify({
            'error': 'Please enter a valid question.'
        }), 400
    
    if not HUGGINGFACE_API_TOKEN:
        return jsonify({
            'error': 'API token not configured. Please set HUGGINGFACE_API_TOKEN in .env file.'
        }), 400
    
    # Preprocess the question
    processed_question, tokens = preprocess_text(question)
    
    # Query the LLM
    answer = query_llm(question, HUGGINGFACE_API_TOKEN)
    
    return jsonify({
        'original_question': question,
        'processed_question': processed_question,
        'tokens': tokens,
        'answer': answer
    })

if __name__ == '__main__':
    # Run the Flask app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
