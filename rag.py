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

def retrieve(q):
    v = vo.embed([q], model=c.EMBED_MODEL, input_type="query").embeddings[0]
    hits = qd.query_points(c.COLLECTION, query=v, limit=c.TOP_K, with_payload=True).points
    return [h for h in hits if h.score >= c.MIN_SCORE]

@functools.lru_cache(maxsize=512)          # repeated questions cost 0 tokens
def ask(q):
    hits = retrieve(q)
    if not hits:                            # no evidence -> refuse WITHOUT calling the LLM (0 tokens)
        return c.NOT_FOUND, []
    ctx = "\n\n".join(f"[{h.payload['source']} p{h.payload['page']}] {h.payload['text']}" for h in hits)
    r = cl.chat.completions.create(model=c.LLM_MODEL, max_completion_tokens=c.MAX_OUT, reasoning_effort="low",
                                   messages=[{"role": "system", "content": SYSTEM},
                                             {"role": "user", "content": f"CONTEXT:\n{ctx}\n\nQUESTION: {q}"}])
    srcs = sorted({(h.payload["source"], h.payload["page"]) for h in hits})
    ans = re.sub(r"【[^】]*】", "", r.choices[0].message.content).strip()
    if ans.replace(c.NOT_FOUND, "").strip():          # real answer: drop any stray refusal sentence
        return ans.replace(c.NOT_FOUND, "").strip(), srcs
    return c.NOT_FOUND, []
