# Lightweight matcher using sentence-transformers if available.
# If sentence-transformers is not installed, fallback to simple keyword overlap.
try:
    from sentence_transformers import SentenceTransformer, util
    USE_EMBED = True
    model = None  # Lazy load the model when needed
except Exception:
    model = None
    USE_EMBED = False

def _get_model():
    global model
    if model is None and USE_EMBED:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def _score_with_embeddings(job_desc, candidates):
    m = _get_model()
    job_emb = m.encode(job_desc, convert_to_tensor=True)
    results = []
    for c in candidates:
        res_emb = m.encode(c.resume_text or '', convert_to_tensor=True)
        score = float(util.cos_sim(job_emb, res_emb))
        results.append({"candidate_id": c.id, "name": c.name, "email": c.email, "score": round(score * 100, 2)})
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

def _score_with_keyword(job_desc, candidates):
    job_set = set([w.lower() for w in job_desc.split() if len(w)>2])
    results = []
    for c in candidates:
        txt = (c.resume_text or '').lower()
        cnt = sum(1 for w in job_set if w in txt)
        # simple normalization
        score = min(1.0, cnt / max(1, len(job_set)))
        results.append({"candidate_id": c.id, "name": c.name, "email": c.email, "score": round(score * 100, 2)})
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

def match_candidates(job_desc, candidates):
    if USE_EMBED and model:
        try:
            return _score_with_embeddings(job_desc, candidates)
        except Exception:
            return _score_with_keyword(job_desc, candidates)
    else:
        return _score_with_keyword(job_desc, candidates)