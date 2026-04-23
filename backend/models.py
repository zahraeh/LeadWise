"""
models.py — LeadWise Core
Pydantic data models shared across the backend.
"""

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


class LeadStatus(str, Enum):
    HOT = "Hot"
    WARM = "Warm"
    COLD = "Cold"


class Lead(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    opt_in: bool
    industry: str
    fields: Dict[str, Any] = {}


class ScoreResult(BaseModel):
    lead_email: str
    score: float
    status: LeadStatus
    reason: str
    recommended_action: str
    industry: str
