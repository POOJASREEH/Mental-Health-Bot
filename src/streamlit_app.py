import streamlit as st

st.set_page_config(page_title="Mental Health Bot", layout="centered")

st.title("💚 Mental Health Companion Bot")

st.write(
    "Hello! I am your Mental Health Companion. "
    "I can provide advice, answer FAQs, and share resources to support your mental well-being."
)

user_input = st.text_input("Type your message:")

if user_input:
    # Dummy response for now
    st.text_area("Bot:", f"You said: {user_input}\n\nI am still learning to respond intelligently.")
