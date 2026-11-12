class AnswerNormalizer:
    def normalize(self, data):
        pages=data.get("pages",[]) if isinstance(data,dict) else []
        grouped={}
        for page in pages:
            if page.get("page_type")!="ANSWER": continue
            for answer in page.get("answers",[]) or []:
                n=str(answer.get("answer_number","")).strip()
                if not n: continue
                e=grouped.setdefault(n,{"question_number":n,"answer_text":"","source_pages":[],"ocr_confidence":[]})
                if e["answer_text"]: e["answer_text"]+="\n\n"
                e["answer_text"]+=answer.get("answer_text","") or ""
                pg=answer.get("source_page",page.get("page_number"))
                if pg is not None and pg not in e["source_pages"]: e["source_pages"].append(pg)
                for el in answer.get("elements",[]) or []:
                    c=el.get("confidence")
                    if isinstance(c,(int,float)): e["ocr_confidence"].append(c)
        for e in grouped.values():
            v=e["ocr_confidence"]
            e["ocr_confidence"]=round(sum(v)/len(v),4) if v else None
        return grouped
