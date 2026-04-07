# AI Study Assistant

A multi-user AI-powered study assistant built with Flask. Upload PDFs, paste YouTube links, or type questions — and get context-aware responses powered by Groq. Each user gets isolated sessions with persistent chat history backed by PostgreSQL and a two-layer Redis caching architecture.

---

## Features

- **Multi-user authentication** — JWT-based auth with secure cookie handling and CSRF protection
- **Session management** — create, switch between, and persist multiple named chat sessions per user
- **Context-aware responses** — last 10 messages of each session are held in Redis for fast, stateful conversation
- **PDF support** — upload PDFs and ask questions about their content
- **YouTube support** — paste a YouTube URL and get a transcript-based AI response
- **Two-layer Redis caching**
  - *Stateless cache*: SHA-256 keyed prompt → response cache for repeated factual questions
  - *Stateful detection*: follow-up prompts ("explain that", "give me an example") are never cached
  - *Session cache*: per-session message history stored as Redis lists, rebuilt from PostgreSQL on cache miss
- **Token revocation** — logout invalidates the JWT via a Redis blocklist (TTL-matched to token expiry)
- **Blueprint architecture** — modular route structure with an app factory pattern

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | PostgreSQL + Flask-SQLAlchemy + Flask-Migrate |
| Cache | Redis |
| Auth | Flask-JWT-Extended |
| LLM | Groq API |
| PDF Parsing | PyMuPDF (fitz) |
| YouTube | youtube-transcript-api |
| Server | Gunicorn |
| Containerization | Docker + Docker Compose |

---

## Project Structure

```
app/
├── __init__.py              # App factory
├── extensions.py            # db, redis, jwt init
├── models/
│   ├── user.py
│   ├── sessions.py
│   ├── messages.py
│   └── token_blocklist.py
├── routes/
│   ├── auth.py              # Register, login, logout
│   ├── prompt.py            # Core LLM interaction
│   ├── session_extractor.py # Session listing/switching
│   └── uploads.py           # PDF upload handling
└── services/
    ├── llm_services/        # Groq provider
    ├── llm_cache_services/  # Stateless text + PDF cache
    ├── session_cache_services/ # Per-session Redis history
    ├── session_services/    # Session creation
    ├── message_services/    # DB read/write for messages
    ├── pdf_services/        # PDF text extraction
    └── yt_services/         # YouTube transcript fetching
```

---

## Getting Started

### Prerequisites

- Docker and Docker Compose
- A [Groq API key](https://console.groq.com)

### Setup

**1. Clone the repo**
```bash
git clone https://github.com/jayssSmm/StudyMindAI.git
cd StudyMindAI
```

**2. Create a `.env` file**
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
GROQ_API_KEY=your-groq-api-key

DATABASE_URL=postgresql://postgres:password@db:5432/studydb
REDIS_URL=redis://redis:6379/0
```

**3. Start the containers**
```bash
docker compose up --build
```

**4. Run database migrations**
```bash
docker compose exec web flask db upgrade
```

The app will be available at `http://localhost:5000`.

---

## How It Works

### Request Flow

```
User sends prompt
       │
       ▼
Is it stateful? (e.g. "explain that") ──► Yes ──► Skip cache, go to LLM
       │ No
       ▼
Cache hit in Redis? ──► Yes ──► Return cached response
       │ No
       ▼
Is it a YouTube URL? ──► Yes ──► Fetch transcript ──► LLM
       │ No
       ▼
Fetch last 10 messages from Redis (or rebuild from PostgreSQL)
       │
       ▼
Send prompt + history to Groq
       │
       ▼
Store response in Redis cache + session history + PostgreSQL
```

### Stateful Detection

Prompts like *"give me an example"*, *"explain that"*, *"continue"*, or *"as you mentioned above"* are detected as context-dependent via regex pattern matching and are never cached — they always go through the full LLM pipeline with session history attached.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Create a new user account |
| POST | `/auth/login` | Login, returns JWT cookie |
| POST | `/auth/logout` | Invalidates token via Redis blocklist |
| POST | `/prompt` | Send a prompt, get an AI response |
| GET | `/sessions` | List all sessions for current user |
| POST | `/uploads/pdf` | Upload a PDF for context |

All protected routes require a valid JWT cookie.

---

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask secret key |
| `JWT_SECRET_KEY` | JWT signing key |
| `GROQ_API_KEY` | Groq API key |
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string |

---