"""
AI Legal Assistant — FastAPI Application
Main entry point for the backend API server.
Serves both the API and the frontend static files in production.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import router
from app.api.auth_routes import auth_router
from app.models.schemas import HealthResponse
from app.database import init_db


# ─── Application Setup ───────────────────────────────────

app = FastAPI(
    title="AI Legal Assistant",
    description=(
        "An AI-powered legal assistant for Indian contract analysis, "
        "risk detection, compliance checking, and draft generation. "
        "Supports PDF, DOCX, and scanned document uploads."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ─── CORS Middleware ─────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Include API Routes ─────────────────────────────────

app.include_router(router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])


# ─── Database Init ───────────────────────────────────────

@app.on_event("startup")
def on_startup():
    init_db()


# ─── Root & Health Endpoints ─────────────────────────────

@app.get("/api/diag/groq")
async def diag_groq():
    """Diagnostic endpoint to check Groq connectivity."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"status": "error", "message": "GROQ_API_KEY is missing from environment"}
    
    from app.services.nlu import _groq_client
    try:
        from groq import Groq
        client = Groq(api_key=api_key.strip())
        test_response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5
        )
        return {
            "status": "success",
            "message": "Groq is connected",
            "api_key_prefix": api_key.strip()[:8] + "...",
            "response": test_response.choices[0].message.content
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Groq Error: {str(e)}",
            "api_key_prefix": api_key.strip()[:8] + "..." if api_key else "None"
        }


@app.get("/health")
async def health():
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        features=[
            "Contract Upload & Parsing (PDF, DOCX, OCR)",
            "Clause Segmentation & Classification",
            "Risk Detection & Analysis",
            "Indian Law Compliance Check",
            "Party & Obligation Extraction",
            "Contract Summarization",
            "AI Chat Assistant (Groq LLM)",
            "India-Compliant Draft Generation",
        ],
    )


# ─── Serve Frontend Static Files (Production) ───────────

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")

if os.path.exists(STATIC_DIR):
    # Serve static assets (JS, CSS, images)
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")

    # Catch-all: serve index.html for any non-API route (SPA routing)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Don't serve index.html for API or docs routes
        if full_path.startswith(("api/", "docs", "redoc", "openapi", "health")):
            return
        file_path = os.path.join(STATIC_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))
else:
    @app.get("/")
    async def root():
        return {
            "message": "AI Legal Assistant API",
            "version": "1.0.0",
            "docs": "/docs",
            "note": "Frontend not built. Run 'npm run build' in the frontend directory.",
        }
