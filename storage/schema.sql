PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS atlas_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS concepts (
    id INTEGER PRIMARY KEY CHECK (id > 0),
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL CHECK (length(trim(title)) > 0),
    summary TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    normalized_name TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS concept_tags (
    concept_id INTEGER NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (concept_id, tag_id)
);

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY,
    concept_id INTEGER NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    locator TEXT NOT NULL,
    UNIQUE (concept_id, title, locator)
);

CREATE TABLE IF NOT EXISTS relations (
    id INTEGER PRIMARY KEY,
    from_concept_id INTEGER NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    to_concept_id INTEGER NOT NULL REFERENCES concepts(id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL,
    weight REAL NOT NULL DEFAULT 1.0 CHECK (weight > 0),
    note TEXT NOT NULL DEFAULT '',
    CHECK (from_concept_id <> to_concept_id),
    UNIQUE (from_concept_id, to_concept_id, relation_type)
);

CREATE INDEX IF NOT EXISTS idx_relations_from ON relations(from_concept_id);
CREATE INDEX IF NOT EXISTS idx_relations_to ON relations(to_concept_id);
CREATE INDEX IF NOT EXISTS idx_sources_concept ON sources(concept_id);

INSERT OR IGNORE INTO atlas_meta(key, value) VALUES ('schema_version', '1');
