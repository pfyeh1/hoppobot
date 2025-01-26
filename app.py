import streamlit as st
from streamlit_option_menu import option_menu
import json
from openai import OpenAI

# Streamlit App Layout: Set page config at the very beginning
st.set_page_config(page_title="Multi-Personality Chatbot", layout="wide")

# Load configuration file for OpenAI API key
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    st.error("Config file not found. Please ensure `config.json` is present.")
    config = {}

# Initialize OpenAI API client
api_key = config.get('openai_api_key', st.text_input("Enter your OpenAI API key:", type="password"))
if not api_key:
    st.warning("Please provide a valid OpenAI API key to proceed.")
    st.stop()

client = OpenAI(api_key=api_key)

# Define chatbot personalities
def chatbot_response(personality, user_input):
    prompt_templates = {
        "Friendly": "You are a friendly and cheerful assistant. Respond warmly and positively.",
        "Professional": "You are a professional assistant. Respond formally and concisely.",
        "Witty": "You are a witty and humorous assistant. Respond with clever humor.",
    }
    system_prompt = prompt_templates.get(personality, "You are a helpful assistant.")
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=150,
            temperature=0.7,
        )
        response_message = response.choices[0].message.content
        return response_message
    except Exception as e:
        return f"[Error]: {str(e)}"

# Streamlit App Layout
st.title("🤖 Multi-Personality Chatbot")
st.markdown("A sleek chatbot with multiple personalities.")

# Sidebar for selecting personality
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

# Chat input and display
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chat_input = st.text_input("Type your message here:")

if st.button("Send"):
    if chat_input.strip():
        # Get chatbot response
        response = chatbot_response(personality, chat_input)

        # Save the interaction in chat history
        st.session_state.chat_history.append({"role": "user", "content": chat_input})
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        # Display the chat history
        for message in st.session_state.chat_history:
            role_style = (
                "color: white; background: #1f2937;"
                if message["role"] == "assistant"
                else "color: black; background: #d1d5db;"
            )
            st.markdown(
                f"<div style='padding:10px; border-radius:8px; {role_style}'>{message['content']}</div>",
                unsafe_allow_html=True,
            )

# Footer with styling
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
