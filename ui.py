import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/ideas")

st.set_page_config(page_title="Idea Tracker", page_icon="💡")
st.title("💡 Idea Tracker")

st.header("Submit a New Idea")
with st.form("idea_form"):
    title = st.text_input("Title")
    description = st.text_area("Description")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if title:
            try:
                response = requests.post(API_URL, json={"title": title, "description": description})
                if response.status_code == 200:
                    st.success("Idea submitted successfully!")
                else:
                    st.error(f"Failed to submit idea. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error connecting to API: {e}")
        else:
            st.warning("Title is required.")

st.header("All Ideas")
if st.button("Refresh Ideas"):
    st.rerun()

try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        ideas = response.json()
        if ideas:
            for idea in ideas:
                with st.expander(f"{idea['id']}: {idea['title']}"):
                    st.write(idea['description'] or "No description provided.")
        else:
            st.info("No ideas found. Submit one above!")
    else:
        st.error("Failed to fetch ideas.")
except Exception as e:
    st.error(f"Could not connect to the API. Ensure FastAPI is running on {API_URL}. Error: {e}")
