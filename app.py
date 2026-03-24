import streamlit as st
import google.generativeai as genai
import os

# --- CONFIGURATION ---
# Replace with your key or use a .env file
API_KEY = "AIzaSyC40hJ9F-gKs8zVEcDRn4Sd3a-tC8DaTHE" 
genai.configure(api_key=API_KEY)

# Use Flash for the Free Tier (High limits)
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="Personal Researcher", layout="wide")
st.title("🕵️‍♂️ AI Personal Researcher")

# --- SIDEBAR: Document Upload ---
with st.sidebar:
    st.header("Research Material")
    uploaded_files = st.file_uploader("Upload PDFs or Text files", type=['pdf', 'txt'], accept_multiple_files=True)
    process_button = st.button("Analyze Documents")

# --- MAIN INTERFACE ---
query = st.text_input("What would you like me to find or summarize?")

if process_button and uploaded_files:
    with st.spinner("Reading documents..."):
        # Combine text from files
        combined_text = ""
        for file in uploaded_files:
            combined_text += f"\n--- Source: {file.name} ---\n"
            combined_text += file.read().decode("utf-8")
        
        # The "Research" Prompt
        prompt = f"""
        You are a professional research assistant. 
        Below are documents provided by the user. 
        Your task: Answer the following question based ONLY on the provided text.
        If the answer isn't there, say you can't find it.
        
        Question: {query}
        
        Documents:
        {combined_text}
        """
        
        response = model.generate_content(prompt)
        st.subheader("Research Findings:")
        st.write(response.text)