"""
main.py — LeadWise Core
FastAPI backend exposing lead scoring endpoints.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import Lead, ScoreResult
from backend.scoring_agent import score_lead
from backend.config import get_config

app = FastAPI(
    title="LeadWise Core API",
    description="AI-powered lead scoring engine. Industry-agnostic.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    config = get_config()
    return {
        "product": "LeadWise Core",
        "industry": config["name"],
        "company": config["company"],
        "status": "running",
    }


@app.get("/config")
def config_endpoint():
    """Return the active industry configuration (used by the frontend)."""
    return get_config()


@app.post("/score", response_model=ScoreResult)
def score_endpoint(lead: Lead):
    """
    Submit a lead for AI scoring.
    Returns score (0–10), status (Hot/Warm/Cold), reason, and recommended action.
    """
    try:
        result = score_lead(lead)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
