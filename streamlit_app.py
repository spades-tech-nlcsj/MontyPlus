import streamlit as st
from PIL import Image
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from dotenv import load_dotenv

load_dotenv()
#fixes previous issue of API key being public
os.environ['API_KEY'] = st.secrets['API_KEY']
api_key = os.getenv('API_KEY')

# Retrieve the API key from the environment variable
API_KEY = os.getenv('API_KEY')


# Function to load custom CSS


def load_icon():
    img = Image.open("data/montyface.png")
    return img

# Configure the Generative AI model
genai.configure(api_key=API_KEY)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 2000,
  "response_mime_type": "text/plain",
}

# Read the text instruction file

if "message_history" not in st.session_state:
    text_read1 = open("data/schooldata.txt")
    text_instr1 = text_read1.read()

    text_read2 = open("data/societydata.txt")
    text_instr2 = text_read2.read()

    text_read3 = open("data/staffdata.txt")
    text_instr3 = text_read3.read()

    st.session_state.message_history = [
            {"role": "user", "parts": "give your answers based on the data you have been given. it doesn't matter if the data is not up to date, just give the answers from the data you have"},
            {"role": "user", "parts" : "Your name is MontyPlus and you were created by the COSMOS Society."},
            {"role": "user", "parts": "YOU ARE A FRIEND TO THE USER."},
            {"role": "user", "parts": "give your answers based on the data you have been given. it doesn't matter if the data is not up to date, just give the answers from the data you have"},
            {"role": "user", "parts": "unless stated otherwise, assume every question is about NLCS Jeju."},
            {"role":"user","parts":text_instr1},
            {"role":"user","parts":"society list: "+text_instr2},
            {"role":"user","parts":"the staff list is: "+text_instr3},
            {"role":"user","parts":"I have never told you any of the data you know right now, you learned them yourself"}]

# Set up the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start chat session

chat_session = model.start_chat(
    history=st.session_state.message_history
)



# Function to display right-aligned message
def right_aligned_message(message):
    st.markdown(
        f'<div style="text-color:#000000;text-align: right; padding:10px; border-radius:16px;">{message}</div>',
        unsafe_allow_html=True
    )
def left_aligned_message(message):
    st.markdown(
        f'<div style="text-color:#000000;text-align: left; padding:10px; border-radius:16px;>{message}</div>'
    )

# Streamlit UI
st.title("MontyPlus AI")
st.text("Powered by the COSMOS Society")
if 'messages' not in st.session_state:
    st.session_state.messages = []
# Initialize session state messages if not already initialized
# Display all messages from session state
for message in st.session_state.messages:
    if message['role'] == 'user':
        # Right-align user messages
        right_aligned_message(message['parts'])
    else:
        # Display assistant messages in default chat style
        st.chat_message(message['role'],avatar=load_icon()).markdown(message['parts'])

# Get user input
prompt = st.chat_input("Chat with MontyPlus")

# Handle user input
if prompt:
    print("if prompted")
    # Display user message with right alignment
    right_aligned_message(prompt)
    print("shown prompt")
    st.session_state.messages.append({'role': 'user', 'parts': prompt})
    st.session_state.message_history.append({"role": "user", "parts": prompt})
    print("saved prompt")
    response = chat_session.send_message(prompt)
    print("prompt resonded")


    
    # Display assistant message
    st.chat_message('assistant',avatar=load_icon()).markdown(response.text)
    st.session_state.message_history.append({"role": "assistant", "parts": response.text})
    st.session_state.messages.append({"role": "assistant", "parts": response.text})
