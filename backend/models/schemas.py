from pydantic import BaseModel
from typing import List

class RewriteResponse(BaseModel):
    match_score: float
    before: List[str]
    after: List[str]
    download_url: str # Add this line
