# College RAG Assistant (cloud-only, Claude-powered)
Claude (answers) + Voyage AI (embeddings) + Qdrant Cloud (vector DB) + Streamlit Community Cloud (UI) + Jira (tracking, project RAG).
## Deploy (no localhost)
1. Free keys: console.anthropic.com, dash.voyageai.com, cloud.qdrant.io (1 free cluster).
2. Push repo to GitHub -> share.streamlit.io -> New app -> `app.py`. In *Secrets* paste:
   ANTHROPIC_API_KEY, VOYAGE_API_KEY, QDRANT_URL, QDRANT_API_KEY
3. Index PDFs from a cloud shell (GitHub Codespaces): `pip install -r requirements.txt && python ingest.py data/`
4. Evaluate: `python tests/evaluate.py tests/questions.csv`
## Scalability
Stateless app + managed vector DB (horizontal scale), batched embed/upsert, idempotent content-hash IDs (cheap re-ingest), payload index on `source`, page-level citations.
## Token efficiency
Haiku tier, top-4 x 800-char chunks, max_tokens 300, prompt caching on system prompt, score gate refuses without any LLM call, lru_cache on repeats, retrieval eval uses 0 LLM tokens.
