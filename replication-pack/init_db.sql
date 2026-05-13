-- init_db.sql
-- Initialize the observations table for Engram Persistence Bridge

CREATE TABLE IF NOT EXISTS observations (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    type TEXT,
    project TEXT,
    topic_key TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster sync lookups
CREATE INDEX IF NOT EXISTS idx_topic_key ON observations(topic_key);
CREATE INDEX IF NOT EXISTS idx_title ON observations(title);
