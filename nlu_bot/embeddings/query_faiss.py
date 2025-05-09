import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the model, index, and metadata
model = SentenceTransformer("all-MiniLM-L6-v2")
#model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
index = faiss.read_index("embeddings/faiss_index.index")

with open("embeddings/metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

def search_faiss(query, top_k=3):
    query_vector = model.encode(query)
    D, I = index.search(np.array([query_vector], dtype=np.float32), top_k)
    
    results = []
    for idx in I[0]:
        if idx < len(metadata):
            results.append(metadata[idx])
    return results

# Test it
if __name__ == "__main__":
    while True:
        q = input("\n🔍 Ask me anything about UTD: ")
        if q.lower() in ['exit', 'quit']:
            break
        results = search_faiss(q)
        print("\n🧠 Top Results:")
        for r in results:
            print(f"➡️ [{r['title']}] {r['text']}\n   🔗 {r['url']}\n")
