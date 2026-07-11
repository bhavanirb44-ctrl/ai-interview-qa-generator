# AI Interview Q&A Generator

A complete Streamlit application that:
- Uploads PDF, DOCX, or TXT resumes
- Compares a resume with a job description
- Generates tailored interview questions
- Shows intent, difficulty, and ideal answer blueprints
- Runs a mock interview
- Evaluates candidate answers
- Generates a final interview report

## Setup

1. Create and activate a virtual environment.

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your API key:
```env
OPENAI_API_KEY=your_key_here
```

4. Run:
```bash
streamlit run app.py
```

## Notes

The default model is `gpt-4o-mini`. You can change it from the sidebar.
Your OpenAI API usage may incur charges depending on your account and model usage.
