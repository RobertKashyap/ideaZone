# Phase 0 - Frontend Manual Tests

## Prerequisites
```bash
cd frontend
npm install
```

## Test 1: Development Server
**Command:**
```bash
npm run dev
```

**Expected:**
- Server starts at http://localhost:5173
- No compilation errors

---

## Test 2: Dashboard Page
**URL:** http://localhost:5173

**Expected:**
- "💡 Idea Tracker" heading visible
- Quick Capture section with Record button
- Recent Ideas placeholder
- Transcription Preview section

---

## Test 3: Idea Workspace Page
**URL:** http://localhost:5173/idea/test-123

**Expected:**
- Back to Dashboard link
- ID badge shows "test-123"
- Audio recording section
- Transcript editor section
- Research report placeholder

---

## Test 4: PWA Manifest
**Check:** DevTools → Application → Manifest

**Expected:**
- Name: "Idea Tracker"
- Display: "standalone"
- Theme color visible

---

## Test 5: Service Worker
**Check:** DevTools → Console

**Expected:**
- "Service Worker registered" message appears
- DevTools → Application → Service Workers shows active worker

---

## Acceptance Criteria
- [ ] Frontend runs locally without errors
- [ ] Dashboard and IdeaWorkspace pages render
- [ ] Placeholders show endpoints they will call
- [ ] PWA manifest loads correctly
- [ ] Service worker registers successfully
