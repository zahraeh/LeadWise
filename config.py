"""
config.py — LeadWise Core
Industry configuration switcher.
Set INDUSTRY env var to 'banking' or 'travel' to change mode.
"""

import os
from dotenv import load_dotenv

load_dotenv()

INDUSTRY = os.getenv("INDUSTRY", "banking").lower()

CONFIGS = {
    "banking": {
        "name": "LeadWise Banking",
        "emoji": "🏦",
        "company": "BankWise Retail",
        "product": "Livret A Boosté",
        "target": "25–45 ans, digital-first",
        "channels": ["Email", "SMS", "Push Notification", "Conseiller"],
        "kpis": {
            "conversion_target": 0.15,
            "optin_target": 0.60,
            "callback_sla_hours": 24,
        },
        "lead_fields": [
            {"key": "age", "label": "Âge", "type": "number"},
            {"key": "income_bracket", "label": "Tranche de revenus", "type": "select",
             "options": ["< 20k€", "20–40k€", "40–60k€", "> 60k€"]},
            {"key": "product_interest", "label": "Produit d'intérêt", "type": "select",
             "options": ["Livret A", "PEL", "Assurance-vie", "Compte courant"]},
            {"key": "channel", "label": "Canal d'entrée", "type": "select",
             "options": ["Email", "SMS", "Push", "Conseiller"]},
            {"key": "digital_score", "label": "Score digital (1–5)", "type": "number"},
        ],
        "scoring_context": (
            "You are a lead scoring agent for BankWise Retail, a French retail bank. "
            "Evaluate banking leads for the 'Livret A Boosté' campaign targeting digital-first "
            "customers aged 25–45. Score the lead from 0 to 10 based on: age fit, income level, "
            "product interest alignment, channel preference, and digital engagement score. "
            "A score of 0–3 = Cold, 4–6 = Warm, 7–10 = Hot."
        ),
    },
    "travel": {
        "name": "LeadWise Travel",
        "emoji": "🌍",
        "company": "LinguaWise International",
        "product": "Séjour Linguistique Été",
        "target": "18–35 ans & professionnels",
        "channels": ["Google Ads", "Email", "Comparateurs", "Réseaux sociaux"],
        "kpis": {
            "conversion_target": 0.18,
            "optin_target": 0.65,
            "callback_sla_hours": 24,
        },
        "lead_fields": [
            {"key": "age", "label": "Âge", "type": "number"},
            {"key": "destination", "label": "Destination souhaitée", "type": "select",
             "options": ["Londres", "Dublin", "New York", "Malte", "Toronto"]},
            {"key": "budget", "label": "Budget estimé", "type": "select",
             "options": ["< 1000€", "1000–2000€", "2000–4000€", "> 4000€"]},
            {"key": "duration_weeks", "label": "Durée souhaitée (semaines)", "type": "number"},
            {"key": "departure_urgency", "label": "Urgence départ", "type": "select",
             "options": ["< 1 mois", "1–3 mois", "3–6 mois", "> 6 mois"]},
        ],
        "scoring_context": (
            "You are a lead scoring agent for LinguaWise International, a language travel agency. "
            "Evaluate leads for the 'Séjour Linguistique Été' campaign targeting young adults 18–35 "
            "and professionals. Score the lead from 0 to 10 based on: age fit, destination appeal, "
            "budget level, trip duration, and departure urgency. "
            "A score of 0–3 = Cold, 4–6 = Warm, 7–10 = Hot."
        ),
    },
}


def get_config() -> dict:
    """Return the active industry configuration."""
    if INDUSTRY not in CONFIGS:
        raise ValueError(f"Unknown industry: '{INDUSTRY}'. Choose 'banking' or 'travel'.")
    return CONFIGS[INDUSTRY]
