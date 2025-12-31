from llama_cpp import Llama
import os

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "granite-embedding-278m-multilingual-Q8_0.gguf")  # local model path


class EmbeddingService:
    def __init__(self, model_path: str = MODEL_PATH,  
                 n_ctx: int = 512, n_threads: int = 8):
        """
        Initialize the embedding service with a GGUF model.
        
        Args:
            model_path: Path to the GGUF model file
            n_ctx: Context window size
            n_threads: Number of threads for processing
        """
        self.llm = Llama(
            model_path=model_path,
            embedding=True,
            n_ctx=n_ctx,
            n_threads=n_threads,
            verbose=False
        )
    
    def create_embedding(self, text: str) -> list[float]:
        """
        Create an embedding for the given text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of float values representing the embedding
        """
        result = self.llm.create_embedding(text)
        return result["data"][0]["embedding"]

