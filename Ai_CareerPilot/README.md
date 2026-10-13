# AI CareerPilot — Your Personal AI Career Agent

**Analyze. Learn. Grow.** A purple-themed Flask portfolio website for resume-to-role skill matching, career roadmaps, interview practice, learning bookmarks, and admin insights.

## What works locally
- Email/username registration and login, hashed passwords, CSRF protection, user profiles, password change, account deletion.
- Default development administrator seeded once (change credentials before any shared/public deployment).
- PDF/DOCX resume extraction, configurable skill dictionary, transparent skill coverage calculation, database-backed analysis history, ownership-protected results and PDF exports.
- Starter roadmap tasks and progress tracking; local interview question fallback; reputable learning links and database bookmarks.
- Admin dashboard, user activation/deactivation, analysis metadata, role analytics, configuration status, and audit logs.
- Optional Google and GitHub OAuth via Authlib; optional OpenAI-compatible chat-completions endpoint.
- Responsive desktop/mobile website UI.

## Requirements
Python 3.10–3.12 recommended. Use a fresh virtual environment. Internet is required to download dependencies and to load Bootstrap/Chart.js/Bootstrap Icons from CDNs in the UI.

## Windows PowerShell setup
```powershell
cd path\to\ai-careerpilot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```
If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal and activate again, or use `.venv\Scripts\python.exe` explicitly.

Open `.env` and replace `SECRET_KEY` with a long random value. Defaults are for local development only. The development admin defaults are username `Mantasha`, password `Mantasha`; sign in and change it before sharing the application. If the account already exists, changing `ADMIN_PASSWORD` does not overwrite the existing hash.

Initialize database and run:
```powershell
python scripts/init_db.py
python app.py
```
Open **http://127.0.0.1:5000**. SQLite is created under `instance/` by default. Resume files are stored temporarily outside `static/` and removed after processing. Maximum upload size is 5 MB.

## AI provider (optional)
Without credentials, resume matching, roadmap, PDF reports, and interview questions work using the local skill dictionary/question bank. To use an OpenAI-compatible API, set `AI_PROVIDER=openai-compatible`, `AI_API_KEY`, `AI_BASE_URL` (base URL ending before `/chat/completions`), and `AI_MODEL`. The optional provider is used for interview questions; failures fall back locally and are labeled. Do not commit `.env`.

## Google OAuth (optional)
1. Create an OAuth client in Google Cloud Console and configure the consent screen.
2. For local development add `http://127.0.0.1:5000/auth/google/callback` as an authorized redirect URI.
3. Put the client ID and secret in `.env` as `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`.
4. Restart Flask. The login page's Google button uses the real OAuth flow only when credentials exist.

## GitHub OAuth (optional)
1. Create a GitHub OAuth App in Developer settings.
2. Set callback URL to `http://127.0.0.1:5000/auth/github/callback`.
3. Put client ID and secret in `.env` as `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`; restart Flask. GitHub must provide a verified email for account creation.

## Tests
```powershell
python -m pytest -q
```
The tests use a separate temporary SQLite database.

## Folder structure
```text
ai-careerpilot/
  app.py config.py extensions.py requirements.txt .env.example README.md
  models/ routes/ services/
  templates/ static/
  scripts/init_db.py tests/ instance/
```

## Security and production notes
- This is a portfolio/demo starter, not a security-audited production service. Set a strong `SECRET_KEY`, change the default admin password, set `FLASK_ENV=production`, serve behind HTTPS, configure secure cookies at the deployment layer, add rate limiting and monitoring, and review privacy/legal copy before public deployment.
- OAuth and AI provider integrations require your own credentials; none are included. OAuth failures are not simulated as successful logins.
- The skill dictionary is intentionally explainable but limited; it can miss synonyms and does not judge resume quality or predict hiring outcomes. Scanned PDFs without embedded text may not parse.
- Admin analytics are derived from actual stored records. User-facing resume content is not shown in the admin tables.
- External CSS/JS uses public CDNs; replace with pinned local assets if you need offline operation.
- Account deletion and database cascades should be reviewed for the exact deployment database before production.

## Portfolio description
Built AI CareerPilot, a responsive Flask-based career assistant featuring secure authentication, PDF/DOCX resume parsing, explainable skill-gap matching, personalized roadmap tracking, interview practice, learning bookmarks, PDF reports, OAuth-ready sign-in, and a role-protected admin dashboard.
