import os
import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="Web Content Q&A", layout="wide")

st.title("🔍 Web Content Q&A Tool")
st.write("Enter a URL, ingest the content, and ask questions!")

# Initialize session state
if "url_ingested" not in st.session_state:
    st.session_state.url_ingested = False

# Input Fields
url = st.text_input("🌍 Enter URL to Ingest:")
question = st.text_input("❓ Ask a Question:")

# Use environment variable for API URL (or fallback to localhost for testing)
API_URL = os.getenv("API_URL", "http://localhost:8000")  # Change this to your backend URL after deployment

# Ingest URL
if st.button("🚀 Ingest URL"):
    if not url:
        st.error("❌ Please enter a URL.")
    else:
        try:
            response = requests.post(f"{API_URL}/ingest", json={"url": url})
            if response.status_code == 200:
                st.session_state.url_ingested = True  # Mark URL as ingested
                st.success("✅ URL successfully ingested!")
                st.text(f"Preview: {response.json().get('preview', 'No content')[:300]}")
            else:
                st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"⚠️ Request failed: {str(e)}")

# Ask Question
if st.button("🤖 Get Answer"):
    if not question:
        st.error("❌ Please enter a question.")
    elif not st.session_state.url_ingested:  # Check if URL has been ingested
        st.error("❌ No content ingested. Please ingest a URL first.")
    else:
        try:
            response = requests.post(f"{API_URL}/ask", json={"question": question})
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer found")
                st.success(f"**📝 Answer:** {answer}")
            else:
                st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"⚠️ Request failed: {str(e)}")