def chunk_text(text, max_chars=800):
    words = text.split()
    chunks = []
    cur = []
    cur_len = 0
    for w in words:
        cur.append(w)
        cur_len += len(w) + 1
        if cur_len > max_chars:
            chunks.append(' '.join(cur))
            cur = []
            cur_len = 0
    if cur:
        chunks.append(' '.join(cur))
    return chunks
