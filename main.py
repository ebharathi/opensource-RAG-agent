from fastapi import FastAPI
import uvicorn
from routes import router

# ---------------------------
# FastAPI app
# ---------------------------
app = FastAPI(title="Local GGUF Embedding Service")

# ---------------------------
# Include routes
# ---------------------------
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)