import json
from pathlib import Path

class OutputManager:
    def __init__(self, output_dir): self.output_dir=Path(output_dir); self.output_dir.mkdir(parents=True, exist_ok=True)
    def write(self, name, data):
        p=self.output_dir/name
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return str(p)
