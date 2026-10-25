"""Run: python tests/evaluate.py tests/questions.csv   (needs the 4 secrets as env vars)
Retrieval is measured WITHOUT any LLM call (0 tokens). Only the 10 unanswerable questions may call the LLM (refusal test).
Writes tests/results.csv and tests/answers_for_human_scoring.csv"""
import csv, sys
sys.path.insert(0, ".")
from rag import retrieve, ask
import config as c
rows = list(csv.DictReader(open(sys.argv[1])))
res, hit1, hitk = [], {}, {}
for r in rows:
    if not r["expected_source"]: continue
    h = retrieve(r["question"]); srcs = [x.payload["source"] for x in h]
    t1, tk = bool(srcs) and srcs[0] == r["expected_source"], r["expected_source"] in srcs
    cat = r["category"]; hit1.setdefault(cat, []).append(t1); hitk.setdefault(cat, []).append(tk)
    res.append({"question": r["question"], "expected": r["expected_source"], "retrieved_top1": srcs[0] if srcs else "", "top1_correct": t1, "in_top_k": tk, "category": cat})
un = [r for r in rows if not r["expected_source"]]
ref = [ask(r["question"])[0] == c.NOT_FOUND for r in un]
pct = lambda l: f"{sum(l)/max(len(l),1)*100:.1f}%"
print("Retrieval Accuracy (top-1):", pct([x for v in hit1.values() for x in v]), {k: pct(v) for k, v in hit1.items()})
print("Retrieval Hit Rate (in top-k):", pct([x for v in hitk.values() for x in v]), {k: pct(v) for k, v in hitk.items()})
print(f"Safe Refusal Rate: {pct(ref)}  ({sum(ref)}/{len(ref)})")
with open("tests/results.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(res[0])); w.writeheader(); w.writerows(res)
with open("tests/answers_for_human_scoring.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["question", "answer", "correctness_1to5", "relevance_1to5", "groundedness_1to5", "clarity_1to5", "completeness_1to5"])
    for r in rows[:50:5]: w.writerow([r["question"], ask(r["question"])[0], "", "", "", "", ""])   # every 5th question: 10 answers to score
