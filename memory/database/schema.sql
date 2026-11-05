-- Phase 09 - Memory DB Schema - SQLite
-- All tables local only, encrypted in Phase 16

CREATE TABLE IF NOT EXISTS short_term_memory (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  role TEXT NOT NULL,
  text TEXT NOT NULL,
  emotion TEXT,
  created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS long_term_memory (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  key TEXT UNIQUE NOT NULL,
  value TEXT NOT NULL,
  category TEXT, -- preference, important, fact, goal
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS conversation_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  user_text TEXT,
  aira_text TEXT,
  emotion TEXT,
  created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS user_preferences (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS important_info (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  detail TEXT,
  is_important INTEGER DEFAULT 0,
  created_at INTEGER NOT NULL
);
