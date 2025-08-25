import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")

st.set_page_config(page_title="Flight Booking Agent", page_icon="✈️")

if "messages" not in st.session_state:
    st.session_state.messages = []

#Send input to backend
def send_message(message):
    try:
        response = requests.post(
            f"{BACKEND_URL}/agent",
            json={"input": message}
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response from server.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return "Error occurred while sending message."
    
# UI Layout
st.title('Flight Booking Agent')
st.subheader("Powered by FastAPI & Streamlit")

#Container for chat history
chat_container = st.container()

# Create form for message input
with st.form(key='message_form', clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Type your message here...", key='user_input')
    with col2:
        submit_button = st.form_submit_button("Send")

    # Handle form submission
    if submit_button and user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Send message to backend and get response
        response = send_message(user_input)
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "bot", "content": response})

# Display chat history
with chat_container:
    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.markdown(
                f"""
                <div style='background-color: #black; color: #ffffff; padding: 10px; border-radius: 10px; margin: 5px;'>
                    <strong>You:</strong> {message['content']}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='background-color: #black; color: #ffffff; padding: 10px; border-radius: 10px; margin: 5px;'>
                    <strong>Bot:</strong> {message['content']}
                </div>
                """,
                unsafe_allow_html=True
            )

# Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()  # Refresh the app to clear the chat display

#Add footer
st.markdown("""
---
Made with ❤️ by [Arinda](https://github.com/blaxpyda)
""")