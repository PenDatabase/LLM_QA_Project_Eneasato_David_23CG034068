"""
NLP Question-and-Answering System - CLI Application
Part A: Python CLI Application
"""

import re
import string
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    Send question to HuggingFace Inference API with fallback models
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
                    print(f"Model {model} is loading, waiting...")
                    wait_time = min(result['estimated_time'], 20)
                    time.sleep(wait_time)
                    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            # Skip this model if it returns 410
            if response.status_code == 410:
                print(f"Model {model} is not available (410), trying next...")
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
                
        except requests.exceptions.RequestException as e:
            print(f"Error with model {model}: {str(e)}")
            continue
    
    return "Error: Unable to get response from any available models. Please check your API token or try again later."

def main():
    """
    Main CLI application function
    """
    print("=" * 60)
    print("NLP Question-and-Answering System (CLI)")
    print("Powered by HuggingFace Inference API")
    print("=" * 60)
    print()
    
    # Get API token from environment variable or user input
    api_token = os.getenv('HUGGINGFACE_API_TOKEN')
    
    if not api_token:
        print("HUGGINGFACE_API_TOKEN not found in environment variables.")
        api_token = input("Please enter your HuggingFace API token: ").strip()
    
    if not api_token:
        print("Error: API token is required to run this application.")
        return
    
    print("\nType 'exit' or 'quit' to end the session.\n")
    
    while True:
        # Get user question
        question = input("Enter your question: ").strip()
        
        # Check for exit command
        if question.lower() in ['exit', 'quit', 'q']:
            print("\nThank you for using the Q&A system. Goodbye!")
            break
        
        if not question:
            print("Please enter a valid question.\n")
            continue
        
        print("\n" + "-" * 60)
        print("Processing your question...")
        print("-" * 60)
        
        # Preprocess the question
        processed_question, tokens = preprocess_text(question)
        
        print(f"\nOriginal Question: {question}")
        print(f"Processed Question: {processed_question}")
        print(f"Tokens: {tokens}")
        print("\nQuerying LLM API...")
        
        # Query the LLM
        answer = query_llm(question, api_token)
        
        print("\n" + "=" * 60)
        print("ANSWER:")
        print("=" * 60)
        print(answer)
        print("=" * 60)
        print()

if __name__ == "__main__":
    main()
