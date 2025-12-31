from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas.schemas import EmbedRequest, EmbedResponse, StoreDocumentRequest, StoreDocumentResponse
from services.embedding_service import EmbeddingService
from services.store_embedding_service import StoreEmbeddingService
from database.models import DocumentChunk


class EmbeddingController:
    def __init__(self, embedding_service: EmbeddingService):
        """
        Initialize the embedding controller with a service instance.
        
        Args:
            embedding_service: Instance of EmbeddingService
        """
        self.embedding_service = embedding_service
        self.store_service = StoreEmbeddingService(embedding_service)
    
    def embed_text(self, req: EmbedRequest) -> EmbedResponse:
        """
        Handle the embedding request.
        
        Args:
            req: EmbedRequest containing the text to embed
            
        Returns:
            EmbedResponse with embedding and dimensions
            
        Raises:
            HTTPException: If text is empty
        """
        if not req.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        embedding = self.embedding_service.create_embedding(req.text)
        
        return EmbedResponse(
            embedding=embedding,
            dimensions=len(embedding)
        )
    
    def store_document(
        self, 
        req: StoreDocumentRequest, 
        db: Session
    ) -> StoreDocumentResponse:
        """
        Store a document with chunked embeddings.
        
        Args:
            req: StoreDocumentRequest containing text and chunking parameters
            db: Database session
            
        Returns:
            StoreDocumentResponse with document ID and chunk count
            
        Raises:
            HTTPException: If text is empty
        """
        if not req.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        document = self.store_service.store_document_with_chunks(
            db=db,
            text=req.text,
            chunk_size=req.chunk_size,
            overlap=req.overlap
        )
        
        # Query chunks count from database
        chunks_count = db.query(func.count(DocumentChunk.id)).filter(
            DocumentChunk.document_id == document.id
        ).scalar()
        
        return StoreDocumentResponse(
            document_id=document.id,
            chunks_count=chunks_count,
            message=f"Document stored successfully with {chunks_count} chunks"
        )

