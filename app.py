import os
import streamlit as st
from groq import Groq
import PyPDF2

# Page Config
st.set_page_config(page_title="CareerCraft AI", page_icon="💼", layout="wide")

# Initialize Groq Client
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = os.getenv("GROQ_API_KEY", "")

if not api_key:
    st.error("🚨 Groq API Key not found! Please configure it in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# Helper function to read uploaded PDF
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# UI Header
st.title("💼 CareerCraft AI Copilot")
st.markdown("Supercharge your job hunt with lightning-fast AI powered by **Groq** and **Llama 3**.")

# Sidebar for Inputs
with st.sidebar:
    st.header("1. Input Details")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_description = st.text_area("Paste Job Description Here", height=200)
    
    model_choice = st.selectbox(
        "Choose Groq Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
    )

# Extract resume text if available
resume_text = extract_text_from_pdf(uploaded_file) if uploaded_file else ""

# Main Dashboard Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 ATS Match", 
    "✨ Bullet Generator", 
    "✉️ Cover Letter", 
    "🤖 Mock Interview"
])

# --- TAB 1: ATS Match & Critique ---
with tab1:
    st.subheader("Resume vs. Job Description Match")
    if st.button("Analyze ATS Score"):
        if not resume_text or not job_description:
            st.warning("Please upload a resume and enter a job description in the sidebar.")
        else:
            with st.spinner("Analyzing resume compatibility..."):
                prompt = f"""
                You are an expert technical recruiter. Analyze the candidate resume against the job description.
                
                RESUME:
                {resume_text}
                
                JOB DESCRIPTION:
                {job_description}
                
                Provide:
                1. ATS Match Score (Out of 100).
                2. Missing critical keywords.
                3. 3 specific recommendations to improve resume bullet points.
                """
                try:
                    response = client.chat.completions.create(
                        model=model_choice,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3
                    )
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Groq API Error: {e}")

# --- TAB 2: Tailored Resume Bullet Generator ---
with tab2:
    st.subheader("Targeted Resume Bullet Rewriter")
    if st.button("Rewrite Experience Bullets"):
        if not resume_text or not job_description:
            st.warning("Please provide both resume and job description.")
        else:
            with st.spinner("Optimizing bullet points..."):
                prompt = f"""
                Take the experience section from this resume and rewrite the bullet points so they align strongly with the target job description, using action verbs and quantifiable metrics where possible.
                
                RESUME:
                {resume_text}
                
                JOB DESCRIPTION:
                {job_description}
                """
                try:
                    response = client.chat.completions.create(
                        model=model_choice,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.5
                    )
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Groq API Error: {e}")

# --- TAB 3: Targeted Cover Letter Writer ---
with tab3:
    st.subheader("Custom Cover Letter Generator")
    tone = st.selectbox("Select Tone", ["Professional", "Enthusiastic", "Concise"])
    if st.button("Generate Cover Letter"):
        if not resume_text or not job_description:
            st.warning("Please provide both resume and job description.")
        else:
            with st.spinner("Drafting cover letter..."):
                prompt = f"""
                Write a tailored cover letter based on this resume and job description. Tone: {tone}.
                
                RESUME:
                {resume_text}
                
                JOB DESCRIPTION:
                {job_description}
                """
                try:
                    response = client.chat.completions.create(
                        model=model_choice,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7
                    )
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Groq API Error: {e}")

# --- TAB 4: Mock Interviewer Chatbot ---
with tab4:
    st.subheader("Mock Interview Prep")
    st.markdown("Practice answering interview questions tailored to the job description.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Answer the interviewer or ask a question..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                system_prompt = f"You are a tough technical hiring manager interviewing a candidate for this job: {job_description}. Evaluate their answers and ask follow-ups."
                messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages
                
                try:
                    response = client.chat.completions.create(
                        model=model_choice,
                        messages=messages,
                        temperature=0.5
                    )
                    ai_response = response.choices[0].message.content
                    st.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                except Exception as e:
                    st.error(f"Groq API Error: {e}")
