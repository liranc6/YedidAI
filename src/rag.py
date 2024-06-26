from datasets import load_dataset
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
import torch
import json
import os

class SemanticSearchEngine:
    def __init__(self, model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.embedded_documents = []
    
    def load_data(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            self.documents = json.load(f)
    
    def preprocess(self, document, *args):
        if (args):
            return document[args]
        return document
        
    def embed_document(self, document):
        embeddings = self.model.encode(str(document), convert_to_tensor=True)
        return embeddings
        
    
    def embed_documents(self):
        for document in tqdm(self.documents):
            document_to_embed = self.preprocess(document)
            embedding = self.embed_document(document_to_embed)
            embedded_document = document
            embedded_document['embedding'] = embedding
            self.embedded_documents.append(embedded_document)
    
    def save_embeddings(self, file_path):
        json_serializable_documents = self.embedded_documents
        with open(file_path, 'w', encoding='utf-8') as f:
            for document in json_serializable_documents:
                # Convert tensor to list for JSON serialization
                document['embedding'] = document['embedding'].cpu().tolist()
            json.dump(json_serializable_documents, f)
            for document in json_serializable_documents:
                # Convert tensor to list for JSON serialization
                document['embedding'] = torch.tensor(document['embedding'])
    
    def load_embeddings(self, file_path):
        with open(file_path, 'r') as f:
            self.embedded_documents = json.load(f)
            # Convert lists back to tensors
            for document in self.embedded_documents:
                document['embedding'] = torch.tensor(document['embedding'])
    
    def semantic_search(self, query, top_k=5):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        document_embeddings = torch.stack([doc['embedding'] for doc in self.embedded_documents])
        hits = util.semantic_search(query_embedding, document_embeddings, top_k=top_k)
        
        results = []
        for hit in hits[0]:  # hits[0] because semantic_search returns a list of lists
            result = self.embedded_documents[hit['corpus_id']]
            result['score'] = hit['score']
            results.append(result)
        
        return results
    
    def run_search(self, query, top_k=5):
        results = self.semantic_search(query, top_k)
        print("\nSemantic Search Results:")
        for result in results:
            print(f"Score: {result['score']:.4f}, Sentence: {result['title'][::-1]}")
    
def main():
    search_engine = SemanticSearchEngine()
    
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
        search_engine.run_search(query, top_k=5)

if __name__ == "__main__":
    main()
