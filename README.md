# Smart_CV

modify any CV to a given job description.

- **Backend:** FastAPI (Python)
- **Frontend:** Next.js + TypeScript
- **Storage:** Supabase (public bucket or signed URLs)
- **LLM:** Google Gemini

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Install & Run (Windows)](#install--run-windows)
  - [Backend (FastAPI)](#backend-fastapi)
  - [Frontend (Nextjs)](#frontend-nextjs)
- [Supabase Setup](#supabase-setup)
- [Gemini Model Notes](#gemini-model-notes)
- [Unicode PDF Fonts](#unicode-pdf-fonts)
- [API Usage (Swagger)](#api-usage-swagger)
- [GitHub: Ignore Big Folders & Push](#github-ignore-big-folders--push)
  - [A) First-time push](#a-first-time-push)
  - [B) If you previously pushed large files](#b-if-you-previously-pushed-large-files)
- [.gitignore (put at repo root)](#gitignore-put-at-repo-root)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Prerequisites

- **Windows PowerShell**
- **Python 3.10+**
- **Node.js 18+ and npm**
- **Git**

Verify:

```powershell
python --version
node -v
npm -v
git --version



Smart_CV/
├─ backend/
│  ├─ assets/fonts/DejaVuSans.ttf      # Unicode TTF for PDF (required)
│  ├─ main.py                          # FastAPI entrypoint
│  ├─ routers/ services/ models/
│  ├─ requirements.txt
│  └─ .env                             # NOT committed
├─ frontend/
│  ├─ pages/ components/ utils/
│  ├─ package.json  tsconfig.json  tailwind.config.js
│  └─ .env.local (optional)
└─ README.md 


GOOGLE_API_KEY=your_gemini_api_key
SUPABASE_URL=https://YOUR-PROJECT.supabase.co
SUPABASE_KEY=your_service_role_key   # service_role only on server 



NEXT_PUBLIC_BACKEND_URL=http://localhost:8000


cd .\backend

# Create & activate virtual env
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install deps
pip install -r requirements.txt

# Ensure Unicode font exists:
# backend\assets\fonts\DejaVuSans.ttf  (see "Unicode PDF Fonts")

# Run API
uvicorn main:app --reload --host 0.0.0.0 --port 8000
 

cd .\frontend
npm install
npm run dev
