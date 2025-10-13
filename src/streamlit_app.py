import streamlit as st
import os
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

st.set_page_config(page_title="Mental Health Bot", page_icon="🧠")

st.title("🧠 Mental Health Companion Bot")

@st.cache_resource(show_spinner=True)
def load_model():
    st.info("Downloading and loading BioMistral model... (4GB, may take a few minutes)")
    
    # Downloads the model from Hugging Face Hub
    model_path = hf_hub_download(
        repo_id="MaziyarPanahi/BioMistral-7B-GGUF",
        filename="BioMistral-7B.gguf"
    )
    
    # Load model with llama-cpp-python
    return Llama(model_path=model_path)

# Load model
llm = load_model()

# User input
user_input = st.text_input("How are you feeling today?")

if user_input:
    st.info("Generating response...")
    response = llm(user_input, max_tokens=200)
    st.success(response['choices'][0]['text'])
