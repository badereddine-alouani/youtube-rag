import streamlit as st
from app.rag_chain import create_rag_chain
import shutil


def run_interface():
    st.set_page_config(page_title="YouTube RAG", layout="centered")

    st.title("🎥 YouTube RAG Demo")
    st.markdown("Ask a question based on a YouTube video transcript.")

    url = st.text_input("YouTube URL")
    question = st.text_input("Your question")

    if "last_url" not in st.session_state:
        st.session_state.last_url = None
    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None

    if st.button("Get Answer"):
        if not url or not question:
            st.warning("Please enter both a URL and a question.")
        else:
            with st.spinner("Loading transcript and thinking..."):
                try:

                    if url != st.session_state.last_url:
                        st.session_state.rag_chain = create_rag_chain(url)
                        st.session_state.last_url = url

                    if st.session_state.rag_chain is None:
                        st.error("Failed to initialize RAG chain. Please check the URL and try again.")
                    else:
                        answer = st.session_state.rag_chain.invoke({"query": question})
                        st.success("✅ Answer:")
                        st.markdown(f"> {answer.get('result', 'No response generated')}")
                except Exception as e:
                    st.error(f"An error occurred:\n\n{str(e)}")
    if st.button("🗑️ Delete all vectorstores"):
        try:
            shutil.rmtree("vectorstores")
            st.success("Deleted all vectorstores.")
        except Exception as e:
            st.error(f"Could not delete vectorstores:\n{str(e)}")
