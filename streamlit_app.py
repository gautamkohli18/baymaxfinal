import streamlit as st
from streamlit_lottie import st_lottie
import google.generativeai as genai
import os
import requests
import time

st.set_page_config(layout="wide", page_title="Baymax - Friendly Neighborhood AI", page_icon="🤖")

# Function to load Lottie animations from a URL
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Set up the Google Generative AI API key
api_key = 'AIzaSyB3n1FTI2oiL_G7M7WqzdroNcQ-dJiFgyA'
os.environ["GOOGLE_API_KEY"] = api_key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-002",
    generation_config=generation_config,
)

# Start the chatbot session
chat_session = model.start_chat(history=[])

# Add the Lottie animation using HTML
lottie_html = """
<script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>
<div style="display: flex; justify-content: right; align-items: right; height: 500vh;">
    <dotlottie-player src="https://lottie.host/4ff3d5f4-1d6b-4f35-ac12-ac93de643c6e/3Ic3MV6yIu.lottie"
                      background="transparent" speed="1" style="width: 150px; height: 150px" loop autoplay>
    </dotlottie-player>
</div>
"""

st.components.v1.html(lottie_html, height=150, width=150)

# Streamlit app layout with custom styling for black font
st.markdown("""
    <h1 style='color: black; text-align: center;'>Baymax - Your friendly neighborhood AI</h1>
    <p style='color: black; text-align: center;'>Hello Human! I am Baymax. I am here to fetch you valuable information whenever you need some!</p>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
        .stApp {
            background: url('https://img.freepik.com/free-vector/pastel-ombre-background-pink-purple_53876-120750.jpg') no-repeat center center fixed;
            background-size: cover;
            height: 100vh;
        }
        .message-box {
            display: flex;
            margin: 10px 0;
        }
        .user-message {
            background-color: #74EBD5;
            background-image: linear-gradient(90deg, #74EBD5 0%, #9FACE6 100%);
            color: black;
            padding: 10px 20px;
            border-radius: 15px;
            margin-left: auto;
            max-width: 70%;
            word-wrap: break-word;
        }
        .ai-message {
            background-color: #4158D0;
            background-image: linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
            color: white;
            padding: 10px 20px;
            border-radius: 15px;
            max-width: 70%;
            word-wrap: break-word;
            white-space: pre-wrap;
        }
        input[type="text"] {
            background-color: white !important;
            color: black !important;
            border: 1px solid black !important;
            border-radius: 10px !important;
            padding: 10px !important;
        }
        .stButton>button {
            background-color: white !important;
            color: black !important;
            border: 1px solid black !important;
            border-radius: 10px !important;
            padding: 8px 16px !important;
        }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_message_displayed' not in st.session_state:
    st.session_state.last_message_displayed = True

# Typewriting effect function
def typewrite_effect(text):
    placeholder = st.empty()  # Create a placeholder
    typewritten_text = ""
    for char in text:
        typewritten_text += char
        placeholder.markdown(f'<div class="ai-message">{typewritten_text}</div>', unsafe_allow_html=True)
        time.sleep(0.006)  # Reduced sleep time for smoother typing effect
    placeholder.markdown(f'<div class="ai-message">{text}</div>', unsafe_allow_html=True)

# Handle input submission
def handle_input():
    user_input = st.session_state.user_input
    if user_input:
        # Append user input to history
        st.session_state.history.append({'role': 'user', 'text': user_input})
        response = chat_session.send_message(user_input)
        
        # Append AI response to history
        st.session_state.history.append({'role': 'chatbot', 'text': response.text})
        st.session_state.last_message_displayed = False  # Mark the latest message as not displayed yet
        
        # Clear the input box
        st.session_state.user_input = ""

# Display chat history
for idx, message in enumerate(st.session_state.history):
    if message['role'] == 'user':
        st.markdown(f'<div class="message-box"><div class="user-message">{message["text"]}</div></div>', unsafe_allow_html=True)
    elif idx == len(st.session_state.history) - 1 and not st.session_state.last_message_displayed:
        # Apply typewriting effect only to the most recent AI message
        typewrite_effect(message["text"])
        st.session_state.last_message_displayed = True
    else:
        # Display previous AI messages directly
        st.markdown(f'<div class="message-box"><div class="ai-message">{message["text"]}</div></div>', unsafe_allow_html=True)

# Input box for user to type their message
st.text_input("You:", key="user_input", placeholder="Type your message here...", on_change=handle_input)

# Button to reset the chat
if st.button('Reset Chat'):
    st.session_state.history = []
    st.session_state.last_message_displayed = True
    chat_session = model.start_chat(history=[])
    st.write("Chat has been reset.")
