import streamlit as st
from langchain.llms import LlamaCpp

st.title("Mental Health Companion Bot")
st.write("Talk to the bot about your mental health.")

# Initialize LLaMA model (adjust model path if needed)
llm = LlamaCpp(model_path="models/your-model.bin")  # replace with your model

user_input = st.text_input("You: ")

if user_input:
    response = llm(user_input)
    st.text_area("Bot:", value=response, height=200)
