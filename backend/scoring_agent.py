"""
scoring_agent.py — LeadWise Core
AI scoring agent powered by Claude API (Anthropic).
Takes a Lead, returns a ScoreResult.
"""

import json
import os

import anthropic

from backend.config import CONFIGS
from backend.models import Lead, LeadStatus, ScoreResult


def score_lead(lead: Lead) -> ScoreResult:
    """
    Send lead data to Claude API and get back a structured score.
    Returns a ScoreResult with score (0–10), status, reason, and action.
    """

    # GDPR gate — no opt-in, no scoring
    if not lead.opt_in:
        return ScoreResult(
            lead_email=lead.email,
            score=0.0,
            status=LeadStatus.COLD,
            reason="Lead sans consentement RGPD. Scoring impossible.",
            recommended_action="Envoyer email de demande de consentement.",
            industry=lead.industry,
        )

    config = CONFIGS.get(lead.industry)
    if not config:
        raise ValueError(f"Unknown industry: {lead.industry}")

    scoring_context = config["scoring_context"]

    prompt = f"""
{scoring_context}

Here is the lead to evaluate:
- Name: {lead.first_name} {lead.last_name}
- Email: {lead.email}
- GDPR opt-in: {lead.opt_in}
- Industry fields: {json.dumps(lead.fields, ensure_ascii=False)}

Respond ONLY with a valid JSON object — no preamble, no markdown, no explanation outside the JSON.
The JSON must have exactly these fields:
{{
  "score": <float between 0 and 10>,
  "status": <"Hot", "Warm", or "Cold">,
  "reason": <one sentence explaining the score in French>,
  "recommended_action": <one concrete next action for the sales advisor in French>
}}
"""

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()

    # Clean potential markdown fences
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Claude returned invalid JSON: {e}\nRaw response: {raw}")

    score = float(data["score"])
    status_str = data.get("status", "")

    # Validate status, derive from score if unexpected
    valid_statuses = [s.value for s in LeadStatus]
    if status_str not in valid_statuses:
        if score >= 7:
            status_str = "Hot"
        elif score >= 4:
            status_str = "Warm"
        else:
            status_str = "Cold"

    return ScoreResult(
        lead_email=lead.email,
        score=score,
        status=LeadStatus(status_str),
        reason=data["reason"],
        recommended_action=data["recommended_action"],
        industry=lead.industry,
    )
