import streamlit as st
import google.generativeai as genai
import os

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

# Streamlit app layout
st.title("Baymax - your neighborhood AI")
st.write("Hey there Human ! I am here to assist you whenever you need some information. Type something to start the conversation........")

# Embed the Lottie animation with the provided HTML embed code
lottie_embed_html = """
<script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>
<dotlottie-player src="https://lottie.host/703302ed-68d8-4bed-99ff-f550f8cb3d6c/dTcLdt3L7h.lottie" background="transparent" speed="1" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:2;" loop autoplay></dotlottie-player>
"""
# Display Lottie animation in Streamlit
st.markdown(lottie_embed_html, unsafe_allow_html=True)

# Add custom CSS to style the background image and overlay
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
