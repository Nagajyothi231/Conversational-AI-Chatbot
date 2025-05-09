import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import re

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # You can fine-tune later
#model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")
# Load cleaned content
with open("data/utd_scraped.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Split long text into chunks
def chunk_text(text, max_words=60):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    count = 0

    for sentence in sentences:
        words = sentence.split()
        if count + len(words) <= max_words:
            current_chunk += " " + sentence
            count += len(words)
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
            count = len(words)

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# Build FAISS index
index = faiss.IndexFlatL2(384)  # MiniLM has 384-dimensional output
metadata = []

for entry in raw_data:
    chunks = chunk_text(entry["content"])

    for chunk in chunks:
        embedding = model.encode(chunk)
        index.add(np.array([embedding], dtype=np.float32))

        metadata.append({
            "text": chunk,
            "url": entry["url"],
            "title": entry["title"]
        })

# Save FAISS index and metadata
os.makedirs("embeddings", exist_ok=True)

faiss.write_index(index, "embeddings/faiss_index.index")

with open("embeddings/metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"✅ Stored {len(metadata)} chunks in FAISS with metadata.")
