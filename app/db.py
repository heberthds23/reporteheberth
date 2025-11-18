import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class DB:
    def __init__(self):
        self.db = SessionLocal()

    def insert_upload(self, source, filename, storage_url, file_type, size_bytes):
        q = text("INSERT INTO uploads (source, filename, storage_url, file_type, size_bytes) VALUES (:s,:f,:u,:t,:b) RETURNING id")
        r = self.db.execute(q, {"s": source, "f": filename, "u": storage_url, "t": file_type, "b": size_bytes})
        id = r.fetchone()[0]
        self.db.commit()
        return id

    def get_upload(self, upload_id):
        q = text("SELECT * FROM uploads WHERE id=:id")
        r = self.db.execute(q, {"id": upload_id})
        row = r.fetchone()
        if not row:
            return {"error": "not found"}
        keys = r.keys()
        return dict(zip(keys, row))

    def insert_transcription(self, upload_id, text, model):
        q = text("INSERT INTO transcriptions (upload_id, text, model) VALUES (:u,:t,:m)")
        self.db.execute(q, {"u": upload_id, "t": text, "m": model})
        self.db.commit()

    def insert_chunk(self, document_id, chunk_text, embedding):
        # si usas pgvector, la columna embedding es vector(1536)
        q = text("INSERT INTO chunks (document_id, chunk_text, embedding) VALUES (:d,:c,:e)")
        self.db.execute(q, {"d": document_id, "c": chunk_text, "e": embedding})
        self.db.commit()

    def update_upload_status(self, upload_id, status):
        q = text("UPDATE uploads SET status=:s WHERE id=:id")
        self.db.execute(q, {"s": status, "id": upload_id})
        self.db.commit()
