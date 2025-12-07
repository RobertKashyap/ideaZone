# Idea Tracker 2.0

A full-stack idea tracking application with a React/TypeScript frontend and FastAPI backend.

## Prerequisites

- **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.10 or higher) - [Download](https://python.org/)
- **npm** (comes with Node.js)

## Project Structure

```
idea-tracker-2.0/
├── frontend/          # React + TypeScript + Vite PWA
├── backend/           # FastAPI Python backend
└── README.md
```

---

## Getting Started

### 1. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 2. Backend Setup

Navigate to the backend directory and create a virtual environment:

```bash
cd backend
python3 -m venv venv
```

Activate the virtual environment:

- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Start the backend server:

```bash
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

---

## Regenerating Ignored Files

The following files are generated at runtime and excluded from version control:

| File/Directory | How to Regenerate |
|----------------|-------------------|
| `frontend/node_modules/` | Run `npm install` in `/frontend` |
| `backend/venv/` | Run `python3 -m venv venv` in `/backend` |
| `backend/__pycache__/` | Auto-generated when Python runs |
| `backend/*.db` | Auto-created on first backend startup |

---

## API Documentation

Once the backend is running, API docs are available at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## Development

### Frontend Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
```

### Backend Commands

```bash
uvicorn app.main:app --reload  # Start with auto-reload
uvicorn app.main:app           # Start without auto-reload
```

---

## License

MIT
