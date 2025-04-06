DROP INDEX IF EXISTS ix_movie_id;
DROP INDEX IF EXISTS ix_movie_imdb_id;
DROP TABLE IF EXISTS rating;
DROP TABLE IF EXISTS movie;


CREATE TABLE IF NOT EXISTS movie (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    year int NOT NULL,
    rated VARCHAR,
    released DATE,
    runtime VARCHAR,
    genre VARCHAR,
    director VARCHAR,
    writer VARCHAR,
    actors VARCHAR,
    plot VARCHAR,
    language VARCHAR,
    country VARCHAR,
    awards VARCHAR,
    poster VARCHAR,
    metascore INTEGER,
    imdb_rating FLOAT,
    imdb_votes INTEGER,
    imdb_id VARCHAR NOT NULL UNIQUE,
    type VARCHAR NOT NULL,
    dvd VARCHAR,
    box_office VARCHAR,
    production VARCHAR,
    website VARCHAR
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
