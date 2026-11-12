import os
from pathlib import Path

OUTPUT_DIR = Path(os.getenv("MODULE7_OUTPUT_DIR", "output/module_7"))
MODEL = os.getenv("MODULE7_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = int(os.getenv("MODULE7_MAX_TOKENS", "12000"))

# The evaluator is instructed not to use temperature because current Anthropic
# SDK/API combinations may reject that parameter.
