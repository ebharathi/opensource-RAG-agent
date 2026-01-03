from fastapi import FastAPI
import uvicorn
import os
from routes import router
from middleware.logging_middleware import LoggingMiddleware
from services.ocr_service import OCRService
from utils.logger import logger

# ---------------------------
# Initialize OCR Service on startup
# ---------------------------
ocr_service = None
try:
    ocr_service = OCRService()
    logger.info("[OCR] Service initialized successfully")
    
    # Test OCR with example image if it exists
    images_dir = os.path.join(os.path.dirname(__file__), "images")
    example_image_path = None
    
    # Try different possible filenames
    for filename in ["example_one.png", "example_1.png", "example.png"]:
        test_path = os.path.join(images_dir, filename)
        if os.path.exists(test_path):
            example_image_path = test_path
            break
    
    if example_image_path:
        logger.info(f"[OCR] Testing with image: {example_image_path}")
        try:
            text = ocr_service.extract_text_from_path(example_image_path)
            logger.info(f"[OCR] Extracted text:\n{text}")
        except Exception as e:
            logger.error(f"[OCR] Error during test: {str(e)}")
    else:
        logger.warning(f"[OCR] No example image found in {images_dir}")
        
except Exception as e:
    logger.error(f"[OCR] Failed to initialize OCR service: {str(e)}")

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