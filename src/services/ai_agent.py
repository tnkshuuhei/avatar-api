import os
from typing import List, Tuple, Dict
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from src.config import settings


class AIAgent:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        self.llm = ChatOpenAI(
            temperature=0.2,
            model_name=settings.MODEL_NAME,
            openai_api_key=settings.OPENAI_API_KEY,
        )
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True, output_key="answer"
        )
        self.vector_db = None
        self.conversation_chain = None

        # Initialize the vector database
        self._initialize_vector_db()

    def _initialize_vector_db(self):
        """Initialize or load the vector database from PDFs."""
        # Check if the vector database already exists
        if os.path.exists(settings.VECTOR_DB_PATH):
            print("Loading existing vector database...")
            self.vector_db = Chroma(
                persist_directory=settings.VECTOR_DB_PATH,
                embedding_function=self.embeddings,
            )
        else:
            print("Creating new vector database from PDFs...")
            # Process PDFs and create the vector database
            self._create_vector_db_from_pdfs()

        # Create the conversation chain
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_db.as_retriever(search_kwargs={"k": 4}),
            memory=self.memory,
            return_source_documents=True,
        )

    def _create_vector_db_from_pdfs(self):
        """Create a vector database from PDF files in the configured directory."""
        documents = []

        # Get all PDF files
        for filename in os.listdir(settings.PDF_DIR):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(settings.PDF_DIR, filename)
                try:
                    loader = PyPDFLoader(pdf_path)
                    documents.extend(loader.load())
                    print(f"Loaded {pdf_path}")
                except Exception as e:
                    print(f"Error loading {pdf_path}: {e}")

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)

        # Create and persist the vector database
        self.vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=settings.VECTOR_DB_PATH,
        )
        self.vector_db.persist()
        print(f"Created vector database with {len(chunks)} chunks")

    def ask(self, question: str, context: List[str] = None) -> Tuple[str, List[str]]:
        """
        Ask a question to the AI agent and get an answer.

        Args:
            question: The question text
            context: Optional list of previous conversation messages

        Returns:
            Tuple of (answer_text, source_documents)
        """
        if not self.conversation_chain:
            raise ValueError("AI agent is not properly initialized")

        # Get the answer
        result = self.conversation_chain({"question": question})

        # Extract answer and sources
        answer = result.get("answer", "I'm sorry, I couldn't find an answer.")
        source_docs = result.get("source_documents", [])

        # Extract source information
        sources = []
        for doc in source_docs:
            if hasattr(doc, "metadata") and "source" in doc.metadata:
                sources.append(doc.metadata["source"])

        return answer, list(set(sources))  # Deduplicate sources

    def reset_conversation(self):
        """Reset the conversation history."""
        self.memory.clear()
