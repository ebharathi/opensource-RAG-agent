from sqlalchemy.orm import Session
from database.models import Document, DocumentChunk
from services.embedding_service import EmbeddingService
from typing import List


class StoreEmbeddingService:
    def __init__(self, embedding_service: EmbeddingService):
        """
        Initialize the store embedding service.
        
        Args:
            embedding_service: Instance of EmbeddingService for creating embeddings
        """
        self.embedding_service = embedding_service
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into chunks with optional overlap.
        
        Args:
            text: Text to chunk
            chunk_size: Maximum size of each chunk in characters
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary if possible
            if end < len(text):
                # Look for sentence endings near the end
                for punct in ['. ', '.\n', '! ', '!\n', '? ', '?\n']:
                    last_punct = chunk.rfind(punct)
                    if last_punct > chunk_size * 0.7:  # If found in last 30% of chunk
                        chunk = chunk[:last_punct + 1]
                        end = start + len(chunk)
                        break
            
            chunks.append(chunk.strip())
            start = end - overlap  # Overlap for context
        
        return chunks
    
    def store_document_with_chunks(
        self, 
        db: Session, 
        text: str, 
        chunk_size: int = 500, 
        overlap: int = 50
    ) -> Document:
        """
        Store a document and its chunks with embeddings in the database.
        
        Args:
            db: Database session
            text: Text to store
            chunk_size: Maximum size of each chunk
            overlap: Overlap between chunks
            
        Returns:
            Created Document object
        """
        # Create document
        document = Document(text=text)
        db.add(document)
        db.flush()  # Flush to get the document ID
        
        # Chunk the text
        chunks = self.chunk_text(text, chunk_size, overlap)
        
        # Create chunks with embeddings
        for chunk_text in chunks:
            if not chunk_text.strip():
                continue
            
            # Create embedding for chunk
            embedding = self.embedding_service.create_embedding(chunk_text)
            
            # Create chunk record
            chunk = DocumentChunk(
                document_id=document.id,
                text=chunk_text,
                embedding=embedding
            )
            db.add(chunk)
        
        # Commit all changes
        db.commit()
        db.refresh(document)
        
        return document
