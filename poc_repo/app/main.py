from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import base64, uuid, os
from pathlib import Path
from app.db import DB
from app.tasks import enqueue_process

app = FastAPI()
UPLOAD_DIR = Path('/app/uploads')
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class WebhookPayload(BaseModel):
    filename: str
    data_base64: str
    source: str | None = None

@app.post('/webhook')
async def webhook(payload: WebhookPayload):
    try:
        content = base64.b64decode(payload.data_base64)
    except Exception:
        raise HTTPException(status_code=400, detail='base64 inválido')
    file_id = str(uuid.uuid4())
    fname = f"{file_id}_{payload.filename}"
    path = UPLOAD_DIR / fname
    with open(path, 'wb') as f:
        f.write(content)
    db = DB()
    upload_id = db.insert_upload(payload.source, fname, str(path), 'audio', len(content))
    # encolar tarea Celery
    enqueue_process.delay(upload_id, str(path))
    return {"upload_id": upload_id, "status": "queued"}

@app.get('/uploads/{upload_id}')
async def get_upload(upload_id: int):
    db = DB()
    return db.get_upload(upload_id)
