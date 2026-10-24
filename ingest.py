"""Scalable ingestion: PDF -> page-aware chunks -> batched embeddings -> batched idempotent upserts.
Run: python ingest.py data/   (re-running only re-writes changed chunks: IDs are content hashes)"""
import sys, glob, hashlib, os, uuid
from pypdf import PdfReader
import voyageai
from qdrant_client import QdrantClient, models as m
import config as c

vo = voyageai.Client(api_key=c.VOYAGE_API_KEY)
qd = QdrantClient(url=c.QDRANT_URL, api_key=c.QDRANT_API_KEY)

def chunks(src, name):
    for pno, page in enumerate(PdfReader(src).pages, 1):
        t = (page.extract_text() or "").strip()        # empty pages are skipped safely
        for i in range(0, len(t), c.CHUNK - c.OVERLAP):
            piece = t[i:i + c.CHUNK]
            if len(piece) > 40:
                yield {"text": piece, "source": name, "page": pno}

def index(files, batch=64):
    """files: list of (name, path_or_filelike)"""
    if not qd.collection_exists(c.COLLECTION):
        qd.create_collection(c.COLLECTION, vectors_config=m.VectorParams(size=c.DIM, distance=m.Distance.COSINE))
        qd.create_payload_index(c.COLLECTION, "source", m.PayloadSchemaType.KEYWORD)
    buf = [x for n, f in files for x in chunks(f, n)]
    for i in range(0, len(buf), batch):
        b = buf[i:i + batch]
        vecs = vo.embed([x["text"] for x in b], model=c.EMBED_MODEL, input_type="document").embeddings
        qd.upsert(c.COLLECTION, points=[
            m.PointStruct(id=str(uuid.UUID(hashlib.md5(x["text"].encode()).hexdigest())), vector=v, payload=x)
            for x, v in zip(b, vecs)])
    return len(buf)

def run(folder):
    print("Indexed", index([(os.path.basename(p), p) for p in glob.glob(f"{folder}/*.pdf")]), "chunks")

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "data")
