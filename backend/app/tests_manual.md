# Phase 0 - Backend Manual Tests

## Prerequisites
```bash
cd backend
pip install fastapi uvicorn sqlmodel pydantic-settings
```

## Test 1: Server Startup
**Command:**
```bash
uvicorn app.main:app --reload --port 8000
```

**Expected:**
- Server starts without errors
- Console shows "Starting Idea Tracker API..."
- Console shows "Database initialized."

---

## Test 2: Health Check Endpoint
**Command:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status": "ok"}
```

---

## Test 3: OpenAPI Docs
**URL:** http://localhost:8000/docs

**Expected:**
- Swagger UI loads
- `/health` endpoint visible under "health" tag

---

## Acceptance Criteria
- [ ] Server boots without errors
- [ ] Router registered correctly
- [ ] DB connection opens (SQLite file created)
- [ ] Health endpoint returns `{"status": "ok"}`
