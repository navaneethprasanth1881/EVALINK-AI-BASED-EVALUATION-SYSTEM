import json,re
def extract_json(text):
    text=(text or "").strip()
    text=re.sub(r"^\s*```(?:json)?\s*","",text,flags=re.I)
    text=re.sub(r"\s*```\s*$","",text)
    candidates=[text]
    s,e=text.find("{"),text.rfind("}")
    if s>=0 and e>s: candidates.append(text[s:e+1])
    for c in candidates:
        try: return json.loads(c)
        except json.JSONDecodeError: pass
    try:
        from json_repair import repair_json
        for c in candidates:
            r=repair_json(c,return_objects=True)
            if r is not None: return r
    except Exception: pass
    raise ValueError("Could not parse OpenAI response as JSON.")
