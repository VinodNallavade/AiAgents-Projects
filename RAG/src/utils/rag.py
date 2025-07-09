from src.utils.model import models
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
import streamlit as st
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStore
from langchain_community.vectorstores import FAISS
from typing import List, Any, Optional
import logging
from langchain_community.docstore.in_memory import InMemoryDocstore
from uuid import uuid4
import faiss

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class RAG:
    def __init__(self,chat_model_name,api_key,embedding_model):
        """Initialize LLM and embedding model."""
        try:
            model_cls = models(api_key=api_key,chat_model_name=chat_model_name,embedding_model=embedding_model)
            self.llm = model_cls.get_llm_model()
            self.embedding_model = model_cls.get_embedding_model()
            logger.info("LLM and embedding models loaded successfully.")
        except Exception as e:
            logger.exception("Failed to initialize models.")
            st.error("Model initialization failed.")
            raise

    async def process_file(self, files: Any) -> List[Document]:
        """
        Handle the uploaded PDF file and load it into Document objects.
        """
        with st.spinner("Loading PDF..."):
            try:

                return await self._load_file(files)
            except Exception as e:
                logger.exception("Error processing file.")
                st.error("Error while processing file.")
                return []

    async def _load_file(self, uploaded_files: Any) -> List[Document]:
        """
        Save the uploaded file temporarily and load it using PyPDFLoader.
        """
        try:     
            all_documents = []       
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(bytes_data)
                    tmp_file_path = tmp_file.name
                    st.write(tmp_file_path)

                loader = PyPDFLoader(tmp_file_path)
                documents = await loader.aload()
                logger.info(f"Loaded {len(documents)} documents from PDF.")
                all_documents.extend(documents)

            logger.info(f"Total documents loaded: {len(all_documents)}")
            return all_documents

        except Exception as e:
            logger.exception("Error loading PDF file.")
            raise

    def chunk_documents(self, documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 100) -> List[Document]:
        """
        Split documents into chunks using a recursive character splitter.
        """
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            chunks = splitter.split_documents(documents)
            logger.info(f"Split into {len(chunks)} chunks.")
            return chunks
        except Exception as e:
            logger.exception("Error while chunking documents.")
            st.error("Failed to split documents into chunks.")
            return []

    def create_chroma_persist_directory(self) -> str:
        """
        Create or get a directory for storing the Chroma vector database.
        """
        try:
            persist_directory = "db"
            st.session_state.persist_directory = persist_directory
            logger.info(f"Chroma persist directory set to: {persist_directory}")
            return persist_directory
        except Exception as e:
            logger.exception("Error setting Chroma persist directory.")
            raise

    def store_to_vectordb(self, chunks: List[Document]) -> Optional[Chroma]:
        """
        Store text chunks into a Chroma vector store.
        """
        try:
            index = faiss.IndexFlatL2(len(self.embedding_model.embed_query("hello world")))

            vector_store = FAISS(
                embedding_function=self.embedding_model,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )
            uuids = [str(uuid4()) for _ in range(len(chunks))]

            vector_store.add_documents(documents=chunks, ids=uuids)
            logger.info("Chunks successfully stored in Chroma vector store.")
            return vector_store
        except Exception as e:
            logger.exception("Failed to store chunks in Chroma.")
            st.error("Failed to store data in vector database.")
            return None

    def get_retriever(self, vector_store: VectorStore, k: int = 6, lambda_mult: float = 0.25) -> Optional[Any]:
        """
        Return a retriever interface from a vector store using MMR.
        """
        try:
            retriever = vector_store.as_retriever(
                search_type="mmr",
                search_kwargs={"k": k, "lambda_mult": lambda_mult}
            )
            logger.info("Retriever initialized successfully.")
            return retriever
        except Exception as e:
            logger.exception("Error creating retriever from vector store.")
            st.error("Failed to create retriever.")
            return None

    async def run_rag_pipeline(
        self,
        files: Any,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
        k: int = 6,
        lambda_mult: float = 0.25
        ) -> Optional[Any]:
        """
        Full RAG pipeline: Load file → chunk → embed → vector DB → retriever.
        Returns a retriever ready for querying.
        """
        try:
            with st.spinner("📄 Loading PDF files..."):
                documents = await self.process_file(files)
            if not documents:
                st.warning("No documents found.")
                return None

            with st.spinner("✂️ Splitting documents into chunks..."):
                chunks = self.chunk_documents(documents, chunk_size, chunk_overlap)
            if not chunks:
                st.warning("No chunks created.")
                return None

            with st.spinner("🧠 Storing chunks in vector database..."):
                vector_store = self.store_to_vectordb(chunks)
            if not vector_store:
                st.error("Failed to store documents in vector DB.")
                return None

            with st.spinner("🔍 Preparing retriever..."):
                retriever = self.get_retriever(vector_store, k, lambda_mult)
            if not retriever:
                st.error("Failed to initialize retriever.")
                return None

            st.success("✅ RAG pipeline completed successfully.")
            return retriever

        except Exception as e:
            logger.exception("Error running full RAG pipeline.")
            st.error("❌ An error occurred while running the RAG pipeline.")
            return None