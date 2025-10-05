from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import rewrite

app = FastAPI(
    title="TailorMyCV API",
    description="AI-powered CV tailoring backend"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rewrite.router, prefix="/api")
