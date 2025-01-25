import streamlit as st
import pyttsx3
from streamlit_option_menu import option_menu
import subprocess
import sys

# Ensure required packages are installed
#def install_and_import(package):
#    try:
#        __import__(package)
#    except ImportError:
#        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install necessary libraries
#install_and_import("streamlit")
#install_and_import("streamlit-option-menu")
#install_and_import("pyttsx3")

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Chatbot personalities
def chatbot_response(personality, user_input):
    if personality == "Friendly":
        return f"[Friendly Bot]: Hi there! {user_input} sounds interesting! How can I assist you?"
    elif personality == "Professional":
        return f"[Professional Bot]: Thank you for sharing. How may I help with that?"
    elif personality == "Witty":
        return f"[Witty Bot]: Oh, {user_input}? Sounds like a plot twist! What do you need?"
    return "[Default Bot]: I'm here to help!"

# Function to speak chatbot responses
def speak_response(response):
    engine.say(response)
    engine.runAndWait()

# App layout
st.set_page_config(page_title="Multi-Personality Chatbot", layout="wide")
st.title("🤖 Multi-Personality Chatbot")
st.markdown("A sleek chatbot with voice capabilities and multiple personalities.")

# Sidebar for selecting chatbot personality
with st.sidebar:
    st.header("Select Personality")
    personality = option_menu(
        menu_title=None,
        options=["Friendly", "Professional", "Witty"],
        icons=["emoji-smile", "briefcase", "emoji-laughing"],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"background-color": "#111827"},
            "icon": {"color": "#10b981", "font-size": "25px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin": "0px",
                "color": "#d1d5db",
                "--hover-color": "#374151",
            },
            "nav-link-selected": {"background-color": "#2563eb"},
        },
    )

# Main chat interface
chat_input = st.text_input("Type your message here:")

if st.button("Send"):
    if chat_input.strip():
        response = chatbot_response(personality, chat_input)
        st.markdown(f"<div style='padding: 10px; border-radius: 8px; background: #1f2937; color: white;'>"
                    f"{response}</div>", unsafe_allow_html=True)

        # Option to hear the response
        if st.checkbox("🔊 Enable Voice Response"):
            speak_response(response)

# Footer with animated futuristic styling
st.markdown(
    """
    <style>
    footer {
        background-color: #111827;
        color: #d1d5db;
        text-align: center;
        padding: 10px;
        position: fixed;
        bottom: 0;
        width: 100%;
    }
    footer::before {
        content: "";
        display: block;
        height: 2px;
        background: linear-gradient(to right, #10b981, #2563eb);
        margin-bottom: 10px;
    }
    </style>
    <footer>Multi-Personality Chatbot - Designed with ❤️</footer>
    """,
    unsafe_allow_html=True,
)
