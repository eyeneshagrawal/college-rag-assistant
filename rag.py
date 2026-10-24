"""Query path: embed -> vector search -> (score gate) -> Groq LLM. Token-lean by design."""
import functools, re
from groq import Groq
import voyageai
from qdrant_client import QdrantClient
import config as c

vo = voyageai.Client(api_key=c.VOYAGE_API_KEY)
qd = QdrantClient(url=c.QDRANT_URL, api_key=c.QDRANT_API_KEY)
cl = Groq(api_key=c.GROQ_API_KEY)

SYSTEM = ("College assistant. Answer ONLY from the CONTEXT. Be concise (max 3 sentences). "
          f"If the context fully lacks the answer, reply with ONLY: {c.NOT_FOUND} "
          "Never add that sentence to a real answer. Do not write citations; sources are shown separately.")

def retrieve(q, k=None):
    v = vo.embed([q], model=c.EMBED_MODEL, input_type="query").embeddings[0]
    hits = qd.query_points(c.COLLECTION, query=v, limit=k or c.TOP_K, with_payload=True).points
    return [h for h in hits if h.score >= c.MIN_SCORE]

@functools.lru_cache(maxsize=512)          # repeated questions cost 0 tokens
def ask(q, deep=False, wide=False):
    hits = retrieve(q, 8 if wide else None)
    if not hits:                            # no evidence -> refuse WITHOUT calling the LLM (0 tokens)
        return c.NOT_FOUND, []
    ctx = "\n\n".join(f"[{h.payload['source']} p{h.payload['page']}] {h.payload['text']}" for h in hits)
    r = cl.chat.completions.create(model=c.LLM_MODEL, max_completion_tokens=1800 if deep else c.MAX_OUT, reasoning_effort="high" if deep else "low",
                                   messages=[{"role": "system", "content": SYSTEM},
                                             {"role": "user", "content": f"CONTEXT:\n{ctx}\n\nQUESTION: {q}"}])
    srcs = [(h.payload["source"], h.payload["page"], h.payload["text"]) for h in hits]
    ans = re.sub(r"【[^】]*】", "", r.choices[0].message.content).strip()
    if ans.replace(c.NOT_FOUND, "").strip():          # real answer: drop any stray refusal sentence
        return ans.replace(c.NOT_FOUND, "").strip(), srcs
    return c.NOT_FOUND, []


def docs():
    """[(source, chunk_count)] of everything indexed."""
    if not qd.collection_exists(c.COLLECTION): return []
    try:
        return sorted((h.value, h.count) for h in qd.facet(c.COLLECTION, key="source", limit=200).hits)
    except Exception:
        from collections import Counter
        cnt, off = Counter(), None
        while True:
            pts, off = qd.scroll(c.COLLECTION, limit=256, offset=off, with_payload=["source"], with_vectors=False)
            cnt.update(p.payload["source"] for p in pts)
            if off is None: return sorted(cnt.items())

@functools.lru_cache(maxsize=64)
def topics(source):
    """One cheap LLM call per document (cached): 6-8 askable topics from a sample of its chunks."""
    from qdrant_client import models as m
    f = m.Filter(must=[m.FieldCondition(key="source", match=m.MatchValue(value=source))])
    pts, _ = qd.scroll(c.COLLECTION, scroll_filter=f, limit=40, with_payload=True, with_vectors=False)
    step = max(1, len(pts) // 10)
    sample = "\n".join(p.payload["text"][:260] for p in pts[::step][:10])
    r = cl.chat.completions.create(model=c.LLM_MODEL, max_completion_tokens=400, reasoning_effort="low",
        messages=[{"role": "user", "content": "From this document excerpt list 6-8 short topics a student could ask about. "
                   "One per line, no numbering, no extra text.\n\n" + sample}])
    return [x.strip("-•* \t") for x in r.choices[0].message.content.splitlines() if x.strip()][:8]
