import os
from dotenv import load_dotenv
import gradio as gr
from rag import SemanticSearchEngine
from anthropic_wrapper import AnthropicWrapper
from chatbot import ChatApp, conversation_iterator, summarize  # Assuming your code is in chat_app_module.py

load_dotenv()
chat_app = ChatApp()

def process_query(query):
    search_engine = SemanticSearchEngine()
    llm = AnthropicWrapper()
    
    data_file = 'data/dataset.json'
    embeddings_file = 'data/embeded_data.json'
    
    if not os.path.exists(embeddings_file):
        search_engine.load_data(data_file)
        search_engine.embed_documents()
        search_engine.save_embeddings(embeddings_file)
    else:
        search_engine.load_embeddings(embeddings_file)
    
    retrieved_docs = search_engine.run_search(query, top_k=5)
    prompt = llm.create_prompt(retrieved_docs, query)
    response = llm.generate_text(prompt)
    return response

def chat_and_process(message, history):
    
    if history is None:
        history = []
    if len(history) <= 3:
        output = conversation_iterator(message,chat_app)
        print(output)
        yield output
    else:
        output = summarize(chat_app)
        yield process_query(message)




def main():

    
    interface = gr.ChatInterface(
        fn=chat_and_process,
    )
    interface.launch()

    

if __name__ == "__main__":
    main()
