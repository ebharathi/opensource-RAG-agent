import base64
import os
import io
import tempfile
from PIL import Image
from nexaai import CV

# Path to your GGUF OCR model (DeepSeek-OCR-GGUF)
MODEL_NAME = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models",
    "DeepSeek-OCR.Q4_0.gguf"
)

class OCRService:
    def __init__(self, model_name: str = MODEL_NAME, device: str = "cpu"):
        """
        Initialize the OCR service with NexaSDK.
        Args:
            model_name: The path to the GGUF OCR model
            device: "cpu" or "cuda"
        """
        print(model_name)
        
        # Correct initialization according to documentation
        # CV.from_(model, capabilities=0, plugin_id="cpu_gpu")
        self.cv_model = CV.from_(
            model=model_name,
            capabilities=0,  # Default capabilities
            plugin_id="cpu_gpu"
        )
    
    def extract_text_from_path(self, img_path: str) -> str:
        """
        Performs OCR on an image file path.
        """
        # Run inference
        result = self.cv_model.infer(input_image_path=img_path)
        
        # Return extracted text
        # The result should have a text attribute or can be converted to string
        return result.text if hasattr(result, "text") else str(result)
    
    def extract_text_from_base64(self, image_b64: str) -> str:
        """
        Performs OCR from a base64 image string.
        """
        # Remove data prefix if present
        if image_b64.startswith("data:image"):
            image_b64 = image_b64.split(",", 1)[1]
        
        # Decode and open
        image_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Save to a unique temp file (avoid collisions)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
            image.save(tmp_path)
        
        try:
            # Run inference on the temp image
            result = self.cv_model.infer(input_image_path=tmp_path)
            return result.text if hasattr(result, "text") else str(result)
        finally:
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except Exception:
                pass