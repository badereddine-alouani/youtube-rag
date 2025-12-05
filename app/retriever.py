import os
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
import traceback

def get_retriever(url: str):
    embed = OllamaEmbeddings(model="mistral:7b")
    video_id = None
    detected_language = None

    if "youtu" in url:
        if "shorts/" in url:
            video_id = url.split("shorts/")[-1].split("?")[0].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[-1].split("?")[0].split("&")[0]
        elif "v=" in url:
            video_id = url.split("v=")[-1].split("&")[0]

    if not video_id:
        print("Invalid YouTube URL format")
        print(f"Supported formats:")
        print(f"  - https://www.youtube.com/watch?v=VIDEO_ID")
        print(f"  - https://youtu.be/VIDEO_ID")
        print(f"  - https://www.youtube.com/shorts/VIDEO_ID")
        return None, None

    normalized_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"Normalized URL: {normalized_url}")

    persist_dir = f"vectorstores/{video_id}"
    index_file = f"{persist_dir}/index.faiss"

    os.makedirs("vectorstores", exist_ok=True)
    os.makedirs(persist_dir, exist_ok=True)

    vectorstore = None

    if os.path.exists(index_file):
        print("Loading existing vectorstore...")
        vectorstore = FAISS.load_local(persist_dir, embed, allow_dangerous_deserialization=True)
        
        # Extract language from metadata
        if vectorstore.docstore._dict:
            first_doc = next(iter(vectorstore.docstore._dict.values()))
            detected_language = first_doc.metadata.get("language", "unknown")
            print(f"Loaded transcript language: {detected_language}")

    if vectorstore is None:
        print("Creating new vectorstore...")

        print("Fetching YouTube transcript...")
        try:
            ytt_api = YouTubeTranscriptApi()
            
            # Get list of available transcripts
            transcript_list = ytt_api.list(video_id)
            
            # Try to find any available transcript
            # Priority: manually created > generated
            transcript = None
            language_code = None
            
            try:
                # First try to find any manually created transcript
                transcript = transcript_list.find_manually_created_transcript(['en'])
                language_code = transcript.language_code
                print(f"Using manually created transcript in language: {language_code}")
            except:
                try:
                    # If no manual transcript, try generated ones
                    transcript = transcript_list.find_generated_transcript(['en'])
                    language_code = transcript.language_code
                    print(f"Using auto-generated transcript in language: {language_code}")
                except:
                    try:
                        # If English not available, try any language
                        transcript = transcript_list.find_transcript([t.language_code for t in transcript_list])
                        language_code = transcript.language_code
                        print(f"Using transcript in language: {language_code}")
                    except:
                        pass
            
            if not transcript:
                raise Exception("No transcripts available for this video")

            # Fetch the actual transcript data
            fetched_transcript = transcript.fetch()
            detected_language = language_code  # Set detected_language here
            
            print(f"Retrieved {len(fetched_transcript)} transcript entries")
            print(f"Transcript language: {detected_language}")
            
            # Extract text from snippets
            transcript_text = " ".join([snippet.text for snippet in fetched_transcript])
            
            docs = [Document(
                page_content=transcript_text,
                metadata={
                    "source": normalized_url,
                    "video_id": video_id,
                    "language": language_code or "unknown"
                }
            )]
            
        except Exception as e:
            print("Failed to fetch transcript:")
            print(str(e))
            traceback.print_exc()
            docs = None

        if not docs:
            print("No transcript available — aborting")
            return None, None

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        if not splits:
            print("No document chunks created")
            return None, None

        vectorstore = FAISS.from_documents(documents=splits, embedding=embed)
        vectorstore.save_local(persist_dir)
        print("Vectorstore saved locally")

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    print("Retriever created successfully")
    return retriever, detected_language