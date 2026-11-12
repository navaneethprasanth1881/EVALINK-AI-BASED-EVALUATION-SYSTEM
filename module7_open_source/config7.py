import os
MODEL = os.getenv("MODULE7_MODEL", "llama3.1:8b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MAX_TOKENS = int(os.getenv("MODULE7_MAX_TOKENS", "6000"))
OUTPUT_DIR = os.getenv("MODULE7_OUTPUT_DIR", "output/module_7")
