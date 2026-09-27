"""
Backfill embeddings for all schemes in the government_schemes table.

Run from the backend/ directory:
    cd govassist/backend
    python ../scripts/backfill_embeddings.py

What it does:
  1. Loads BAAI/bge-small-en-v1.5 locally via sentence-transformers
  2. Fetches every scheme whose `embedding` column is NULL
  3. Concatenates scheme text fields into a single string
  4. Encodes in batches of 32
  5. UPDATEs each row via the Supabase service-role client

After running this once, new schemes added via the seed script or admin
panel will also need embeddings — re-run this script or call the
/admin/schemes/backfill endpoint (if you add one later).
"""

import sys
import os
import asyncio

# ── make sure we can import app modules ─────────────────────────────────────
BACKEND_DIR = os.path.join(os.path.dirname(__file__), "..", "backend")
sys.path.insert(0, BACKEND_DIR)

from dotenv import load_dotenv
load_dotenv(os.path.join(BACKEND_DIR, ".env"))

from supabase import create_client
from sentence_transformers import SentenceTransformer

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
MODEL_NAME = "BAAI/bge-small-en-v1.5"
BATCH_SIZE = 32

db = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def build_scheme_text(scheme: dict) -> str:
    """Same logic as embeddings.build_scheme_text — must stay in sync."""
    parts = [
        scheme.get("scheme_name", ""),
        scheme.get("details", ""),
        scheme.get("benefits", ""),
        scheme.get("eligibility", ""),
        scheme.get("scheme_category", ""),
        scheme.get("level", ""),
    ]
    tags = scheme.get("tags") or []
    if tags:
        parts.append(" ".join(tags))
    return " ".join(p for p in parts if p).strip()


def pgvector_literal(vec: list) -> str:
    return "[" + ",".join(f"{v:.8f}" for v in vec) + "]"


def fetch_schemes_without_embeddings() -> list:
    """Fetch all schemes that have no embedding yet."""
    result = (
        db.table("government_schemes")
        .select("id, scheme_name, details, benefits, eligibility, scheme_category, level, tags")
        .is_("embedding", "null")
        .execute()
    )
    return result.data or []


def fetch_all_schemes() -> list:
    """Fetch ALL schemes (use when regenerating all embeddings)."""
    result = (
        db.table("government_schemes")
        .select("id, scheme_name, details, benefits, eligibility, scheme_category, level, tags")
        .execute()
    )
    return result.data or []


def update_embedding(scheme_id: str, vec_literal: str):
    db.table("government_schemes").update(
        {"embedding": vec_literal}
    ).eq("id", scheme_id).execute()


def run(regenerate_all: bool = False):
    print(f"Loading model: {MODEL_NAME} ...")
    model = SentenceTransformer(MODEL_NAME)
    print("Model loaded.\n")

    if regenerate_all:
        schemes = fetch_all_schemes()
        print(f"Regenerating embeddings for ALL {len(schemes)} schemes.")
    else:
        schemes = fetch_schemes_without_embeddings()
        print(f"Found {len(schemes)} schemes without embeddings.")

    if not schemes:
        print("Nothing to do. All schemes already have embeddings.")
        return

    # Build text corpus
    texts = [build_scheme_text(s) for s in schemes]

    # Encode in batches — normalize so cosine sim == dot product
    print(f"Encoding {len(texts)} schemes in batches of {BATCH_SIZE} ...")
    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=BATCH_SIZE,
        show_progress_bar=True,
    )

    # Push to Supabase
    print("\nUploading embeddings to Supabase ...")
    success = 0
    errors = 0
    for scheme, vec in zip(schemes, vectors):
        try:
            update_embedding(str(scheme["id"]), pgvector_literal(vec.tolist()))
            success += 1
        except Exception as e:
            print(f"  ❌  {scheme['scheme_name']}: {e}")
            errors += 1

    print(f"\n✅  Done — {success} updated, {errors} errors.")


if __name__ == "__main__":
    # Pass --all flag to regenerate every embedding, not just missing ones
    regenerate_all = "--all" in sys.argv
    run(regenerate_all=regenerate_all)
