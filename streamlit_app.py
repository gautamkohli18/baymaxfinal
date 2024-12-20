import streamlit as st
from streamlit_lottie import st_lottie
import google.generativeai as genai
import os
import requests

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
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Start the chatbot session
chat_session = model.start_chat(history=[])

# Add the Lottie animation with transparent background using HTML
# Add the Lottie animation with transparent background and centered alignment using HTML
lottie_html = """
<script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>
<div style="display: flex; justify-content: right; align-items: right; height: 500vh;">
    <dotlottie-player src="https://lottie.host/4ff3d5f4-1d6b-4f35-ac12-ac93de643c6e/3Ic3MV6yIu.lottie" 
                      background="transparent" speed="1" style="width: 150px; height: 150px" loop autoplay>
    </dotlottie-player>
</div>
"""

st.components.v1.html(lottie_html, height=150, width=150)



# Streamlit app layout
st.title("Baymax - Your friendly neighborhood AI")
st.write("Hello Human! I am Baymax. I am here to fetch you valuable information whenever you need some!")

# Load and display the Lottie animation

# Add custom CSS to style the background and chat interface
st.markdown("""
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #111;
            color: #fff;
        }
        
        .stApp {
            background: url('https://img.freepik.com/free-photo/vivid-blurred-colorful-background_58702-2515.jpg') no-repeat center center fixed;
            background-size: cover;
            height: 100vh;
        }

        .chat-container {
            position: relative;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: rgba(0, 0, 0, 0.7);  /* Semi-transparent black for readability */
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            z-index: 1;
        }

        .message-box {
            display: flex;
            margin: 10px 0;
        }

        .user-message {
            background-color: #ff6b6b;
            color: white;
            padding: 10px 20px;
            border-radius: 15px;
            margin-left: auto;
            max-width: 70%;
            word-wrap: break-word;
        }

        .ai-message {
            background-color: #2e2e2e;
            color: white;
            padding: 10px 20px;
            border-radius: 15px;
            max-width: 70%;
            word-wrap: break-word;
        }

        input[type="text"] {
            background-color: #333;
            color: white;
            border: 1px solid #444;
            padding: 10px 15px;
            border-radius: 5px;
            width: 80%;
            font-size: 16px;
            margin-top: 10px;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #ff6b6b;
        }

        button {
            background-color: #ff6b6b;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }

        button:hover {
            background-color: #ff4c4c;
        }
    </style>
""", unsafe_allow_html=True)

# Create a container for the chat window
with st.container():
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Display message history
    for message in st.session_state.history:
        if message['role'] == 'user':
            st.markdown(f'<div class="message-box"><div class="user-message">{message["text"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-box"><div class="ai-message">{message["text"]}</div></div>', unsafe_allow_html=True)

    # Input box for user to type their message
    user_input = st.text_input("You: ", "", key="user_input")

    # Send message to the model and display response
    if user_input:
        response = chat_session.send_message(user_input)

        # Append the conversation to the history
        st.session_state.history.append({'role': 'user', 'text': user_input})
        st.session_state.history.append({'role': 'chatbot', 'text': response.text})

        # Display the chatbot's response
        st.markdown(f'<div class="message-box"><div class="ai-message">{response.text}</div></div>', unsafe_allow_html=True)

    # Button to reset the chat
    if st.button('Reset Chat'):
        st.session_state.history = []
        chat_session = model.start_chat(history=[])
        st.write("Chat has been reset.")
