import os
from langchain_chroma import Chroma  # Updated import
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from app.youtube import extract_video_id, get_transcript

embed = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def get_retriever(url):
    video_id = extract_video_id(url)
    persist_dir = f"vectorstores/{video_id}"
    os.makedirs("vectorstores", exist_ok=True)

    if os.path.exists(persist_dir) and len(os.listdir(persist_dir)) > 0:
        print("Loading existing vectorstore...")
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embed,
        )
    else:
        print("Creating new vectorstore...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        transcript = get_transcript(url)
        doc = Document(page_content=transcript)
        splits = text_splitter.split_documents([doc])

        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embed,
            persist_directory=persist_dir,
        )

    return vectorstore.as_retriever()
