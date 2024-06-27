from rag import SemanticSearchEngine
from anthropic_wrapper import AnthropicWrapper
import os
def main():
    search_engine = SemanticSearchEngine()
    llm = AnthropicWrapper()
    
    data_file = 'data/dataset.json'
    embeddings_file = 'data/embeded_data.json'
    
    if not os.path.exists(embeddings_file):
        # Load data and create embeddings if not already done
        search_engine.load_data(data_file)
        search_engine.embed_documents()
        search_engine.save_embeddings(embeddings_file)
    else:
        # Load precomputed embeddings
        search_engine.load_embeddings(embeddings_file)
    while (True):
        query = input("Enter query: ")
        retrieved_docs = search_engine.run_search(query, top_k=5)
        prompt = llm.create_prompt(retrieved_docs, query)
        response = llm.generate_text(prompt)[::-1]
        print(response)
    #TODO connect to llm and get the response and create ui
if __name__ == "__main__":
    main()