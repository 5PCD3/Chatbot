from dotenv import load_dotenv
import streamlit as st
import os 
import google.generativeai as genai 

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro and get responses.
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initializing our streamlit app
st.set_page_config(page_title="Q&A Chatbot")
st.header("Q&A Chatbot")

# Chat History
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

input_text = st.text_input("Input: ", key="input")
submit_button = st.button("Start to chat")

# When Submit is clicked.
if submit_button and input_text:
    response = get_gemini_response(input_text)
    # Storing chat history
    st.session_state['chat_history'].append(("You", input_text))
    st.subheader("Response...")
    full_response = ""
    for chunk in response:
        full_response += chunk.text
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
    
    st.subheader("Chat History...")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
