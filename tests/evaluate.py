"""Eval: python tests/evaluate.py tests/questions.csv   (cols: question,expected_source[,category])
Retrieval Accuracy and Safe Refusal Rate. Retrieval-only for answerable Qs -> costs 0 LLM tokens."""
import csv, sys
sys.path.insert(0, ".")
from rag import retrieve, ask
import config as c
rows = list(csv.DictReader(open(sys.argv[1])))
ans = [r for r in rows if r["expected_source"]]; un = [r for r in rows if not r["expected_source"]]
ok = sum(bool(h) and h[0].payload["source"] == r["expected_source"] for r in ans for h in [retrieve(r["question"])])
ref = sum(ask(r["question"])[0] == c.NOT_FOUND for r in un)
print(f"Retrieval Accuracy: {ok/max(len(ans),1)*100:.1f}%  Safe Refusal Rate: {ref/max(len(un),1)*100:.1f}%")
