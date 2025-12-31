from fastapi import APIRouter
from schemas.schemas import ChatRequest, ChatResponse
from controllers.chat_controller import ChatController

# Initialize controller
chat_controller = ChatController()

# Create router
router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Endpoint to chat with the agent.
    The agent can use semantic search to find relevant information from stored documents.
    
    Args:
        req: ChatRequest containing the user message
        
    Returns:
        ChatResponse with the agent's response
    """
    return chat_controller.chat(req)

