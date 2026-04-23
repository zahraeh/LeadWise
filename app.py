"""
app.py — LeadWise Core
Streamlit frontend: industry toggle, lead submission form, real-time AI scoring.
"""

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="LeadWise Core",
    page_icon="⚡",
    layout="centered",
)

# ── Industry toggle ───────────────────────────────────────────
st.sidebar.title("⚡ LeadWise Core")
industry = st.sidebar.radio(
    "Choisir l'industrie",
    options=["banking", "travel"],
    format_func=lambda x: "🏦 Banking" if x == "banking" else "🌍 Travel",
)

# Fetch config from backend
try:
    config_res = requests.get(f"{API_URL}/config", params={"industry": industry}, timeout=5)
    config = config_res.json()
except Exception:
    st.error("❌ Impossible de contacter le backend. Vérifiez que FastAPI tourne sur le port 8000.")
    st.stop()

# ── Header ────────────────────────────────────────────────────
st.title(f"{config['emoji']} {config['name']}")
st.caption(f"**{config['company']}** · Produit : {config['product']} · Cible : {config['target']}")
st.divider()

# ── Lead submission form ──────────────────────────────────────
st.subheader("📋 Nouveau Lead")

with st.form("lead_form"):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("Prénom *", placeholder="ex: Sarah")
    with col2:
        last_name = st.text_input("Nom *", placeholder="ex: Morel")

    email = st.text_input("Email *", placeholder="sarah.morel@email.com")
    phone = st.text_input("Téléphone", placeholder="+33 6 12 34 56 78")
    opt_in = st.checkbox("✅ Consentement RGPD — Le prospect accepte d'être contacté")

    st.markdown("---")
    st.markdown("**Informations métier**")

    dynamic_fields = {}
    for field in config["lead_fields"]:
        if field["type"] == "number":
            val = st.number_input(
                field["label"],
                min_value=field.get("min", 0),
                max_value=field.get("max", None),
                value=field.get("default", 1),
            )
            dynamic_fields[field["key"]] = val
        elif field["type"] == "select":
            val = st.selectbox(field["label"], options=field["options"])
            dynamic_fields[field["key"]] = val

    submitted = st.form_submit_button("🔍 Scorer ce lead", use_container_width=True)

# ── Scoring result ────────────────────────────────────────────
if submitted:
    if not first_name or not last_name or not email:
        st.warning("Veuillez remplir tous les champs obligatoires (*)")
    else:
        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "opt_in": opt_in,
            "industry": industry,
            "fields": dynamic_fields,
        }

        with st.spinner("🤖 Analyse IA en cours..."):
            try:
                res = requests.post(f"{API_URL}/score", json=payload, timeout=30)
                result = res.json()
            except Exception as e:
                st.error(f"Erreur de connexion au backend : {e}")
                st.stop()

        # Display result
        status = result.get("status", "Cold")
        score = result.get("score", 0)
        reason = result.get("reason", "")
        action = result.get("recommended_action", "")

        color_map = {"Hot": "🔴", "Warm": "🟡", "Cold": "🔵"}
        bg_map = {"Hot": "#ffe5e5", "Warm": "#fff8e1", "Cold": "#e8f0fe"}
        emoji = color_map.get(status, "⚪")

        st.divider()
        st.subheader("📊 Résultat du Scoring IA")

        col1, col2, col3 = st.columns(3)
        col1.metric("Score", f"{score}/10")
        col2.metric("Statut", f"{emoji} {status}")
        col3.metric("SLA Rappel", f"< {config['kpis']['callback_sla_hours']}h")

        st.info(f"**💡 Analyse :** {reason}")
        st.success(f"**✅ Action recommandée :** {action}")

        if not opt_in:
            st.warning("⚠️ Ce lead n'a pas donné son consentement RGPD. Score bloqué à 0.")

# ── Footer ────────────────────────────────────────────────────
st.divider()
st.caption("LeadWise Core · Built by Zahra · Powered by Claude API (Anthropic) · Portfolio BA 2025")
