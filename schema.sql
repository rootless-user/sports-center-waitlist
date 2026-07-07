CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    social_contact TEXT,
    preferred_days TEXT,
    preferred_time TEXT,
    trainer_preference TEXT,
    status TEXT NOT NULL DEFAULT 'Ожидает',
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);