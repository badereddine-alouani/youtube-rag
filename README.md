# 🎥 YouTube-RAG: Retrieval-Augmented Generation from YouTube Videos

**YouTube-RAG** is a lightweight app that allows users to ask questions based on the transcript of any YouTube video. It combines modern LLMs and vector databases to create a simple but powerful retrieval-augmented generation (RAG) pipeline.

Built with:
- 🧠 [LangChain](https://github.com/langchain-ai/langchain)
- 🔍 [ChromaDB](https://www.trychroma.com/)
- 💬 [DeepSeek LLM](https://openrouter.ai/chat/deepseek) via [OpenRouter](https://openrouter.ai/)
- 📺 [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
- 🌐 [Streamlit](https://streamlit.io/) for the frontend

---

## 🚀 Features

- 🔗 Enter any YouTube video URL
- 📝 Automatically fetch the transcript (supports multiple languages)
- 📚 Split and embed transcript into a vectorstore (Chroma)
- 🤖 Ask questions about the content using DeepSeek LLM
- ♻️ Persistent or temporary vectorstore support
- 💡 Simple Streamlit interface

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/youtube-rag.git
cd youtube-rag

# Create and activate virtual environment (optional)
python -m venv venv
source venv/bin/activate  # on Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

---

## 🛠️ Configuration

### 🔐 OpenRouter API Key (for DeepSeek)
You’ll need an OpenRouter API key to access DeepSeek or other LLMs.

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

Then make sure your code loads it using `os.getenv("OPENROUTER_API_KEY")`.

---

## 🧠 How It Works

1. User enters a YouTube URL and a question in the Streamlit app.
2. The backend:
   - Extracts the video ID and retrieves the transcript via **YouTube Transcript API**
   - Splits and embeds the transcript using **LangChain** with **HuggingFace Embeddings**
   - Stores/fetches embeddings from a **Chroma vectorstore**
3. The user’s question is passed to a **LangChain RAG pipeline** powered by **DeepSeek (via OpenRouter)**
4. The model returns a context-aware answer, grounded in the video transcript.

---

## 🖥️ Usage

```bash
streamlit run main.py
```

Then open your browser to the URL shown in the terminal (usually http://localhost:8501).

---

## 📁 Project Structure

```
youtube-rag/
├── app/
│   ├── interface.py        # Streamlit frontend
│   ├── retriever.py        # Vectorstore logic
│   ├── rag_chain.py        # LangChain RAG pipeline
│   └── youtube.py          # Transcript extraction and video ID parsing
├── vectorstores/           # (Ignored) Folder for persisted vectorstores
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📄 .gitignore

Make sure your `.gitignore` includes:

```
/vectorstores/
.env
```

---

## 🧪 Example Prompt

> **YouTube URL:** `https://www.youtube.com/watch?v=dQw4w9WgXcQ`  
> **Question:** "What is the main message of the video?"

---

## 🤝 Contributions

PRs are welcome! Feel free to open issues or suggest improvements.

---

## 📜 License

MIT License.

---

## 💬 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain)
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)
- [Chroma DB](https://www.trychroma.com/)
- [OpenRouter](https://openrouter.ai/)
- [DeepSeek](https://github.com/deepseek-ai)
- [Streamlit](https://streamlit.io/)
