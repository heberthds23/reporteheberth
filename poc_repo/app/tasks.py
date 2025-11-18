from celery import Celery
import os
from app.db import DB
import openai
from app.embeddings import get_embedding
from app.utils import chunk_text

broker = os.getenv('REDIS_URL', 'redis://redis:6379/0')
celery = Celery('tasks', broker=broker)
openai.api_key = os.getenv('OPENAI_API_KEY')

@celery.task
def enqueue_process(upload_id: int, filepath: str):
    db = DB()
    # 1) Transcribir (si OpenAI key está presente)
    text = ''
    try:
        with open(filepath, 'rb') as audio_file:
            resp = openai.Audio.transcribe('whisper-1', audio_file)
            text = resp.get('text','')
    except Exception as e:
        # si falla la transcripción, guardar error y salir
        db.update_upload_status(upload_id, 'failed_transcription')
        return
    db.insert_transcription(upload_id, text, 'whisper-1')
    # 2) chunk + embeddings
    chunks = chunk_text(text)
    for c in chunks:
        emb = get_embedding(c)
        db.insert_chunk(upload_id, c, emb)
    db.update_upload_status(upload_id, 'processed')
