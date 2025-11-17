from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Tuple

import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import Program, VectorChunk


_model_cache = {"local": None}


def _get_local_model():
    global _model_cache
    if _model_cache["local"] is None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise RuntimeError("sentence-transformers not installed. Install with: pip install sentence-transformers") from e
        _model_cache["local"] = SentenceTransformer("all-MiniLM-L6-v2")
    return _model_cache["local"]


def _embed_query_local(text: str, pad_to: int = 1024) -> np.ndarray:
    model = _get_local_model()
    vec = model.encode([text], show_progress_bar=False)[0].astype(float)
    # pad or truncate to pad_to
    if vec.shape[0] < pad_to:
        vec = np.pad(vec, (0, pad_to - vec.shape[0]))
    elif vec.shape[0] > pad_to:
        vec = vec[:pad_to]
    return vec


@dataclass
class ScoredProgram:
    program_id: str
    score: float
    preview: str


def search_programs(db: Session, query: str, top_k: int = 10) -> List[ScoredProgram]:
    """
    Simple semantic search over program chunks using cosine similarity in Python.
    Uses the local sentence-transformers model for query embedding.
    """
    # 1) Embed query
    q = _embed_query_local(query)
    q_norm = np.linalg.norm(q) + 1e-8

    # 2) Fetch all chunks
    chunks = db.execute(
        select(VectorChunk.chunk_source_id, VectorChunk.chunk_text, VectorChunk.chunk_embedding)
    ).fetchall()

    # 3) Score each chunk and keep best per program
    best: Dict[str, Tuple[float, str]] = {}
    for program_id, text, emb in chunks:
        v = np.array(emb, dtype=float)
        denom = (np.linalg.norm(v) + 1e-8) * q_norm
        if denom == 0:
            continue
        score = float(np.dot(v, q) / denom)
        prev = text[:160].replace("\n", " ")
        if program_id not in best or score > best[program_id][0]:
            best[program_id] = (score, prev)

    # 4) Rank and take top_k
    ranked = sorted((ScoredProgram(pid, s, p) for pid, (s, p) in best.items()), key=lambda x: x.score, reverse=True)
    ranked = ranked[:top_k]

    return ranked


def hydrate_programs(db: Session, scored: List[ScoredProgram]) -> List[Dict]:
    if not scored:
        return []
    ids = [s.program_id for s in scored]
    # Fetch programs and map
    programs = db.query(Program).filter(Program.id.in_(ids)).all()
    by_id = {p.id: p for p in programs}

    # Preserve order and include scores
    results: List[Dict] = []
    for s in scored:
        p = by_id.get(s.program_id)
        if not p:
            continue
        results.append({
            "program": {
                "id": p.id,
                "name": p.name,
                "institution": getattr(p, "institution_name", None) or None,
                "degree_type": getattr(p, "degree_type", None) or None,
                "duration_years": getattr(p, "duration_years", None),
                "cost_total": getattr(p, "cost_total", None),
            },
            "score": round(float(s.score), 4),
            "preview": s.preview,
        })
    return results
