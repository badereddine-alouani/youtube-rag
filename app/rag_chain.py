from app.retriever import get_retriever
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA


llm = OllamaLLM(model="mistral:7b", temperature=0)

def detect_language(text_sample):
    """Detect the language of the transcript"""
    detect_prompt = f"""Analyze this text and identify its language. Respond with ONLY the language name in English (e.g., "German", "English", "French", "Spanish").

Text:
{text_sample[:500]}

Language:"""
    
    try:
        response = llm.invoke(detect_prompt)
        return response.strip()
    except:
        return "English"

def create_rag_chain(url):
    print(f"Creating RAG chain for URL: {url}")
    
    retriever, language_code = get_retriever(url)
    print(f"Transcript language code: {language_code}")
    
    if retriever is None:
        print("ERROR: Failed to create retriever. Check the logs above for specific errors.")
        return None
    
    print("Successfully created retriever, building RAG chain...")
    
    # Get a sample of the documents to detect language
    sample_docs = retriever.invoke("sample")
    if sample_docs:
        transcript_sample = sample_docs[0].page_content
        detected_language = detect_language(transcript_sample)
        print(f"LLM detected transcript language: {detected_language}")
    else:
        detected_language = "the same language as the transcript"
    
    # Create a prompt with the language already filled in
    prompt_with_language = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an AI assistant. You will be answering questions based on the content of a YouTube video transcript.

CRITICAL INSTRUCTION: The transcript is in {language}. You MUST answer in {language}.

Additional Instructions:
- Use ONLY the information in the context (YouTube transcript) to answer.
- If the answer is not in the transcript, say "I could not find the answer in the video" in {language}.
- Be concise and clear.

Context (YouTube transcript):
{context}

Question:
{question}

Answer (in {language}):
"""
    ).partial(language=detected_language)
    
    try:
        rag_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt_with_language}
        )
        print("RAG chain created successfully!")
        return rag_chain
        
    except Exception as e:
        print(f"Error creating RAG chain: {e}")
        return None


def ask_question(rag_chain, question):
    """Helper function to safely ask questions"""
    if rag_chain is None:
        return "Error: RAG chain is not available. Please check the video URL and try again."
    
    try:
        response = rag_chain.invoke({"query": question})
        return response.get("result", "No response generated")
    except Exception as e:
        return f"Error processing question: {str(e)}"