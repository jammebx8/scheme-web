-- ============================================================
-- GovAssist Full Database Migration
-- Run this in Supabase SQL editor (Dashboard → SQL Editor)
-- ============================================================

-- ── Users ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email            TEXT UNIQUE NOT NULL,
    password_hash    TEXT,
    full_name        TEXT,
    phone            TEXT,
    date_of_birth    DATE,
    gender           TEXT,
    state            TEXT,
    district         TEXT,
    annual_income    NUMERIC,
    caste_category   TEXT,        -- GEN, OBC, SC, ST, EWS
    is_student       BOOLEAN DEFAULT FALSE,
    is_farmer        BOOLEAN DEFAULT FALSE,
    occupation       TEXT,
    disability_status BOOLEAN DEFAULT FALSE,
    profile_complete  BOOLEAN DEFAULT FALSE,
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    updated_at       TIMESTAMPTZ DEFAULT NOW()
);

-- ── Government Schemes ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS government_schemes (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scheme_name      TEXT NOT NULL,
    slug             TEXT NOT NULL UNIQUE,
    details          TEXT NOT NULL,
    benefits         TEXT NOT NULL,
    eligibility      TEXT NOT NULL,
    application      TEXT,
    documents        TEXT,
    level            VARCHAR(30) NOT NULL,
    scheme_category  VARCHAR(100) NOT NULL,
    tags             TEXT[],
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    updated_at       TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for schemes
CREATE INDEX IF NOT EXISTS idx_scheme_category ON government_schemes(scheme_category);
CREATE INDEX IF NOT EXISTS idx_level ON government_schemes(level);
CREATE INDEX IF NOT EXISTS idx_tags ON government_schemes USING GIN(tags);

-- Full-text search column
ALTER TABLE government_schemes
    ADD COLUMN IF NOT EXISTS search_vector tsvector
    GENERATED ALWAYS AS (
        to_tsvector(
            'english',
            coalesce(scheme_name, '') || ' ' ||
            coalesce(details, '') || ' ' ||
            coalesce(benefits, '') || ' ' ||
            coalesce(eligibility, '') || ' ' ||
            coalesce(tags::text, '')
        )
    ) STORED;

CREATE INDEX IF NOT EXISTS idx_scheme_search ON government_schemes USING GIN(search_vector);

-- ── User Documents ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_documents (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id          UUID REFERENCES users(id) ON DELETE CASCADE,
    doc_type         TEXT NOT NULL,
    file_url         TEXT,
    digilocker_uri   TEXT,
    extracted_data   JSONB,
    verified         BOOLEAN DEFAULT FALSE,
    uploaded_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_documents_user_id ON user_documents(user_id);
CREATE INDEX IF NOT EXISTS idx_user_documents_doc_type ON user_documents(doc_type);

-- ── Application Jobs ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS application_jobs (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id              UUID REFERENCES users(id) ON DELETE CASCADE,
    scheme_id            UUID REFERENCES government_schemes(id),
    status               TEXT DEFAULT 'queued'
                         CHECK (status IN ('queued','running','completed','failed','needs_review')),
    agent_log            JSONB DEFAULT '[]'::jsonb,
    screenshot_urls      TEXT[] DEFAULT ARRAY[]::TEXT[],
    application_ref_id   TEXT,
    error_details        TEXT,
    started_at           TIMESTAMPTZ,
    completed_at         TIMESTAMPTZ,
    created_at           TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_jobs_user_id ON application_jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON application_jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_created ON application_jobs(created_at DESC);

-- ── User Eligibility Cache ─────────────────────────────────
CREATE TABLE IF NOT EXISTS user_eligibility (
    user_id              UUID REFERENCES users(id) ON DELETE CASCADE,
    scheme_id            UUID REFERENCES government_schemes(id) ON DELETE CASCADE,
    eligible             BOOLEAN,
    eligibility_reason   TEXT,
    last_checked         TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, scheme_id)
);

CREATE INDEX IF NOT EXISTS idx_eligibility_user ON user_eligibility(user_id, eligible);

-- ── Row Level Security ─────────────────────────────────────
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE application_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_eligibility ENABLE ROW LEVEL SECURITY;
ALTER TABLE government_schemes ENABLE ROW LEVEL SECURITY;

-- Service role bypasses RLS (used by FastAPI backend)
-- Public read for schemes
CREATE POLICY IF NOT EXISTS "schemes_public_read" ON government_schemes
    FOR SELECT USING (true);

-- Users can only see their own data
CREATE POLICY IF NOT EXISTS "users_self_access" ON users
    FOR ALL USING (auth.uid()::text = id::text);

CREATE POLICY IF NOT EXISTS "documents_self_access" ON user_documents
    FOR ALL USING (auth.uid()::text = user_id::text);

CREATE POLICY IF NOT EXISTS "jobs_self_access" ON application_jobs
    FOR ALL USING (auth.uid()::text = user_id::text);

CREATE POLICY IF NOT EXISTS "eligibility_self_access" ON user_eligibility
    FOR ALL USING (auth.uid()::text = user_id::text);

-- ── Supabase Storage Buckets ───────────────────────────────
-- Run these separately in Supabase Dashboard → Storage → New Bucket:
-- 1. Create bucket: "govassist-documents"  (private, max 10MB)
-- 2. Create bucket: "govassist-screenshots" (public,  max 5MB)

-- ── Updated_at trigger ────────────────────────────────────
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_schemes_updated_at
    BEFORE UPDATE ON government_schemes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ── AI Scheme Summaries Cache ──────────────────────────────
-- Stores Groq-generated plain-English summaries so the LLM is called
-- only once per scheme.  The FastAPI backend writes here on first visit.
CREATE TABLE IF NOT EXISTS scheme_summaries (
    scheme_id            UUID PRIMARY KEY REFERENCES government_schemes(id) ON DELETE CASCADE,
    summary              TEXT NOT NULL,
    benefits_simple      TEXT NOT NULL,
    eligibility_simple   TEXT NOT NULL,
    documents_simple     TEXT NOT NULL,
    generated_at         TIMESTAMPTZ DEFAULT NOW()
);

-- Service role can read/write; public can only read
ALTER TABLE scheme_summaries ENABLE ROW LEVEL SECURITY;

CREATE POLICY IF NOT EXISTS "summaries_public_read" ON scheme_summaries
    FOR SELECT USING (true);
