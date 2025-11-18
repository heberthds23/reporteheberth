-- habilitar pgvector si está disponible
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS uploads (
  id BIGSERIAL PRIMARY KEY,
  source VARCHAR(255),
  filename VARCHAR(512),
  storage_url TEXT,
  file_type VARCHAR(50),
  size_bytes BIGINT,
  status VARCHAR(50) DEFAULT 'uploaded',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS transcriptions (
  id BIGSERIAL PRIMARY KEY,
  upload_id BIGINT REFERENCES uploads(id),
  text TEXT,
  model VARCHAR(100),
  duration_seconds INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS documents (
  id BIGSERIAL PRIMARY KEY,
  upload_id BIGINT REFERENCES uploads(id),
  meta JSONB,
  processed BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS chunks (
  id BIGSERIAL PRIMARY KEY,
  document_id BIGINT REFERENCES documents(id),
  chunk_text TEXT,
  embedding vector(1536),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
