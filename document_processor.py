from typing import List, Optional
from pathlib import Path
import os

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    set_global_service_context,
    Document
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DocumentProcessor:
    def __init__(self, temperature: float = 0.1):
        """Initialize the document processor with custom settings."""
        # Initialize LLM
        llm = OpenAI(temperature=temperature, model="gpt-3.5-turbo")
        
        # Initialize embedding model
        embed_model = OpenAIEmbedding()
        
        # Create and set service context
        service_context = ServiceContext.from_defaults(
            llm=llm,
            embed_model=embed_model,
            chunk_size=1024,
            chunk_overlap=20
        )
        set_global_service_context(service_context)
        
        self.documents = []
        self.index = None
    
    def load_documents(self, directory: str = "data") -> None:
        """Load documents from the specified directory and create an index."""
        # Load new documents
        new_documents = SimpleDirectoryReader(directory).load_data()
        
        # Add to existing documents
        self.documents.extend(new_documents)
        
        # Create or update index with all documents
        self.index = VectorStoreIndex.from_documents(
            self.documents,
            service_context=ServiceContext.from_defaults(chunk_size=1024)
        )
    
    def query_documents(self, query: str) -> str:
        """Query the document index and return the response."""
        if not self.index:
            return "No documents have been loaded yet."
        
        query_engine = self.index.as_query_engine(
            similarity_top_k=5  # Consider top 5 most relevant chunks
        )
        response = query_engine.query(query)
        return str(response)
    
    def get_document_summary(self) -> str:
        """Generate a summary of the loaded documents."""
        if not self.index:
            return "No documents have been loaded yet."
        
        query_engine = self.index.as_query_engine()
        summary_prompt = ("Please provide a comprehensive summary of all the documents, "
                        "highlighting the main topics and key points from each. "
                        "If there are multiple documents, try to show relationships "
                        "between their content when relevant.")
        response = query_engine.query(summary_prompt)
        return str(response)