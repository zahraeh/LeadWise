"""
scoring_agent.py — LeadWise Core
AI scoring agent powered by Claude API (Anthropic).
Takes a lead dict, returns a ScoreResult.
"""

import os
import json
import anthropic
from backend.models import Lead, ScoreResult, LeadStatus
from backend.config import CONFIGS


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
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()

    # Clean potential markdown fences
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    data = json.loads(raw)

    score = float(data["score"])
    status_str = data["status"]

    # Validate status
    if status_str not in [s.value for s in LeadStatus]:
        # Derive from score if model returned something unexpected
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
