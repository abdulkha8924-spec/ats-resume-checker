# ats-resume-checker

# CareerCraft AI 💼🚀

An AI-powered career copilot built with **Streamlit** and **OpenAI**. It helps job seekers optimize their resumes, generate tailored cover letters, and practice live mock interviews.

## Features
- **📊 ATS Match & Critique:** Compares your resume against a target job description, gives an ATS score, and highlights missing keywords.
- **✨ Resume Bullet Generator:** Rewrites your experience section to naturally incorporate high-impact keywords.
- **✉️ Cover Letter Writer:** Instantly drafts a hyper-customized professional cover letter.
- **🤖 Mock Interviewer Chatbot:** Simulates a hiring manager asking targeted interview questions with real-time feedback.

## Deployment on Streamlit Cloud
1. Push these three files (`app.py`, `requirements.txt`, `README.md`) to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and deploy the repository.
3. In your Streamlit app settings under **Secrets**, add your OpenAI API key:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
