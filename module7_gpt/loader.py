import json
from pathlib import Path
class Module7Loader:
    def load_json(self,path):
        p=Path(path)
        if not p.exists(): raise FileNotFoundError(f"File not found: {p}")
        return json.loads(p.read_text(encoding="utf-8"))
