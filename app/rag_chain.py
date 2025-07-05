from app.retriever import get_retriever
from app.youtube import extract_video_id
from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()


llm = ChatOpenAI(model_name="deepseek/deepseek-chat-v3-0324:free")
prompt = hub.pull("rlm/rag-prompt")


def create_rag_chain(url):
    retriever = get_retriever(url)
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
