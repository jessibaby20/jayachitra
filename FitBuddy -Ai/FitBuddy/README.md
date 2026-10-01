# FitBuddy – AI Fitness Plan Generator

FastAPI + Jinja2 + SQLite + Gemini application based on the supplied FitBuddy documentation.

## Quick start

Windows:
```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Edit `.env` and set `GOOGLE_API_KEY`. The model is configurable with `GEMINI_MODEL`.
The source document names Gemini 1.5 Pro/Flash; this implementation uses a configurable current Gemini model instead of hard-coding historical model names.

Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/view-all-users

If no API key is configured, the app uses a small local fallback so the UI and tests remain runnable.

## API
- GET `/api/health`
- POST `/api/users`
- POST `/api/generate-workout`
- POST `/api/feedback`
- GET `/api/users`
- GET `/api/users/{user_id}`

Run tests:
```bash
pytest -q
```

This is general wellness software, not medical care. AI output should be reviewed appropriately and users should stop activity that causes pain or concerning symptoms.
