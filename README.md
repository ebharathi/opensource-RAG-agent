hf download bartowski/granite-embedding-278m-multilingual-GGUF   --include "*Q8_0.gguf"   --local-dir models   
hf download NexaAI/DeepSeek-OCR-GGUF   --include "*Q4_0.gguf"   --local-dir models

curl -X POST "http://localhost:8000/store" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a sample text that will be chunked and stored with embeddings. You can add as much text as you want here. The service will automatically split it into chunks, create embeddings for each chunk, and store them in the database.",
    "chunk_size": 500,
    "overlap": 50
  }'


For Docker setup,download the model to your local models/ folder then run docker compose which will mount the models/ to container
