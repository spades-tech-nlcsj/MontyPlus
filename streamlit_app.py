import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Set API key for Generative AI
os.environ['API_KEY'] = st.secrets['API_KEY']
api_key = os.getenv('API_KEY')

genai.configure(api_key=api_key)

# Configuration for generative AI
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 2000,
    "response_mime_type": "text/plain",
}

# Load custom CSS for better UI
def load_css():
    st.markdown(
        """
        <style>
            .chat-container {
                background-color: #1E293B;
                padding: 20px;
                border-radius: 12px;
                color: white;
            }
            .user-message {
                background-color: #3B82F6;
                padding: 12px;
                border-radius: 12px;
                color: white;
                text-align: right;
                margin-bottom: 10px;
                display: inline-block;
                float: right;
                clear: both;
            }
            .assistant-message {
                background-color: #334155;
                padding: 12px;
                border-radius: 12px;
                color: white;
                text-align: left;
                margin-bottom: 10px;
                display: inline-block;
                float: left;
                clear: both;
            }
            .chat-header {
                text-align: center;
                color: white;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to load custom avatar
@st.cache_resource
def load_icon():
    img = Image.open("data/montyface.png")
    return img

# Initialize chat session
if "message_history" not in st.session_state:
    st.session_state.message_history = []

# Create Generative Model session
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)
chat_session = model.start_chat(
    history=st.session_state.message_history
)

# Streamlit UI Setup
st.title("Monty+")
st.subheader("Your Virtual Chat Companion")
load_css()

# Chat message display
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for message in st.session_state.message_history:
    if message['role'] == 'user':
        st.markdown(
            f"<div class='user-message'>{message['parts']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='assistant-message'>{message['parts']}</div>",
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)

# User input and response handling
user_input = st.text_input("Type your message here...")
if user_input:
    # Display user message
    st.session_state.message_history.append({"role": "user", "parts": user_input})

    # Generate assistant response
    response = chat_session.send_message(user_input)

    # Display assistant message
    st.session_state.message_history.append({"role": "assistant", "parts": response.text})
    st.experimental_rerun()
