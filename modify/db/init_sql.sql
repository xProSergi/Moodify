CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_name TEXT,
    track_name TEXT,
    genre TEXT,
    danceability REAL,
    energy REAL,
    valence REAL,
    tempo REAL,
    acousticness REAL,
    instrumentalness REAL,
    liveness REAL,
    loudness REAL,
    speechiness REAL,
    duration_ms INTEGER,
    mood_inferido TEXT
);
