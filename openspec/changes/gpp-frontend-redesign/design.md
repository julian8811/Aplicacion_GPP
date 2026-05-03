# Design: gpp-frontend-redesign

## Technical Approach

Full-stack rewrite replacing a 1571-line Streamlit monolith with a modern SPA + API architecture. The React SPA handles UI (Vercel), FastAPI serves business logic (Railway), and Supabase provides PostgreSQL + Auth + RLS. Each evaluation is stored as JSONB for PA/PO question sets, with computed percentages and action plans as separate relations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        BROWSER                                  │
│   React SPA (Vite) ──→ Zustand (UI) + React Query (server)     │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTPS (JSON REST)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FASTAPI (Railway)                          │
│   Auth middleware → Supabase JWT verification                   │
│   Endpoints: /auth/*, /api/evaluations/*, /api/results/*      │
│   Wraps pdf_generator.py → /api/pdf/{id}                       │
└──────────┬──────────────────────┬───────────────────────────────┘
           │                     │
           ▼                     ▼
┌──────────────────┐  ┌─────────────────────────────────────┐
│  SUPABASE AUTH    │  │     SUPABASE POSTGRESQL + RLS        │
│  - Email/Password│  │  Tables: profiles, evaluations,     │
│  - Google OAuth  │  │  action_plans (FK cascade)           │
│  - JWT (RS256)   │  │  RLS: user owns profile → owns rows  │
└──────────────────┘  └─────────────────────────────────────┘
```

## Frontend State Management

**Server state**: React Query (`@tanstack/react-query`) for all API calls. Cache keys by resource + ID. Optimistic updates on mutations. Automatic invalidation on create/update/delete.

**UI state**: Zustand for ephemeral state — active tab, sidebar collapse, form draft (pre-save), modal open/close, toast queue. Persisted to sessionStorage for refresh resilience.

```
useEvaluationList()  → GET /api/evaluations        (React Query)
useEvaluation(id)   → GET /api/evaluations/{id}   (React Query)
useCreateEvaluation → POST /api/evaluations       (React Query mutation)

useUIStore()         → Zustand (sidebar, modals, drafts)
```

## Auth Flow

```
1. User → /auth/signup or /auth/google → Supabase Auth
2. Supabase → returns JWT (access_token + refresh_token)
3. Frontend stores JWT in localStorage
4. Every API request → Authorization: Bearer <token>
5. FastAPI middleware verifies JWT → extracts user_id
6. RLS policies in Supabase enforce row-level ownership
```

Logout clears localStorage and calls `POST /auth/logout` to invalidate the session.

## API Contract (Key TypeScript Interfaces)

```typescript
// Shared
interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'owner' | 'viewer';
  establishment_name: string;
}

interface Evaluation {
  id: string;
  user_id: string;
  fecha: string; // ISO timestamp
  general_pct: number;
  pa_pct: number;
  po_pct: number;
  evaluaciones_pa: PAPayload;
  evaluaciones_po: POPayload;
  action_plans?: ActionPlan[];
}

interface ActionPlan {
  id: string;
  evaluation_id: string;
  element: string;
  action: string;
  responsible: string;
  due_date: string; // ISO date
  status: 'pendiente' | 'en_progreso' | 'completada';
}

interface PAPayload { [category: string]: { [questionId: string]: number } }
interface POPayload { [category: string]: { [questionId: string]: number } }

// Results
interface ResultsRequest {
  evals_pa: PAPayload;
  evals_po: POPayload;
}
interface ResultsResponse {
  general_pct: number;
  pa: number;
  po: number;
  priority: 'PA' | 'PO' | 'BALANCED';
}

// Invite
interface InviteRequest { email: string }
interface InviteResponse { message: string }
```

## Component Hierarchy

```
<AppShell>
├── <Sidebar> (desktop) / <BottomNav> (mobile)  ← Zustand-controlled
├── <DashboardPage>      ← KPIs (Recharts), recent evaluations
├── <EvaluationWizard>  ← Multi-step form: PA → PO → Results
│   ├── <SliderQuestion> (×60 questions PA, ×40 PO)
│   └── <AutoSaveIndicator>
├── <ResultsPage>        ← Radar/bar charts, percentage breakdowns
├── <ActionPlanPage>    ← CRUD table for action items
├── <HistoryPage>       ← Paginated list + trend line chart
├── <SettingsPage>      ← Profile edit, invite viewers by email
└── <AuthPage>          ← Login / Signup / Google OAuth callback
```

## Technology Choices

| Choice | Rationale |
|--------|-----------|
| React 18 + Vite | Fast HMR, native ESM, superior build times over CRA |
| TypeScript strict | Catch contract mismatches at compile time; aligns with FastAPI Pydantic |
| Tailwind + shadcn/ui | Reusable components, design-token consistency, no fighting framework styles |
| Zustand | Simpler than Redux, minimal boilerplate, persists to sessionStorage |
| React Query | Dedup, cache, optimistic updates — server state is non-trivial here |
| React Router v6 | Standard SPA routing with nested layouts |
| React Hook Form + Zod | Type-safe forms, schema-driven validation, great DX |
| Recharts | Composable SVG charts, works well with React 18 |

## Key Architectural Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Auth storage | JWT in localStorage | Cookies | Simpler CORS handling; HttpOnly cookie requires proxy; mobile web works fine |
| Server state cache | React Query | SWR, Redux RTK Query | Better devtools, optimistic updates out of box, active maintenance |
| Form persistence | Zustand draft + sessionStorage | IndexedDB, Supabase real-time | Simpler; auto-save every 30s during wizard |
| PDF generation | Wrap pdf_generator.py as API endpoint | Client-side PDF, @react-pdf | Reuse proven logic; avoid browser compatibility issues; async download |
| RLS enforcement | Supabase RLS + FastAPI pre-check | RLS only | Defense in depth; API rejects unauthorized calls before Supabase even sees them |
| Matrices data | GET /api/matrices (cached) | Embedded JSON | Changes to PA/PO questions don't require frontend deploy; React Query caches aggressively |

## Open Questions

- [ ] Will Supabase free tier connection limits cause cold-start latency on Railway? Monitor after Phase 1.
- [ ] Does Google OAuth require a custom redirect URI per Vercel preview deploy? May need wildcard.
- [ ] Is there a rate limit on invitation emails from Supabase? If so, queue via Railway background job.
