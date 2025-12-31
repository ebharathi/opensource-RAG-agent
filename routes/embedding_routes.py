from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.schemas import EmbedRequest, EmbedResponse, StoreDocumentRequest, StoreDocumentResponse
from controllers.embedding_controller import EmbeddingController
from services.embedding_service import EmbeddingService
from database.database import get_db

# Initialize service and controller
embedding_service = EmbeddingService()
embedding_controller = EmbeddingController(embedding_service)

# Create router
router = APIRouter(tags=["embeddings"])


@router.post("/embed", response_model=EmbedResponse)
def embed_text(req: EmbedRequest):
    """
    Endpoint to create embeddings for text.
    
    Args:
        req: EmbedRequest containing the text to embed
        
    Returns:
        EmbedResponse with embedding vector and dimensions
    """
    return embedding_controller.embed_text(req)


@router.post("/store", response_model=StoreDocumentResponse)
def store_document(
    req: StoreDocumentRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint to store a document with chunked embeddings.
    
    Args:
        req: StoreDocumentRequest containing text and chunking parameters
        db: Database session
        
    Returns:
        StoreDocumentResponse with document ID and chunk count
    """
    return embedding_controller.store_document(req, db)

