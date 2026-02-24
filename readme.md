# 📺 Samsung Smart TV Manual Assistant (RAG System)

An AI-powered chatbot application that provides instant, accurate answers directly from official Samsung Smart TV manuals. This project leverages Retrieval-Augmented Generation (RAG) to search through thousands of manual pages (covering Tizen OS, Smart Hub, QLED, Neo QLED, and The Frame) and deliver precise contextual answers.

<img width="495" height="599" alt="Screenshot 2026-02-24 164900" src="https://github.com/user-attachments/assets/cbfd0ae8-efdb-46f5-ad30-a8a1127486af" />
                             <img width="495" height="599" alt="image" src="https://github.com/user-attachments/assets/f4490d0e-07d3-427c-b2fc-148965f6a05d" />


## 🌟 Features

* **Local Embeddings:** Utilizes open-source embeddings to process text locally without relying on paid or rate-limited external APIs.
  * **Fast Vector Search:** Used **FAISS** (Facebook AI Similarity Search) for fast similarity matching and retrieval of relevant manual chunks.
* **Intelligent Text Chunking:** Uses LangChain's `RecursiveCharacterTextSplitter` with overlapping chunks to ensure context isn't lost between pages or paragraphs.
* **Web-Based Chat Interface:** A UI built with **HTML** and chatbot built using ***JS*** served via a **Flask** backend, mimicking a real-world customer support interface.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **RAG Framework:** LangChain 
* **Vector Database:** FAISS
* **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
* **Document Processing:** PyPDFLoader
* **Frontend:** HTML, Vanilla JS

## 📂 Project Structure

```text
├── manual/                 # Directory containing your Samsung TV PDF manuals
├── vector_store/           # Directory where the generated FAISS index is saved
├── static/                 # CSS and JS files for the frontend
├── templates/              # HTML templates (e.g., index.html) for Flask
├── rag_setup.py            # Script to parse PDFs, create embeddings, and build the Vector DB
├── rag_retriever.py        # Module to load the Vector DB and fetch context for queries
├── app.py                  # Main Flask application (Server)
└── README.md               # Project documentation

```

git clone https://github.com/Jayanth-0407/RAG-based-smart-TV-assistant
cd RAG-based-smart-TV-assistant

***To run the application***
python app.py  
