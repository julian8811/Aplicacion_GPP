# Proposal: gpp-frontend-redesign

## Intent

Replace the monolithic Streamlit app (app.py, 1571 lines) with a modern React SPA + FastAPI + Supabase architecture. The current implementation suffers from poor mobile UX, tangled logic, and JSON-file persistence that doesn't scale beyond single-user. The redesign delivers a responsive, multi-user evaluation platform with proper auth, role-based access, and maintainable architecture.

## Scope

### In Scope
- Full frontend rewrite: React 18 + Vite + TypeScript + Tailwind + shadcn/ui
- Backend API: FastAPI (Python 3.11+) on Railway
- Database: Supabase PostgreSQL with RLS policies
- Auth: Supabase email/password + Google OAuth
- Dashboard with KPIs and charts (Recharts)
- PA/PO evaluation forms with auto-save
- Results view with breakdown charts
- Recommendations engine + Action Plan builder
- Evaluation history + benchmarking
- Settings panel with user invites (owner → viewer by email)
- PDF generation (wrap existing pdf_generator.py as API endpoint)
- Responsive mobile-first layout with bottom nav on small screens
- State: Zustand + React Query

### Out of Scope
- Native mobile apps
- Offline-first / PWA
- Advanced analytics / ML-based recommendations
- White-label / multi-tenancy (beyond single establishment per account)
- Evaluation limits or paywalls (future monetization layer)

## Capabilities

### New Capabilities
- `user-auth`: Email/password + Google OAuth via Supabase Auth with RLS
- `role-invite`: Owners invite viewers by email; role-based access (owner/viewer)
- `evaluation-papo`: Full PA + PO evaluation workflow with JSONB storage
- `action-plans`: CRUD for action items linked to evaluations
- `pdf-export`: API endpoint wrapping pdf_generator.py for downloadable reports
- `benchmarking`: Historical comparison across past evaluations

### Modified Capabilities
- None (net-new capabilities — existing Streamlit app is replaced entirely)

## Approach

**Phased delivery** across 10 infrastructure + implementation phases:

| Phase | Focus | Duration |
|-------|-------|----------|
| 0 | Setup: repo, Vercel, Railway, Supabase, DB schema, auth | ~3 days |
| 1 | Backend API: all endpoints + RLS policies | 1.5 weeks |
| 2 | Frontend base: Vite + Tailwind + shadcn/ui + routing | 1 week |
| 3 | Dashboard + Layout: KPIs, nav, responsive shell | 4–5 days |
| 4 | PA/PO Forms: evaluation wizard with validation | 4–5 days |
| 5 | Results: charts (Recharts), percentage breakdowns | 4–5 days |
| 6 | Recommendations + Plan: engine + action plan CRUD | 4–5 days |
| 7 | History + Benchmarking: past evaluations, trends | 3–4 days |
| 8 | Settings + Invites: user management, role assignment | 2–3 days |
| 9 | PDF + Testing: integration tests, PDF endpoint | 3–4 days |
| 10 | Polish + Deploy: production hardening, Vercel/Railway deploy | 2–3 days |

**Total**: ~11–12 weeks

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `app.py` | Removed | Entire Streamlit app replaced |
| `pdf_generator.py` | Wrapped | Exposed as FastAPI endpoint |
| `frontend/` | New | React SPA (Vercel deploy) |
| `backend/` | New | FastAPI app (Railway deploy) |
| Supabase | New | PostgreSQL schema + Auth + RLS |
| JSON persistence | Removed | Replaced by Supabase |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Supabase cold-start / connection limits on free tier | Med | Monitor usage; upgrade to Pro if needed |
| RLS policy misconfiguration exposes data | Med | Test all role scenarios before launch; add integration tests |
| Scope creep from stakeholder feedback mid-build | High | Freezes scope at proposal; all changes go through new SDD cycle |
| Frontend-backend contract drift | Med | Shared OpenAPI schema; React Query typed hooks generated from spec |
| PDF generation regression | Low | Wrap existing proven logic; add regression test |

## Rollback Plan

If the FastAPI + Supabase stack fails unexpectedly:
1. Keep `app.py` in Git history under a `legacy/` branch
2. Re-enable Streamlit hosting (singleDyno on Railway) as fallback
3. Supabase data remains exportable as JSON/SQL dump

If a specific feature (e.g., action plans) fails:
- Feature-flag disable in React; degrade to read-only results view
- All evaluation data stays intact in Supabase

## Dependencies

- Supabase project provisioned with email + Google OAuth enabled
- Vercel account (frontend hosting)
- Railway account (backend hosting)
- Existing `pdf_generator.py` logic retained and wrapped

## Success Criteria

- [ ] Users can sign up, log in (email + Google OAuth), and receive invite emails
- [ ] Owners see full dashboard; viewers see read-only results
- [ ] Complete PA + PO evaluation flow produces a saved result with charts
- [ ] Action plans are created, assigned, and marked complete
- [ ] PDF download renders correct evaluation data
- [ ] Mobile viewport shows functional bottom-nav layout
- [ ] All Supabase RLS policies pass security audit
- [ ] Frontend builds (`npm run build`) with zero TypeScript errors
- [ ] Backend passes `pytest` with >80% coverage on core logic
- [ ] Legacy `app.py` is archived; no active Streamlit dependency