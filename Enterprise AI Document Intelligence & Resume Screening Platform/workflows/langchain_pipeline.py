import os

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

from config import Config


class LangChainPipeline:

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.llm = ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model_name=Config.CHAT_MODEL,
            temperature=0
        )

        self.vector_store = None
        self.qa_chain = None

    def create_vector_store(self, chunks):

        texts = [
            chunk.text
            for chunk in chunks
        ]

        metadatas = [
            {
                **chunk.metadata,
                "file_name": chunk.file_name,
                "file_path": chunk.file_path,
                "file_type": chunk.file_type,
                "chunk_id": chunk.chunk_id
            }
            for chunk in chunks
        ]

        self.vector_store = FAISS.from_texts(
            texts=texts,
            embedding=self.embedding_model,
            metadatas=metadatas
        )

        self.save_vector_store()

    def save_vector_store(self):

        if self.vector_store is None:
            raise ValueError("Vector store not initialized.")

        self.vector_store.save_local(
            Config.EMBEDDINGS_DIR
        )

    def load_vector_store(self):

        if not os.path.exists(Config.EMBEDDINGS_DIR):
            raise FileNotFoundError(
                "FAISS index not found."
            )

        self.vector_store = FAISS.load_local(
            Config.EMBEDDINGS_DIR,
            self.embedding_model,
            allow_dangerous_deserialization=True
        )

    def initialize_qa(self):

        if self.vector_store is None:
            self.load_vector_store()

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": 5
                }
            ),
            return_source_documents=True
        )

    def ask(self, question):

        if self.qa_chain is None:
            self.initialize_qa()

        response = self.qa_chain.invoke(
            {
                "query": question
            }
        )

        return {
            "answer": response["result"],
            "sources": response["source_documents"]
        }

    def similarity_search(
            self,
            query,
            top_k=5
    ):

        if self.vector_store is None:
            self.load_vector_store()

        return self.vector_store.similarity_search(
            query,
            k=top_k
        )