import streamlit as st
from src.ui.uiconfigfile import Config
from src.utils.rag import RAG


class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        print(self.config)
        self.user_controls= {}

    async def side_components(self):
        st.set_page_config(
        page_title="PDF Chat App",
        page_icon="📚",
        layout="centered",
        initial_sidebar_state="expanded",
        )
        st.title("💬 Chat with your PDF")
        with st.sidebar:

            self.user_controls["SelectedLLM"] = st.selectbox("Select LLM Provider",["Azure"])
            self.user_controls["ChatModel"] = st.selectbox("Select Model",["gpt-4o-mini","gpt-35-turbo","gpt-35-turbo-instruct"])
            self.user_controls["EmbeddingModel"] = st.selectbox("Select Model",["text-embedding-ada-002"])      
            self.user_controls["LLMKey"] =  st.text_input("Please provide Key", type= "password")    
            if not self.user_controls["LLMKey"]:
                st.warning("Please provide key")
        uploaded_files = st.file_uploader(label="Please upload file of max 200Mb",accept_multiple_files= True,type=["pdf"])        
        if st.button("Upload and Process"):
            if uploaded_files is not None:
                rag = RAG(self.user_controls["ChatModel"],self.user_controls["LLMKey"],self.user_controls["EmbeddingModel"])
                await rag.run_rag_pipeline(files=uploaded_files)
            else:
                st.error("Please upload files")

        return self.user_controls
