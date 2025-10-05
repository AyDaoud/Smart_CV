# backend/routers/rewrite.py
from fastapi import APIRouter, UploadFile, File, Form
from models.schemas import RewriteResponse
from services import parser, nlp, gemini, storage

router = APIRouter()

@router.post("/rewrite", response_model=RewriteResponse)
async def rewrite_cv(
    cv_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Read file content once and keep it
    original_file_content = await cv_file.read()
    await cv_file.seek(0) # Reset file pointer for parsing

    # 1. Parse CV
    cv_text = await parser.extract_text(cv_file)
    
    # 2. Extract keywords from job description
    job_keywords = nlp.extract_keywords(job_description)
    
    # 3. Rewrite bullets using Gemini
    rewritten, before = gemini.rewrite_bullets(cv_text, job_description, job_keywords)
    
    # 4. Compute match score
    rewritten_full_text = "\n".join(rewritten)
    match_score = nlp.compute_match_score(rewritten_full_text, job_keywords)
    
    # 5. Store in Supabase and get download URL
    download_url = await storage.save_cv(cv_file.filename, original_file_content, rewritten)
    
    # 6. Return response
    return RewriteResponse(
        match_score=match_score, 
        before=before, 
        after=rewritten, 
        download_url=download_url
    )