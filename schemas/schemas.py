from pydantic import BaseModel
from uuid import UUID


class EmbedRequest(BaseModel):
    text: str


class EmbedResponse(BaseModel):
    embedding: list[float]
    dimensions: int


class StoreDocumentRequest(BaseModel):
    text: str
    chunk_size: int = 500
    overlap: int = 50


class StoreDocumentResponse(BaseModel):
    document_id: UUID
    chunks_count: int
    message: str

