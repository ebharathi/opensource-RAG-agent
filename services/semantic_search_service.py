from sqlalchemy.orm import Session
from sqlalchemy import text
from database.models import DocumentChunk, Document
from services.embedding_service import EmbeddingService
from typing import List, Dict, Optional


class SemanticSearchService:
    def __init__(self, embedding_service: EmbeddingService):
        """
        Initialize the semantic search service.
        
        Args:
            embedding_service: Instance of EmbeddingService for creating query embeddings
        """
        self.embedding_service = embedding_service
    
    def search(
        self,
        db: Session,
        query: str,
        limit: int = 5,
        similarity_threshold: float = 0.7
    ) -> List[Dict]:
        """
        Perform semantic search on stored document chunks.
        
        Args:
            db: Database session
            query: Search query text
            limit: Maximum number of results to return
            similarity_threshold: Minimum similarity score (0-1, higher = more similar)
            
        Returns:
            List of dictionaries containing chunk text, document info, and similarity score
        """
        # Create embedding for the query
        query_embedding = self.embedding_service.create_embedding(query)
        
 
        embedding_array = ','.join(map(str, query_embedding))
        
        sql_query = text(f"""
            SELECT 
                dc.id,
                dc.text,
                dc.document_id,
                d.text as document_text,
                d.created_at,
                1 - (dc.embedding <=> ARRAY[{embedding_array}]::vector) / 2 as similarity
            FROM document_chunks dc
            JOIN documents d ON dc.document_id = d.id
            WHERE 1 - (dc.embedding <=> ARRAY[{embedding_array}]::vector) / 2 >= :threshold
            ORDER BY dc.embedding <=> ARRAY[{embedding_array}]::vector
            LIMIT :limit
        """)
        
        result = db.execute(
            sql_query,
            {
                "threshold": similarity_threshold,
                "limit": limit
            }
        )
        
        results = []
        for row in result:
            results.append({
                "chunk_id": str(row.id),
                "chunk_text": row.text,
                "document_id": str(row.document_id),
                "document_text": row.document_text,
                "created_at": row.created_at.isoformat() if row.created_at else None,
                "similarity": float(row.similarity)
            })
        
        return results
    
    def search_simple(
        self,
        db: Session,
        query: str,
        limit: int = 5
    ) -> List[str]:
        """
        Simple semantic search that returns only chunk texts.
        
        Args:
            db: Database session
            query: Search query text
            limit: Maximum number of results to return
            
        Returns:
            List of chunk texts ordered by similarity
        """
        results = self.search(db, query, limit)
        return [result["chunk_text"] for result in results]

