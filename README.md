# ⚡ LeadWise Core

> AI-powered lead qualification engine. Industry-agnostic. Built by a BA who documented every requirement behind it.

## 🏗️ Project Structure

```
leadwise-core/
├── backend/
│   ├── config.py         # Industry toggle (banking / travel)
│   ├── models.py         # Pydantic data models
│   ├── scoring_agent.py  # Claude API scoring logic
│   └── main.py           # FastAPI endpoints
├── frontend/
│   └── app.py            # Streamlit UI
├── data/
│   ├── leads_banking.json  # Demo leads — banking
│   └── leads_travel.json   # Demo leads — travel
├── tests/
│   └── test_scoring.py
├── requirements.txt
├── render.yaml           # Render deployment config
└── .env.example
```

## 🚀 Run locally

```bash
# 1. Clone and install
git clone https://github.com/your-username/leadwise-core
cd leadwise-core
pip install -r requirements.txt

# 2. Set your API key
cp .env.example .env
# Edit .env: add your ANTHROPIC_API_KEY and set INDUSTRY=banking or travel

# 3. Start the backend
uvicorn backend.main:app --reload

# 4. Start the frontend (new terminal)
streamlit run frontend/app.py
```

## 🌍 Industries supported

| Industry | Company | Product | Conv. Target |
|----------|---------|---------|--------------|
| 🏦 Banking | BankWise Retail | Livret A Boosté | 15% |
| 🌍 Travel | LinguaWise International | Séjour Linguistique Été | 18% |

## 🛠️ Tech Stack

- **AI**: Claude API (Anthropic) — `claude-sonnet-4-20250514`
- **Backend**: Python / FastAPI
- **Frontend**: Streamlit
- **Deploy**: Render

## 📋 BA Documentation

Full requirements, user stories, GDPR analysis and test strategy available on Notion.

---
Built by **Zahra** · BA Portfolio Project · 2025
