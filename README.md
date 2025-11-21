# NLP Question-and-Answering System

## Project Overview
A comprehensive Question-and-Answering (Q&A) system powered by Groq LLM API with both CLI and Web GUI interfaces.

**Course:** COS331 - Artificial Intelligence  
**Project:** Part 2 - NLP Question-and-Answering System  
**Date:** November 21, 2025

## Features

### Part A - CLI Application (`LLM_QA_CLI.py`)
- ✅ Accept natural-language questions from users
- ✅ Apply NLP preprocessing (lowercasing, tokenization, punctuation removal)
- ✅ Send questions to Groq LLM API
- ✅ Display processed questions and answers
- ✅ Interactive command-line interface

### Part B - Web GUI Application (`app.py`)
- ✅ Beautiful, responsive web interface
- ✅ Enter questions via web form
- ✅ View processed questions and tokens
- ✅ Display LLM API responses
- ✅ Real-time answer generation
- ✅ Error handling and validation

## Project Structure
```
/NLP/
├── LLM_QA_CLI.py                 # CLI Application
├── app.py                        # Flask Web Application
├── requirements.txt              # Python dependencies
├── LLM_QA_hosted_webGUI_link.txt # Deployment information
├── README.md                     # This file
├── /static/
│   └── style.css                 # CSS styling
└── /templates/
    └── index.html                # HTML template
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Groq API key (free at https://console.groq.com/)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Up API Key
You have two options:

**Option 1: Environment Variable (Recommended)**
```bash
# Windows PowerShell
$env:GROQ_API_KEY="your_api_key_here"

# Windows CMD
set GROQ_API_KEY=your_api_key_here

# Linux/Mac
export GROQ_API_KEY=your_api_key_here
```

**Option 2: Enter at Runtime**
- CLI: Enter when prompted
- Web GUI: Enter in the form field

### Step 3: Get Your Groq API Key
1. Visit https://console.groq.com/
2. Sign up for a free account
3. Navigate to API Keys section
4. Generate a new API key
5. Copy and save it securely

## Usage

### Running the CLI Application
```bash
python LLM_QA_CLI.py
```

**CLI Features:**
- Enter questions at the prompt
- View preprocessing steps (tokens, lowercasing)
- See LLM responses
- Type `exit`, `quit`, or `q` to end session

### Running the Web GUI Application
```bash
python app.py
```

Then open your browser to: `http://localhost:5000`

**Web GUI Features:**
- Enter your API key (if not in environment)
- Type your question in the text area
- Click "Ask Question" or press Enter
- View results including:
  - Original question
  - Processed question
  - Extracted tokens
  - LLM-generated answer

## Deployment

### Recommended Platforms:
1. **Render.com** (Easiest)
2. **PythonAnywhere.com**
3. **Streamlit Cloud**
4. **Vercel**

### Deployment Steps for Render.com:

1. **Create Account**
   - Go to https://render.com
   - Sign up for free

2. **Connect GitHub**
   - Push your code to GitHub
   - Connect your GitHub account to Render

3. **Create Web Service**
   - Click "New +"
   - Select "Web Service"
   - Connect your repository

4. **Configure Service**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment Variables:**
     - Key: `GROQ_API_KEY`
     - Value: Your API key

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment
   - Copy your live URL

### Deployment Steps for PythonAnywhere:

1. **Create Account**
   - Go to https://www.pythonanywhere.com
   - Sign up for free

2. **Upload Files**
   - Use "Files" tab to upload your project
   - Or clone from GitHub in a bash console

3. **Install Dependencies**
   ```bash
   pip install --user -r requirements.txt
   ```

4. **Create Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose Flask
   - Select Python version

5. **Configure WSGI**
   - Edit WSGI configuration file
   - Point to your `app.py`

6. **Set Environment Variable**
   - Add GROQ_API_KEY in WSGI file or virtualenv

7. **Reload**
   - Click "Reload" button
   - Visit your URL

## Testing

### Test the CLI:
```bash
python LLM_QA_CLI.py
```
Example questions:
- "What is artificial intelligence?"
- "Explain machine learning in simple terms"
- "What are the benefits of Python?"

### Test the Web GUI:
1. Run `python app.py`
2. Open http://localhost:5000
3. Enter a question
4. Verify all sections display correctly

## NLP Preprocessing

The system applies the following preprocessing steps:
1. **Lowercasing:** Converts text to lowercase
2. **Tokenization:** Splits text into individual words
3. **Punctuation Removal:** Removes punctuation marks

## Technologies Used

- **Backend:** Flask (Python web framework)
- **LLM API:** Groq (with Llama 3 model)
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** Gunicorn (WSGI server)

## API Information

**LLM Provider:** Groq  
**Model:** llama3-8b-8192  
**API Documentation:** https://console.groq.com/docs

**Why Groq?**
- Fast inference speed
- Free tier available
- High-quality responses
- Easy to use API

## Troubleshooting

### Common Issues:

**1. API Key Error**
```
Error: API key is required
```
**Solution:** Set GROQ_API_KEY environment variable or enter in the form

**2. Module Not Found**
```
ModuleNotFoundError: No module named 'groq'
```
**Solution:** Run `pip install -r requirements.txt`

**3. Port Already in Use**
```
Address already in use
```
**Solution:** Change port in app.py or kill the process using port 5000

**4. Connection Error**
```
Error: Connection refused
```
**Solution:** Check your internet connection and API key validity

## Project Requirements Checklist

### Part A - CLI ✅
- [x] Accept natural-language questions
- [x] Apply preprocessing (lowercasing, tokenization, punctuation removal)
- [x] Send to LLM API
- [x] Display answer

### Part B - Web GUI ✅
- [x] Enter questions via form
- [x] View processed question
- [x] See LLM API response
- [x] Display generated answer
- [x] Flask + HTML/CSS implementation

### Part C - Deployment ✅
- [x] Deployment instructions provided
- [x] Multiple platform options documented
- [x] LLM_QA_hosted_webGUI_link.txt created

### Part D - Project Structure ✅
- [x] LLM_QA_CLI.py
- [x] app.py
- [x] requirements.txt
- [x] LLM_QA_hosted_webGUI_link.txt
- [x] /static/style.css
- [x] /templates/index.html

## Submission Instructions

1. **Update LLM_QA_hosted_webGUI_link.txt**
   - Add your name and matric number
   - Add deployed application URL
   - Add GitHub repository link

2. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: NLP Q&A System"
   git branch -M main
   git remote add origin https://github.com/yourusername/LLM_QA_Project.git
   git push -u origin main
   ```

3. **Submit to Scorac.com**
   - Zip the entire project folder
   - Submit before deadline: November 21, 2025, 12:00 PM

## Contact & Support

For issues or questions about this project:
- Check the README documentation
- Review the code comments
- Test locally before deployment
- Verify API key is valid

## License

This project is created for educational purposes as part of COS331 - Artificial Intelligence course at Covenant University.

---

**Built with ❤️ for COS331 - Artificial Intelligence**  
**Covenant University | November 2025**
