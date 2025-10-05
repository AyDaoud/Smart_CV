# backend/services/storage.py
from __future__ import annotations

import io
import os
import uuid
import unicodedata
from typing import List

from dotenv import load_dotenv
from fpdf import FPDF
from supabase import create_client, Client

load_dotenv()

# ----- Config -----
BUCKET_NAME = "cvs"  # <-- define BEFORE using it

SUPABASE_URL: str | None = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str | None = os.getenv("SUPABASE_KEY")  # use service_role on server

print("--- DEBUG ---")
print(f"Supabase URL Loaded: {SUPABASE_URL}")
print(f"Supabase Key Loaded: {'Exists' if SUPABASE_KEY else 'Not Found!'}")
print("-------------")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in backend/.env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def _ensure_bucket(bucket: str, public: bool = True):
    """Create bucket if it doesn't exist. Safe to leave in production."""
    try:
        # some client versions accept a dict of options, others accept kwargs;
        # this works on recent supabase-py:
        supabase.storage.create_bucket(bucket, {"public": public})
        print(f"[Supabase] Created bucket '{bucket}' (public={public}).")
    except Exception as e:
        msg = str(e).lower()
        if "already exists" in msg or "exists" in msg:
            print(f"[Supabase] Bucket '{bucket}' already exists.")
        else:
            print(f"[Supabase] create_bucket warn: {e}")

# Ensure bucket now that BUCKET_NAME is defined
_ensure_bucket(BUCKET_NAME, public=True)

# ----- Font path (Unicode) -----
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # -> backend/
FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")
FONTPATH = os.path.join(FONTS_DIR, "DejaVuSans.ttf")  # ensure this file exists


def _normalize_text(s: str) -> str:
    """Normalize ligatures and compatibility forms that break PDFs."""
    s = (s or "").replace("\ufb01", "fi").replace("\ufb02", "fl")  # common ligatures
    return unicodedata.normalize("NFKC", s)


class PDF(FPDF):
    """FPDF with Unicode font support and a simple header."""

    def _ensure_unicode_font(self, size: int = 12, bold: bool = False) -> None:
        if os.path.exists(FONTPATH):
            if "DejaVu" not in self.fonts:
                # Register TrueType font with Unicode support (fpdf2)
                self.add_font("DejaVu", "", FONTPATH, uni=True)
            self.set_font("DejaVu", "", size)
        else:
            # Fallback to a core font (not full-Unicode). Keep DejaVu present ideally.
            self.set_font("Helvetica", "B" if bold else "", size)

    def header(self):
        self._ensure_unicode_font(size=12, bold=True)
        self.cell(0, 10, _normalize_text("Tailored CV"), 0, 1, "C")
        self.ln(5)


def _build_pdf_bytes(rewritten_text: str) -> bytes:
    """Render rewritten text to a PDF and return raw bytes."""
    pdf = PDF()
    pdf.add_page()
    pdf._ensure_unicode_font(size=10, bold=False)
    pdf.multi_cell(0, 6, _normalize_text(rewritten_text))

    buf = io.BytesIO()
    pdf.output(buf)  # fpdf2 can write directly to file-like objects
    return buf.getvalue()


async def save_cv(filename: str, original_file_content: bytes, rewritten_bullets: List[str]) -> str:
    """
    Generates a PDF from rewritten bullets, uploads it (and the original file) to Supabase,
    and returns a public URL or a signed URL.
    """
    # Join bullets into a single body
    rewritten_text = "\n".join(b for b in (rewritten_bullets or []) if b)
    pdf_bytes = _build_pdf_bytes(rewritten_text)

    uid = uuid.uuid4().hex
    original_path = f"originals/{uid}-{filename}"
    new_filename = os.path.splitext(filename)[0] + ".pdf"
    rewritten_path = f"rewritten/{uid}-Tailored-{new_filename}"

    # Upload original
    try:
        supabase.storage.from_(BUCKET_NAME).upload(
            path=original_path,
            file=original_file_content,
            file_options={"content-type": "application/octet-stream"},
        )
    except Exception as e:
        print(f"[Supabase] Upload ORIGINAL failed: {e}")

    # Upload rewritten PDF
    try:
        supabase.storage.from_(BUCKET_NAME).upload(
            path=rewritten_path,
            file=pdf_bytes,
            file_options={"content-type": "application/pdf"},
        )
    except Exception as e:
        print(f"[Supabase] Upload REWRITTEN failed: {e}")
        return ""

    # Try to return a public URL (bucket must be public or have read policy)
    try:
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(rewritten_path)
        if public_url:
            return public_url
    except Exception as e:
        print(f"[Supabase] get_public_url failed: {e}")

    # Fallback: signed URL (valid 7 days)
    try:
        signed = supabase.storage.from_(BUCKET_NAME).create_signed_url(
            rewritten_path, 60 * 60 * 24 * 7
        )
        if isinstance(signed, dict):
            return signed.get("signedURL") or signed.get("signed_url", "")
        return signed or ""
    except Exception as e:
        print(f"[Supabase] create_signed_url failed: {e}")
        return ""
