# GovAssist 🇮🇳
### Agentic Government Scheme Application System

Apply to any Indian government scheme with a single click. Our AI agent fills and submits forms automatically.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14, Tailwind CSS |
| Backend API | FastAPI, Pydantic v2 |
| Database | Supabase (PostgreSQL) |
| Storage | Supabase Storage |
| Browser Agent | Playwright (Chromium headless) |
| Primary AI | Grok 3 (via OpenRouter) |
| Vision AI | Qwen VL 72B (via OpenRouter) |
| Document Import | DigiLocker OAuth 2.0 |
| Deploy (API) | Vercel (stateless routes) + Railway (agent runner) |
| Deploy (Frontend) | Vercel |

---

## Setup

### 1. Database (Supabase)

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor** and run `scripts/migrate.sql`
3. Go to **Storage** → create two buckets:
   - `govassist-documents` (private)
   - `govassist-screenshots` (public)
4. Copy your Project URL, anon key, and service role key

### 2. API Keys

Get your API keys:
- **OpenRouter** (for Grok + Qwen): [openrouter.ai](https://openrouter.ai)
- **DigiLocker** (optional): [digilocker.gov.in/developers](https://digilocker.gov.in)

### 3. Backend Setup

```bash
cd backend
cp .env.example .env
# Fill in .env with your keys

pip install -r requirements.txt
playwright install chromium --with-deps

uvicorn app.main:app --reload --port 8000
```

### 4. Seed Schemes

```bash
cd govassist
python scripts/seed_schemes.py
```

### 5. Frontend Setup

```bash
cd frontend
cp .env.local.example .env.local
# Set NEXT_PUBLIC_API_URL=http://localhost:8000

npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

---

## Deployment

### Backend on Railway (Agent Runner — needs Playwright)

1. Push to GitHub
2. Create new Railway project → Deploy from GitHub
3. Select `backend/` as root directory — Railway uses `Dockerfile`
4. Add environment variables from `.env.example`
5. Railway URL becomes your `BACKEND_URL`

### Backend on Vercel (API-only, no agent)

```bash
cd backend
vercel deploy
# Add env vars in Vercel dashboard
```

> **Note:** Vercel cannot run the Playwright agent (60s timeout limit + no browser support).
> Use Railway for the full agent. Vercel works for auth/schemes/eligibility endpoints only.

### Frontend on Vercel

```bash
cd frontend
vercel deploy
# Set NEXT_PUBLIC_API_URL to your Railway backend URL
```

---

## How It Works

### Eligibility Engine
1. User completes profile (age, income, state, caste, occupation)
2. Uploads documents → Qwen Vision extracts all fields (name, DOB, income, etc.)
3. Grok 3 reads user profile against every scheme's eligibility criteria
4. Results cached in `user_eligibility` table, shown on dashboard

### One-Click Apply Agent
1. User clicks **Apply Now** on a scheme
2. `POST /applications/apply/{scheme_id}` creates a job, starts background task
3. Frontend opens SSE stream `/applications/jobs/{job_id}/stream`
4. Agent loop (up to 35 iterations):
   - Takes screenshot of current page
   - Grok 3 sees screenshot + page state → decides next action
   - Playwright executes: fill field / click button / select dropdown / upload file
   - After all fields filled → Qwen Vision verifies correctness
   - On success → extracts reference number, marks job complete
   - On CAPTCHA/OTP → pauses, notifies user via `needs_review` status
5. All screenshots and steps streamed live to frontend

---

## Project Structure

```
govassist/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app + CORS
│   │   ├── config.py            # Settings from env
│   │   ├── database.py          # Supabase client
│   │   ├── models/              # Pydantic models
│   │   ├── routers/             # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── documents.py
│   │   │   ├── schemes.py
│   │   │   └── applications.py  # SSE streaming
│   │   ├── services/
│   │   │   ├── eligibility.py   # Grok LLM matching
│   │   │   ├── document_parser.py  # Qwen Vision OCR
│   │   │   ├── digilocker.py    # DigiLocker OAuth
│   │   │   └── agent/
│   │   │       ├── orchestrator.py  # Main ReAct loop
│   │   │       ├── browser.py       # Playwright manager
│   │   │       ├── planner.py       # Grok action planner
│   │   │       └── verifier.py      # Qwen form verifier
│   │   └── utils/
│   ├── Dockerfile               # Playwright-capable image
│   ├── railway.toml             # Railway deployment
│   └── vercel.json              # Vercel deployment
├── frontend/
│   ├── app/
│   │   ├── (auth)/login|signup  # Auth pages
│   │   ├── onboarding/          # 3-step onboarding
│   │   ├── dashboard/           # Eligible schemes
│   │   ├── schemes/             # Browse + detail
│   │   └── applications/        # History + live view
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── SchemeCard.tsx
│   │   ├── CategoryFilter.tsx
│   │   ├── ApplyButton.tsx      # One-click apply
│   │   └── AgentLiveView.tsx    # Real-time agent UI
│   └── lib/
│       ├── api.ts               # All API calls
│       ├── auth-context.tsx     # Auth state
│       └── utils.ts
├── scripts/
│   ├── migrate.sql              # Full DB schema
│   └── seed_schemes.py          # 25 real schemes
└── docker-compose.yml           # Local dev
```

---

## Environment Variables Reference

### Backend `.env`
```
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
JWT_SECRET=
OPENROUTER_API_KEY=
GROK_MODEL=x-ai/grok-3
VISION_MODEL=qwen/qwen-vl-72b-instruct
FRONTEND_URL=http://localhost:3000
DIGILOCKER_CLIENT_ID=          # optional
DIGILOCKER_CLIENT_SECRET=      # optional
```

### Frontend `.env.local`
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
```
