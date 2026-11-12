import os

MODEL = os.getenv("MODULE8_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = int(os.getenv("MODULE8_MAX_TOKENS", "8000"))
OUTPUT_DIR = os.getenv("MODULE8_OUTPUT_DIR", "output/module_8")
