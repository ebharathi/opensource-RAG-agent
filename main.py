from fastapi import FastAPI
import uvicorn
from routes import router
from middleware.logging_middleware import LoggingMiddleware

# ---------------------------
# FastAPI app
# ---------------------------
app = FastAPI(title="Local GGUF Embedding Service")

# ---------------------------
# Add middleware
# ---------------------------
app.add_middleware(LoggingMiddleware)

# ---------------------------
# Include routes
# ---------------------------
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)