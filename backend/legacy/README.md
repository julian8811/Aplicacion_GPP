# Legacy Code

This folder contains the original Streamlit application (`app_streamlit.py`) that was the predecessor to the current React/FastAPI architecture.

## Files

- `app_streamlit.py` - Original Streamlit app (moved from project root on 2026-05-01)

## Background

The original GPP application was a monolithic Streamlit app that handled:
- User authentication
- Evaluation forms (PA/PO matrices)
- Results calculation and visualization
- PDF generation
- Recommendations engine

This was migrated to a modern SPA architecture:
- **Frontend**: React 18 + Vite + TypeScript + TailwindCSS
- **Backend**: FastAPI + Python
- **Database**: Supabase (PostgreSQL + Auth + RLS)

## Archival Date

Archived: 2026-05-01 as part of gpp-frontend-redesign change (Phase 10.5)