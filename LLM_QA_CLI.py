"""
NLP Question-and-Answering System - CLI Application
Part A: Python CLI Application
"""

import re
import string
from openai import OpenAI
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

def query_llm(question, api_key):
    """
    Send question to DeepSeek LLM API and get response
    """
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
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
            model="deepseek-chat",
            temperature=0.7,
            max_tokens=1024,
        )
        
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """
    Main CLI application function
    """
    print("=" * 60)
    print("NLP Question-and-Answering System (CLI)")
    print("Powered by DeepSeek LLM API")
    print("=" * 60)
    print()
    
    # Get API key from environment variable or user input
    api_key = os.getenv('DEEPSEEK_API_KEY')
    
    if not api_key:
        print("DEEPSEEK_API_KEY not found in environment variables.")
        api_key = input("Please enter your DeepSeek API key: ").strip()
    
    if not api_key:
        print("Error: API key is required to run this application.")
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
        answer = query_llm(question, api_key)
        
        print("\n" + "=" * 60)
        print("ANSWER:")
        print("=" * 60)
        print(answer)
        print("=" * 60)
        print()

if __name__ == "__main__":
    main()
