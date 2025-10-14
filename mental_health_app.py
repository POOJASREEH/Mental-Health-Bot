import gradio as gr
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp

# Load components
print("Loading mental health assistant...")

# Load embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./mental_health_db", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Load BioMistral model
llm = LlamaCpp(
    model_path="/content/drive/MyDrive/BioMistral-7B.Q4_K_M.gguf",
    n_ctx=2048,
    temperature=0.3,
    max_tokens=500,
    top_p=0.9,
    verbose=False
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def mental_health_chat(message, history):
    if not message.strip():
        return "Please share how you're feeling or ask a question about mental health."

    # Get context from vector store
    docs = retriever.get_relevant_documents(message)

    # Fallback response if no relevant documents
    if not docs:
        return """💙 I understand you're seeking support. While I don't have specific information on this, here are resources that might help:

📞 **24/7 Mental Health Support:**
• National Suicide Prevention Lifeline: 988
• Crisis Text Line: Text HOME to 741741
• SAMHSA Helpline: 1-800-662-4357

🧘 **Quick Relaxation Techniques:**
• Deep breathing: 4-7-8 technique
• Grounding: 5-4-3-2-1 exercise
• Progressive muscle relaxation

Remember, professional support is available whenever you need it. You're not alone. 💙"""

    # Use context from documents
    context = format_docs(docs)

    # Create prompt for BioMistral
    prompt = f"""<s>[INST] You are a compassionate mental health assistant. Use this context:

{context}

Question: {message}

Provide a helpful, evidence-based response about mental health. Always remind users to consult healthcare professionals for personal advice. [/INST]"""

    # Get response from BioMistral
    response = llm.invoke(prompt)
    
    return response

# Emergency resources section
emergency_info = """
🚨 **Emergency Resources - Available 24/7**

**Immediate Support:**
• National Suicide Prevention Lifeline: **988**
• Crisis Text Line: Text **HOME** to **741741**
• SAMHSA Helpline: **1-800-662-4357**

**International Resources:**
• International Association for Suicide Prevention:
  [Find your country's helpline](https://www.iasp.info/resources/Crisis_Centres/)
"""

# Create Gradio interface with chat mode
with gr.Blocks(theme=gr.themes.Soft(), title="Mental Health Assistant") as demo:
    gr.Markdown("# 🧠 Mental Health Support Assistant")
    gr.Markdown("I'm here to provide mental health information and supportive listening. How can I help you today? 💙")

    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                label="Mental Health Chat",
                height=500,
                show_copy_button=True,
                placeholder="Ask me about mental health, therapy, coping strategies, or share how you're feeling..."
            )

            with gr.Row():
                msg = gr.Textbox(
                    label="Share how you're feeling or ask a question",
                    placeholder="Type your message here... (e.g., 'What is therapy?', 'How to manage anxiety?')",
                    lines=2,
                    scale=4
                )
                send_btn = gr.Button("Send 🚀", scale=1)

        with gr.Column(scale=1):
            gr.Markdown(emergency_info)

            gr.Markdown("### 🎯 Quick Support Topics")
            gr.Button("😔 Depression Info").click(
                lambda: "What are symptoms of depression and how can I get help?",
                outputs=msg
            )

            gr.Button("😰 Anxiety Help").click(
                lambda: "How can I manage anxiety and panic attacks?",
                outputs=msg
            )

            gr.Button("😤 Stress Management").click(
                lambda: "What are effective ways to manage daily stress?",
                outputs=msg
            )

            gr.Button("💤 Sleep Tips").click(
                lambda: "How can I improve my sleep for better mental health?",
                outputs=msg
            )
            
            gr.Button("🛋️ Therapy Info").click(
                lambda: "What is therapy and how does it work?",
                outputs=msg
            )
            
            gr.Button("🧘 Mindfulness").click(
                lambda: "What are mindfulness techniques for mental health?",
                outputs=msg
            )

    # Chat functionality
    def respond(message, chat_history):
        bot_message = mental_health_chat(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    send_btn.click(respond, [msg, chatbot], [msg, chatbot])

    # Clear button
    clear_btn = gr.Button("Clear Chat")
    clear_btn.click(lambda: None, None, chatbot, queue=False)

    gr.Markdown("---")
    gr.Markdown("""
    **Note:** This assistant provides supportive information but is not a substitute for professional medical advice, diagnosis, or treatment.
    If you're in crisis or having thoughts of harm, please contact emergency services immediately.
    
    **Powered by BioMistral Medical AI** 🏥
    """)

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)
