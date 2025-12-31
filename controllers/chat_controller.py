import time
from fastapi import HTTPException
from schemas.schemas import ChatRequest, ChatResponse
from agent.agent import get_agent_with_history
from langchain_core.messages import HumanMessage
from utils.logger import logger


class ChatController:
    def __init__(self):
        """Initialize the chat controller."""
        pass
    
    def chat(self, req: ChatRequest) -> ChatResponse:
        """
        Handle chat request using the agent.
        
        Args:
            req: ChatRequest containing the user message
            
        Returns:
            ChatResponse with the agent's response
            
        Raises:
            HTTPException: If message is empty
        """
        if not req.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        try:
            start_time = time.time()
            
            # Get agent instance
            agent = get_agent_with_history()
            
            # Create human message
            messages = [HumanMessage(content=req.message)]
            
            # Log agent invocation
            logger.info(f"[AGENT] invoked with message: {req.message[:100]}")
            
            # Invoke agent
            response = agent.invoke({"messages": messages})
            
            # Extract response text from agent output
            # The response format depends on LangChain version
            if isinstance(response, dict):
                if "output" in response:
                    response_text = response["output"]
                elif "messages" in response and len(response["messages"]) > 0:
                    # Get the last message which should be the AI response
                    last_message = response["messages"][-1]
                    response_text = last_message.content if hasattr(last_message, "content") else str(last_message)
                else:
                    response_text = str(response)
            else:
                response_text = str(response)
            
            duration = time.time() - start_time
            logger.info(f"[AGENT] response generated in {duration:.3f}s: {response_text[:200]}")
            
            return ChatResponse(response=response_text)
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing chat request: {str(e)}"
            )

