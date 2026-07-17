CREATE TABLE IF NOT EXISTS metadata.file_status(
    file_id TEXT,
    filename TEXT,
    file_location TEXT,
    last_modified TIMESTAMP,
    status VARCHAR(10),
    first_found_date TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_file_id ON metadata.file_status(file_id);