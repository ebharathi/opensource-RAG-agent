from langchain_core.tools import tool
from sqlalchemy.orm import Session
from services.semantic_search_service import SemanticSearchService
from services.embedding_service import EmbeddingService
from database.database import SessionLocal
from utils.tool_logger import log_tool_call


# Initialize services (singleton pattern)
_embedding_service = None
_search_service = None

def get_search_service():
    """Get or create semantic search service instance"""
    global _embedding_service, _search_service
    if _search_service is None:
        if _embedding_service is None:
            _embedding_service = EmbeddingService()
        _search_service = SemanticSearchService(_embedding_service)
    return _search_service


@tool
@log_tool_call
def semantic_search(query: str, limit: int = 5) -> str:
    """
    Perform semantic search on stored documents using vector similarity.
    Use this tool to find relevant information from the knowledge base.
    
    Args:
        query: The search query/question to find relevant information
        limit: Maximum number of results to return (default: 5)
        
    Returns:
        A formatted string containing the most relevant chunks of text from the knowledge base
    """
    db = SessionLocal()
    try:
        search_service = get_search_service()
        results = search_service.search(db, query, limit=limit)
        
        if not results:
            return "No relevant information found in the knowledge base."
        
        # Format results
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"[Result {i}] (Similarity: {result['similarity']:.2%})\n"
                f"{result['chunk_text']}\n"
                f"---"
            )
        
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Error performing semantic search: {str(e)}"
    finally:
        db.close()


semantic_search_tool = semantic_search

