DROP INDEX IF EXISTS ix_movie_id;
DROP INDEX IF EXISTS ix_movie_imdb_id;
DROP TABLE IF EXISTS movie;
CREATE TABLE IF NOT EXISTS movie (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    year VARCHAR(255),
    imdb_id VARCHAR(255) UNIQUE,
    type VARCHAR(255),
    poster VARCHAR(255)
);

CREATE INDEX IF NOT EXISTS ix_movie_id ON movie(id);

CREATE INDEX IF NOT EXISTS ix_movie_imdb_id ON movie(imdb_id);
