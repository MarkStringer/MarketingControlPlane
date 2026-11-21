#!/usr/bin/env python3
"""Local RAG index for the repo (no API calls).

  scripts/rag_index.py build            # (re)index, incremental by file hash
  scripts/rag_index.py query "text" [-k 8] [--path source/show]

Embeddings: BAAI/bge-small-en-v1.5 via fastembed (ONNX, CPU).
Store: rag-index/{vectors.npy,chunks.jsonl,files.json} (gitignored, regenerable).
"""
import argparse, hashlib, json, re, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "rag-index"
MODEL = "BAAI/bge-small-en-v1.5"
DIRS = ["source", "observed", "queue", "desired-state", "decisions"]
EXTS = {".md", ".txt", ".srt", ".vtt", ".pdf"}
SKIP = {"queue/reply-candidates/template-reply-candidate.md"}
CHUNK_WORDS, OVERLAP = 220, 40
TS = re.compile(r"^\d+$|^\d{1,2}:\d{2}:\d{2}[.,]\d{2,3}\s*-->|^WEBVTT|^\s*$")


def read_text(p: Path) -> str:
    if p.suffix == ".pdf":
        from pypdf import PdfReader
        return "\n".join((pg.extract_text() or "") for pg in PdfReader(str(p)).pages)
    txt = p.read_text(errors="ignore")
    if p.suffix in (".srt", ".vtt"):
        txt = " ".join(l.strip() for l in txt.splitlines() if not TS.match(l))
    return txt


def chunks(text: str):
    words = text.split()
    step = CHUNK_WORDS - OVERLAP
    for i in range(0, max(len(words), 1), step):
        piece = " ".join(words[i:i + CHUNK_WORDS])
        if piece.strip():
            yield piece
        if i + CHUNK_WORDS >= len(words):
            break


def files():
    for d in DIRS:
        for p in sorted((ROOT / d).rglob("*")):
            if p.is_file() and p.suffix.lower() in EXTS and str(p.relative_to(ROOT)) not in SKIP:
                yield p


def embedder():
    from fastembed import TextEmbedding
    return TextEmbedding(MODEL)


def build():
    OUT.mkdir(exist_ok=True)
    old_files = json.loads((OUT / "files.json").read_text()) if (OUT / "files.json").exists() else {}
    old_chunks, old_vecs = [], None
    if (OUT / "chunks.jsonl").exists() and (OUT / "vectors.npy").exists():
        old_chunks = [json.loads(l) for l in (OUT / "chunks.jsonl").open()]
        old_vecs = np.load(OUT / "vectors.npy")
    keep = {}
    for i, c in enumerate(old_chunks):
        keep.setdefault(c["path"], []).append(i)

    new_files, rows, vecs, todo = {}, [], [], []
    for p in files():
        rel = str(p.relative_to(ROOT))
        h = hashlib.sha1(p.read_bytes()).hexdigest()
        new_files[rel] = h
        if old_files.get(rel) == h and rel in keep:
            for i in keep[rel]:
                rows.append(old_chunks[i]); vecs.append(old_vecs[i])
        else:
            try:
                for n, c in enumerate(chunks(read_text(p))):
                    todo.append({"path": rel, "n": n, "text": c})
            except Exception as e:
                print(f"skip {rel}: {e}", file=sys.stderr)
    if todo:
        print(f"embedding {len(todo)} chunks...")
        emb = list(embedder().embed([t["text"] for t in todo]))
        rows += todo; vecs += emb
    mat = np.asarray(vecs, dtype=np.float32)
    mat /= np.linalg.norm(mat, axis=1, keepdims=True) + 1e-9
    np.save(OUT / "vectors.npy", mat)
    with (OUT / "chunks.jsonl").open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    (OUT / "files.json").write_text(json.dumps(new_files))
    print(f"indexed {len(new_files)} files, {len(rows)} chunks ({len(todo)} new)")


def query(q, k, prefix):
    rows = [json.loads(l) for l in (OUT / "chunks.jsonl").open()]
    mat = np.load(OUT / "vectors.npy")
    qv = np.asarray(list(embedder().query_embed([q]))[0], dtype=np.float32)
    qv /= np.linalg.norm(qv) + 1e-9
    scores = mat @ qv
    seen = 0
    for i in np.argsort(-scores):
        r = rows[i]
        if prefix and not r["path"].startswith(prefix):
            continue
        print(f"\n[{scores[i]:.3f}] {r['path']} #{r['n']}\n  {r['text'][:400]}")
        seen += 1
        if seen >= k:
            break


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    qp = sub.add_parser("query")
    qp.add_argument("text"); qp.add_argument("-k", type=int, default=8); qp.add_argument("--path", default="")
    a = ap.parse_args()
    build() if a.cmd == "build" else query(a.text, a.k, a.path)
