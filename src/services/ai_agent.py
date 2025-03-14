import os
from typing import List, Tuple, Dict, Optional
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_anthropic import ChatAnthropic
from langchain.schema.document import Document
from langchain.chains.question_answering import load_qa_chain

from src.config import settings
from src.services.personality_manager import (
    get_personality_prompt,
    get_default_prompt,
)


class AIAgent:
    def __init__(self, personality_id: Optional[str] = None):
        self.personality_id = personality_id
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        self.is_fallback_mode = False

        self.llm = ChatAnthropic(
            temperature=0.2,
            model=settings.ANTHROPIC_MODEL_NAME,
            anthropic_api_key=settings.ANTHROPIC_API_KEY,
            max_tokens=2000,
        )

        if personality_id:
            self.qa_prompt = get_personality_prompt(personality_id)
            self.vector_db_path = os.path.join(settings.VECTOR_DB_PATH, personality_id)
        else:
            self.qa_prompt = get_default_prompt()
            self.vector_db_path = os.path.join(settings.VECTOR_DB_PATH, "general")

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
        # Ensure the vector database directory exists
        os.makedirs(self.vector_db_path, exist_ok=True)

        # Check if the vector database already exists
        if os.path.exists(os.path.join(self.vector_db_path, "chroma.sqlite3")):
            print(
                f"Loading existing vector database for {self.personality_id or 'general'}..."
            )
            self.vector_db = Chroma(
                persist_directory=self.vector_db_path,
                embedding_function=self.embeddings,
            )
            self._create_conversation_chain()
        else:
            print(
                f"Creating new vector database for {self.personality_id or 'general'}..."
            )
            # Process PDFs and create the vector database
            self._create_vector_db_from_pdfs()

        # Create the conversation chain
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_db.as_retriever(search_kwargs={"k": 4}),
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": self.qa_prompt},
        )

    def _create_conversation_chain(self):
        """Create the conversation chain with the current vector database."""
        if self.vector_db:
            # Create normal conversation chain with retriever
            self.conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vector_db.as_retriever(search_kwargs={"k": 4}),
                memory=self.memory,
                return_source_documents=True,
                combine_docs_chain_kwargs={"prompt": self.qa_prompt},
            )
            self.is_fallback_mode = False
        else:
            # Create fallback chain that doesn't use a retriever
            print("WARNING: Using fallback mode without vector database")

            qa_chain = load_qa_chain(
                llm=self.llm, chain_type="stuff", prompt=self.qa_prompt
            )
            # Create a simple QA chain without retrieval
            self.conversation_chain = qa_chain
            self.is_fallback_mode = True

    def _create_vector_db_from_pdfs(self):
        """Create a vector database from PDF files in the configured directory."""
        documents = []

        # If we have a personality ID, only load the corresponding PDF
        if self.personality_id:
            pdf_filename = f"{self.personality_id}.pdf"
            pdf_path = os.path.join(settings.PDF_DIR, pdf_filename)

            if os.path.exists(pdf_path):
                try:
                    loader = PyPDFLoader(pdf_path)
                    documents.extend(loader.load())
                    print(f"Loaded {len(documents)} documents from {pdf_filename}")
                except Exception as e:
                    print(f"Warning: Personality-specific PDF not found: {pdf_path}")
                    self._load_all_pdfs(documents)
            else:
                self._load_all_pdfs(documents)

        if not documents:
            print("Warning: No PDFs were loaded. Creating minimal vector database.")
            # Create a minimal document based on personality
            if self.personality_id:
                # Get personality name from ID with title case formatting
                personality_name = " ".join(
                    word.capitalize() for word in self.personality_id.split("-")
                )
                minimal_text = (
                    f"This is the {personality_name} agent. "
                    f"It specializes in providing advice and information related to {self.personality_id}. "
                    "Since no detailed information is available, responses will be limited."
                )
            else:
                minimal_text = (
                    "This is a general AI assistant. "
                    "Since no detailed information is available, responses will be limited."
                )

            # Create a minimal document
            minimal_doc = Document(
                page_content=minimal_text, metadata={"source": "minimal_info.txt"}
            )
            documents.append(minimal_doc)

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)

        # Create and persist the vector database
        self.vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.vector_db_path,
        )
        self.vector_db.persist()
        print(f"Created vector database with {len(chunks)} chunks")

    def _load_all_pdfs(self, documents):
        """Helper method to load all PDFs from the directory."""
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

        try:
            # Get the answer
            if self.is_fallback_mode:
                # For fallback mode without vector DB
                empty_docs = [Document(page_content="", metadata={"source": "empty"})]
                result = self.conversation_chain(
                    {"input_documents": empty_docs, "question": question}
                )
                answer = result.get(
                    "output_text", "I'm sorry, I couldn't find an answer."
                )
                sources = ["No knowledge base available"]
            else:
                # Normal mode with vector DB
                result = self.conversation_chain({"question": question})
                answer = result.get("answer", "I'm sorry, I couldn't find an answer.")
                source_docs = result.get("source_documents", [])

                # Extract source information
                sources = []
                for doc in source_docs:
                    if hasattr(doc, "metadata") and "source" in doc.metadata:
                        sources.append(doc.metadata["source"])

            return answer, list(set(sources)) if sources else []

        except Exception as e:
            print(f"Error while processing question: {e}")
            # Return a fallback answer
            return (
                "I'm sorry, I encountered an error while processing your question. "
                "Please try again or contact support if the issue persists.",
                [],
            )

    def reset_conversation(self):
        """Reset the conversation history."""
        self.memory.clear()

    def get_personality_info(self) -> Dict[str, str]:
        """Get the personality ID of the AI agent."""
        return self.personality_id
