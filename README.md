# 🤖 JSOM Conversational AI Chatbot
 
This is a category-aware Conversational AI chatbot developed for the Jindal School of Management (JSOM) at the University of Texas at Dallas. It allows users to ask natural language questions and receive accurate, relevant answers drawn from structured website content.
 
---
 
## 📘 About the Project
 
Built as part of BUAN 6390 – Analytics Practicum (Spring 2025), this project simplifies access to academic information by combining:
 
- Semantic search using Sentence-BERT (`all-MiniLM-L6-v2`)
- Fast similarity search with FAISS
- Guided category selection via Chainlit UI
- Query understanding and response logic with Rasa
- Feedback logging for continuous improvement
 
---
 
## 🛠 Technologies Used
 
- Python  
- BeautifulSoup & Trafilatura (Web Scraping)  
- Sentence-BERT (`all-MiniLM-L6-v2`) – Hugging Face  
- FAISS – Facebook AI Similarity Search  
- Rasa SDK – Backend and NLU logic  
- Chainlit – User interface  
- CSV – Feedback logging  
 
---
 
## 🧱 System Workflow
 
1. Scrape and clean JSOM website content  
2. Chunk text and generate embeddings  
3. Store embeddings in FAISS with metadata  
4. User selects category and asks a question  
5. Rasa processes the query, searches FAISS, returns results  
6. Feedback is optionally collected and stored
 
---
 
## 👥 Team Members
 
Group 5  
- Naga Jyothi Muvva  
- Roshini Priyanka Gatreddi  
- Jahnavi Donthula  
- Prasanna Laxmi Endralla  
- Venkata Ganga Govardhan Mowva  
- Praneeth Chandra Budala
 
---
 
## 📚 References
 
- Hugging Face – [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)  
- Facebook – [FAISS](https://github.com/facebookresearch/faiss)  
- [Rasa](https://rasa.com/)  
- [Chainlit](https://docs.chainlit.io/)  
- [JSOM Website](https://jindal.utdallas.edu/)
