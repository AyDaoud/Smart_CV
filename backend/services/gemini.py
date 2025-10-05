# backend/services/gemini.py
from __future__ import annotations
import os
from typing import List, Tuple, Set
from dotenv import load_dotenv

# NEW SDK:
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY missing in backend/.env")

# Force stable v1 and pass our key explicitly
client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(api_version="v1")
)

# Choose your model via env; default to price/perf friendly Flash.
# To use 2.5 Pro, set GEMINI_MODEL=gemini-2.5-pro in backend/.env
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

GEMINI_PROMPT_TEMPLATE = """
You are an expert CV writing assistant. Rewrite the single bullet point below to better align with the job description.
- Use action verbs
- Keep it to 1–2 lines
- Quantify impact if possible
- Do NOT invent facts; only enhance wording
Return ONLY the rewritten bullet (no extra text).

Job keywords: {job_keywords}

Original bullet:
{cv_bullet}

Rewritten bullet:
"""

def _clean(s: str) -> str:
    return (s or "").strip().lstrip("*-• ").strip()

def rewrite_bullets(cv_text: str, job_description: str, job_keywords: Set[str]) -> Tuple[List[str], List[str]]:
    original_bullets = [b.strip() for b in cv_text.splitlines() if b.strip()]
    rewritten_bullets: List[str] = []
    keywords_str = ", ".join(sorted(job_keywords))[:300]

    print(f"[Gemini] Using model: {MODEL}")
    for bullet in original_bullets:
        if len(bullet) < 15:
            rewritten_bullets.append(bullet)
            continue

        prompt = GEMINI_PROMPT_TEMPLATE.format(job_keywords=keywords_str, cv_bullet=bullet)
        try:
            resp = client.models.generate_content(model=MODEL, contents=prompt)
            text = getattr(resp, "text", "") or ""
            rewritten_bullets.append(_clean(text) or bullet)
        except Exception as e:
            # soft fallback to Flash if Pro isn't enabled on your key
            if MODEL != "gemini-2.5-flash":
                try:
                    print(f"[Gemini] {e} → falling back to gemini-2.5-flash")
                    resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                    rewritten_bullets.append(_clean(resp.text) or bullet)
                    continue
                except Exception as e2:
                    print(f"[Gemini] fallback error: {e2}")
            rewritten_bullets.append(bullet)

    return rewritten_bullets, original_bullets
