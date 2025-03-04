CREATE TABLE IF NOT EXISTS public.telegram_posts (
  id SERIAL PRIMARY KEY,
  channel_id TEXT NOT NULL,
  message_id BIGINT NOT NULL,
  published_at TIMESTAMP NOT NULL,
  text TEXT,
  views INTEGER,
  collected_at TIMESTAMP DEFAULT NOW(),
  CONSTRAINT unique_channel_message UNIQUE (channel_id, message_id)
);