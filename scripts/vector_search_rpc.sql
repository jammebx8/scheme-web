-- ============================================================
-- Run this in Supabase SQL Editor ONCE before using vector search.
-- It creates the RPC function called by GET /schemes/search and
-- GET /schemes/recommend in the FastAPI backend.
-- ============================================================

-- Make sure pgvector extension is enabled (it should already be from your schema)
CREATE EXTENSION IF NOT EXISTS vector;

-- ─────────────────────────────────────────────────────────────
-- search_schemes_by_embedding
--
-- Performs cosine-similarity search over government_schemes.embedding
-- using the pgvector HNSW index (idx_government_schemes_embedding).
--
-- Parameters:
--   query_embedding  vector(384) as text   — the query/user-profile vector
--   match_count      int                   — how many results to return
--   category_filter  text / NULL           — optional scheme_category filter
--   level_filter     text / NULL           — optional level filter ("Central" / "State")
--
-- Returns columns that match what SchemeCard expects on the frontend.
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION search_schemes_by_embedding(
    query_embedding  text,         -- passed as a string like "[0.12,0.34,...]"
    match_count      int  DEFAULT 20,
    category_filter  text DEFAULT NULL,
    level_filter     text DEFAULT NULL
)
RETURNS TABLE (
    id               uuid,
    scheme_name      text,
    slug             text,
    details          text,
    benefits         text,
    eligibility      text,
    application      text,
    documents        text,
    level            varchar(30),
    scheme_category  text,
    tags             text[],
    similarity       float
)
LANGUAGE plpgsql
STABLE
AS $$
BEGIN
    RETURN QUERY
    SELECT
        gs.id,
        gs.scheme_name,
        gs.slug,
        gs.details,
        gs.benefits,
        gs.eligibility,
        gs.application,
        gs.documents,
        gs.level,
        gs.scheme_category,
        gs.tags,
        -- cosine similarity: 1 - cosine distance
        (1 - (gs.embedding <=> query_embedding::vector)) AS similarity
    FROM government_schemes gs
    WHERE
        gs.embedding IS NOT NULL
        AND (category_filter IS NULL OR gs.scheme_category = category_filter)
        AND (level_filter     IS NULL OR gs.level           = level_filter)
    ORDER BY gs.embedding <=> query_embedding::vector   -- uses HNSW index
    LIMIT match_count;
END;
$$;

-- Grant execute to the anon and authenticated roles used by Supabase
GRANT EXECUTE ON FUNCTION search_schemes_by_embedding(text, int, text, text)
    TO anon, authenticated, service_role;


-- ─────────────────────────────────────────────────────────────
-- Trigger function: auto-generate search_vector on INSERT/UPDATE
-- (You likely already have this from your schema — included for completeness)
-- ─────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION government_schemes_search_vector_update()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.search_vector := to_tsvector(
        'english',
        coalesce(NEW.scheme_name, '') || ' ' ||
        coalesce(NEW.details,     '') || ' ' ||
        coalesce(NEW.benefits,    '') || ' ' ||
        coalesce(NEW.eligibility, '') || ' ' ||
        coalesce(array_to_string(NEW.tags, ' '), '')
    );
    RETURN NEW;
END;
$$;

-- Only create the trigger if it doesn't exist already
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger
        WHERE tgname = 'trg_search_vector_update'
          AND tgrelid = 'government_schemes'::regclass
    ) THEN
        CREATE TRIGGER trg_search_vector_update
        BEFORE INSERT OR UPDATE ON government_schemes
        FOR EACH ROW EXECUTE FUNCTION government_schemes_search_vector_update();
    END IF;
END $$;
