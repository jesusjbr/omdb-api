DROP INDEX IF EXISTS ix_movie_id;
DROP INDEX IF EXISTS ix_movie_imdb_id;
DROP TABLE IF EXISTS rating;
DROP TABLE IF EXISTS movie;


CREATE TABLE IF NOT EXISTS movie (
    id SERIAL PRIMARY KEY,
    title TEXT,
    year TEXT,
    rated TEXT,
    released TEXT,
    runtime TEXT,
    genre TEXT,
    director TEXT,
    writer TEXT,
    actors TEXT,
    plot TEXT,
    language TEXT,
    country TEXT,
    awards TEXT,
    poster TEXT,
    metascore TEXT,
    imdb_rating TEXT,
    imdb_votes TEXT,
    imdb_id TEXT UNIQUE,
    type TEXT,
    dvd TEXT,
    box_office TEXT,
    production TEXT,
    website TEXT
);

CREATE INDEX IF NOT EXISTS ix_movie_id ON movie(id);
CREATE INDEX IF NOT EXISTS ix_movie_imdb_id ON movie(imdb_id);

CREATE TABLE IF NOT EXISTS rating (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER REFERENCES movie(id) ON DELETE CASCADE,
    source TEXT,
    value TEXT,
    UNIQUE(movie_id, source, value)
);
