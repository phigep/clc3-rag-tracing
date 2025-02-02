import streamlit as st
import requests

# API endpoint
API_URL = "http://34.69.39.243/ask_question"

st.title("Q&A App")

# User input
query = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if query:
        # Make API request
        response = requests.get(f"{API_URL}?query={query}", headers={"accept": "application/json"})
        if response.status_code == 200:
            answer = response.json()
            st.text_area("Answer:", answer, height=100,)
        else:
            st.error("Failed to fetch answer. Please try again.")
    else:
        st.warning("Please enter a question.")
