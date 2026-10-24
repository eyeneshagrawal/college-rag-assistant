import re
def split(text, size=800, overlap_sents=1):
    """Sentence-aware chunks (~size chars) with 1-sentence overlap; never cuts mid-sentence."""
    t = re.sub(r"[ \t]+", " ", text.replace("\r", ""))
    t = re.sub(r"\n(?!\n)", " ", t)                       # join hard-wrapped lines
    sents = [s.strip() for s in re.split(r"(?<=[.!?:;])\s+|\n{2,}", t) if s.strip()]
    out, cur = [], []
    for s in sents:
        if cur and sum(len(x) + 1 for x in cur) + len(s) > size:
            out.append(" ".join(cur)); cur = cur[-overlap_sents:] if overlap_sents else []
        cur.append(s[:size])                              # guard against giant "sentences"
    if cur: out.append(" ".join(cur))
    return [c for c in out if len(c) > 40]
