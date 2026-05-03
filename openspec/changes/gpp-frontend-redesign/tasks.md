# Tasks: gpp-frontend-redesign

## 0. Setup

### 0.1 Create GitHub repository
- **Deliverable**: Repo created with `frontend/` and `backend/` directory structure
- **Dependencies**: None
- **Testing**: Clone and verify directory layout
- **[x] Complete

### 0.2 Provision Supabase project
- **Deliverable**: Supabase project with PostgreSQL + Auth enabled
- **Dependencies**: Supabase account
- **Testing**: Can access Supabase dashboard

### 0.3 Configure Google OAuth
- **Deliverable**: Google Cloud project with OAuth credentials (client_id, client_secret)
- **Dependencies**: Google Cloud account
- **Testing**: Test OAuth flow in Supabase dashboard

### 0.4 Create DB schema (profiles, evaluations, action_plans)
- **Deliverable**: Tables created with proper types, constraints, and indexes
- **Dependencies**: 0.2
- **Testing**: Can insert and query from Supabase SQL editor

### 0.5 Configure RLS policies
- **Deliverable**: RLS policies on all tables; users only see their own data
- **Dependencies**: 0.4
- **Testing**: Create two users; verify user A cannot see user B's data

### 0.6 Set up Vercel project (frontend)
- **Deliverable**: Vercel app connected to GitHub repo, `frontend/` as root
- **Dependencies**: GitHub repo (0.1)
- **Testing**: Vercel deploys `main` branch

### 0.7 Set up Railway project (backend)
- **Deliverable**: Railway app connected to GitHub repo, `backend/` as root
- **Dependencies**: GitHub repo (0.1)
- **Testing**: Railway shows healthy deploy

### 0.8 Create environment template
- **Deliverable**: `.env.example` files in `frontend/` and `backend/` with all required vars
- **Dependencies**: Supabase (0.2), Vercel (0.6), Railway (0.7)
- **Testing**: Team members can copy and fill in values
- **[x] Complete

---

## 1. Backend API

### 1.1 Initialize FastAPI project
- **Deliverable**: `backend/` with FastAPI, uvicorn, requirements.txt
- **Dependencies**: 0.1
- **Testing**: `uvicorn main:app --reload` starts server
- **[x] Complete

### 1.2 Configure Supabase client
- **Deliverable**: `supabase_client.py` with async client for Supabase
- **Dependencies**: 0.2, 1.1
- **Testing**: Can query Supabase from FastAPI endpoint
- **[x] Complete

### 1.3 Implement auth endpoints (signup, login, logout, me)
- **Deliverable**: `/auth/*` routes using Supabase Auth
- **Dependencies**: 1.2
- **Testing**: `POST /auth/signup`, `POST /auth/login`, `GET /auth/me` work correctly
- **[x] Complete

### 1.4 Implement Google OAuth endpoints
- **Deliverable**: `/auth/google` initiating OAuth flow, callback handler
- **Dependencies**: 1.3, 0.3
- **Testing**: Can sign in with Google, JWT returned
- **[x] Complete

### 1.5 Implement profiles endpoint (create/update profile)
- **Deliverable**: `/api/profiles/me` GET/PUT
- **Dependencies**: 1.3, 0.4
- **Testing**: Owner can set establishment_name on first login
- **[x] Complete

### 1.6 Implement matrices endpoint
- **Deliverable**: `GET /api/matrices` returning PA and PO question structure
- **Dependencies**: 1.1
- **Testing**: Returns valid JSON matching app.py MATRIZ_PA and MATRIZ_PO
- **[x] Complete

### 1.7 Migrate `calcular_resultados()` to FastAPI
- **Deliverable**: `POST /api/results/calculate` matching current calculation logic
- **Dependencies**: 1.1, source MATRIZ_PA/PO from app.py
- **Testing**: Compare output with Streamlit app for same input ratings

### 1.8 Implement evaluations CRUD
- **Deliverable**: Full CRUD on `/api/evaluations`
- **Dependencies**: 1.2, 0.4
- **Testing**: Create, read, update, delete evaluation; RLS enforced

### 1.9 Implement action_plans CRUD
- **Deliverable**: Full CRUD on `/api/action-plans`
- **Dependencies**: 1.2, 0.4, 1.8
- **Testing**: Create action plan linked to evaluation; cascade delete works

### 1.10 Wrap pdf_generator.py as API
- **Deliverable**: `GET /api/pdf/{evaluation_id}` returning PDF bytes
- **Dependencies**: 1.8, pdf_generator.py available
- **Testing**: Download PDF, open in reader, verify data matches evaluation

### 1.11 Implement invite flow
- **Deliverable**: `POST /api/invites` sends email; `GET /api/invites?token=X` validates; `PUT /api/invites/accept` creates viewer
- **Dependencies**: 1.3, 0.4
- **Testing**: Owner sends invite → viewer clicks link → viewer account created with role=viewer

### 1.12 Add CORS and middleware
- **Deliverable**: CORS configured for Vercel frontend domain
- **Dependencies**: 0.6, 1.1
- **Testing**: Frontend on Vercel can call backend API without CORS errors
- **[x] Complete

### 1.13 Write backend unit tests
- **Deliverable**: pytest suite covering calcular_resultados, auth, CRUD operations
- **Dependencies**: 1.7, 1.8, 1.9
- **Testing**: `pytest --cov` passes with >80% coverage

---

## 2. Frontend Base

### 2.1 Initialize Vite + React + TypeScript project
- **Deliverable**: `frontend/` with Vite, React 18, TypeScript strict mode
- **Dependencies**: 0.1
- **Testing**: `npm run dev` starts; `npm run build` succeeds with zero TS errors
- **[x] Complete

### 2.2 Configure Tailwind CSS + shadcn/ui
- **Deliverable**: Tailwind configured; shadcn/ui components available
- **Dependencies**: 2.1
- **Testing**: Can use shadcn Button, Card, Input components
- **[x] Complete

### 2.3 Set up React Router v6
- **Deliverable**: Router with routes for /login, /dashboard, /evaluate, /results, /settings, etc.
- **Dependencies**: 2.1
- **Testing**: Navigating to routes renders correct components
- **[x] Complete

### 2.4 Configure React Query + Axios
- **Deliverable**: API client with Authorization header; React Query provider wrap
- **Dependencies**: 2.1
- **Testing**: API calls include JWT; React Query devtools visible in development
- **[x] Complete

### 2.5 Set up Zustand store
- **Deliverable**: `useUIStore` for sidebar, modals, drafts; `useAuthStore` for user state
- **Dependencies**: 2.1
- **Testing**: Store persists to sessionStorage on refresh; state restored correctly
- **[x] Complete

### 2.6 Build AuthPage component
- **Deliverable**: Login/Signup form with email/password + Google OAuth button
- **Dependencies**: 2.2, 2.3, 2.4, 1.4
- **Testing**: Can sign up, log in, log out; protected routes redirect to /login
- **[x] Complete

### 2.7 Build AppShell (sidebar + bottom nav responsive)
- **Deliverable**: Layout shell with collapsible sidebar (desktop) / bottom nav (mobile)
- **Dependencies**: 2.2, 2.3
- **Testing**: View at 1024px+ shows sidebar; view at 768px shows bottom nav
- **[x] Complete

### 2.8 Create design tokens (colors, typography, spacing)
- **Deliverable**: Tailwind config with design tokens matching design.md (primary, bg, surface, etc.)
- **Dependencies**: 2.2
- **Testing**: Visual consistency matches Linear/Stripe aesthetic spec
- **[x] Complete

---

## 3. Dashboard + Layout

### 3.1 Build DashboardPage with KPIs
- **Deliverable**: Dashboard showing health index gauge, recent evaluations, quick actions
- **Dependencies**: 2.7, 2.4, 1.8
- **Testing**: Dashboard shows user's latest evaluation; KPIs calculated correctly
- **[x] Complete

### 3.2 Build OnboardingPage (first-time owner setup)
- **Deliverable**: Single-step form for establishment name
- **Dependencies**: 2.6, 1.5, 2.8
- **Testing**: New owner sees onboarding; after submit, redirected to dashboard
- **[x] Complete

### 3.3 Build NewEvaluationPage (type selector)
- **Deliverable**: Page to create new evaluation: choose PA only, PO only, or both
- **Dependencies**: 2.7, 2.4, 1.8
- **Testing**: Can start new PA evaluation; evaluation appears in list
- **[x] Complete

### 3.4 Add loading states + skeleton UI
- **Deliverable**: Loading skeletons for all data-dependent views
- **Dependencies**: 2.2, 3.1
- **Testing**: Page shows skeleton while fetching data; content appears when ready
- **[x] Complete

### 3.5 Add toast notifications
- **Deliverable**: Success/error toasts using shadcn/ui toast
- **Dependencies**: 2.2
- **Testing**: Create evaluation → success toast; API error → error toast with message
- **[x] Complete

---

## 4. Formularios PA/PO

### 4.1 Build SliderQuestion component
- **Deliverable**: Reusable slider input (0-5 scale) with question text + context
- **Dependencies**: 2.2, 2.8
- **Testing**: Slider at 0-5; value changes on drag; shows current value
- **[x] Complete

### 4.2 Fetch and display PA matrix questions
- **Deliverable**: `GET /api/matrices` → render all PA questions grouped by aspect
- **Dependencies**: 4.1, 2.4, 1.6
- **Testing**: All PA questions render; grouped under Planeación, Organización, Dirección, Control
- **[x] Complete

### 4.3 Fetch and display PO matrix questions
- **Deliverable**: `GET /api/matrices` → render all PO questions grouped by aspect
- **Dependencies**: 4.1, 2.4, 1.6
- **Testing**: All PO questions render; grouped under Logística Compras, Producción, Logística Externa
- **[x] Complete

### 4.4 Implement form auto-save (every 30s)
- **Deliverable**: Draft saved to sessionStorage + React Query cache; "Draft saved" indicator
- **Dependencies**: 2.5, 4.2
- **Testing**: Fill form, wait 30s, refresh page, draft restored
- **[x] Complete

### 4.5 Implement evaluation wizard (PA → PO → submit)
- **Deliverable**: Multi-step flow: PA section, then PO section, then submit to calculate results
- **Dependencies**: 4.2, 4.3, 4.4, 1.7
- **Testing**: Complete PA, continue to PO, submit → redirected to results with saved evaluation
- **[x] Complete

### 4.6 Add progress indicator to wizard
- **Deliverable**: Step indicator showing current step (PA / PO / Results)
- **Dependencies**: 4.5
- **Testing**: Progress bar updates as user completes steps
- **[x] Complete

---

## 5. Resultados + Charts

### 5.1 Build ResultsPage with gauge chart (health index)
- **Deliverable**: Circular gauge showing general_pct (0-100) with color gradient
- **Dependencies**: 2.2, 2.4, 1.8
- **Testing**: Gauge renders with correct percentage; color matches (red <60, yellow 60-74, green ≥75)
- **[x] Complete

### 5.2 Build bar chart for PA aspects
- **Deliverable**: Horizontal bar chart for Planeacion, Organizacion, Direccion, Control percentages
- **Dependencies**: 5.1
- **Testing**: Bars render with correct percentages; labels and values visible
- **[x] Complete

### 5.3 Build bar chart for PO aspects
- **Deliverable**: Horizontal bar chart for Logistica Compras, Produccion, Logistica Externa percentages
- **Dependencies**: 5.2
- **Testing**: Bars render with correct percentages
- **[x] Complete

### 5.4 Build detail table (all questions with scores)
- **Deliverable**: Table showing each question, aspect, and score (0-5 → percentage)
- **Dependencies**: 5.1
- **Testing**: All questions appear with correct score; sortable by aspect
- **[x] Complete

### 5.5 Add "Save as PDF" button
- **Deliverable**: Button triggering `GET /api/pdf/{id}` download
- **Dependencies**: 1.10, 2.2
- **Testing**: Click → PDF downloads and opens with correct data
- **[x] Complete

### 5.6 Add "View Action Plan" link
- **Deliverable**: CTA linking to action plan page for this evaluation
- **Dependencies**: 5.1, 6.1
- **Testing**: Link navigates to action plan page filtered by evaluation
- **[x] Complete

---

## 6. Recomendaciones + Plan

### 6.1 Build RecommendationsPage
- **Deliverable**: Cards showing recommendations filtered by ALTA/MEDIA priority
- **Dependencies**: 2.2, 2.4, 1.7, recomendaciones.py logic
- **Testing**: Recommendations match the recommendations.py matrix for user's scores
- **[x] Complete

### 6.2 Build ActionPlanPage with CRUD table
- **Deliverable**: Table with inline edit: element, action, responsible, due_date, status
- **Dependencies**: 2.2, 2.4, 1.9
- **Testing**: Can create, edit, delete action plans; changes persist on refresh
- **[x] Complete

### 6.3 Add status update (pendiente → en_progreso → completada)
- **Deliverable**: Status dropdown with visual badges (red/yellow/green)
- **Dependencies**: 6.2
- **Testing**: Change status → visual update immediately, API called
- **[x] Complete

### 6.4 Add "Create from Recommendation" button
- **Deliverable**: One-click create action plan from recommendation card
- **Dependencies**: 6.1, 6.2
- **Testing**: Click on recommendation → action plan created with pre-filled element and action text
- **[x] Complete

---

## 7. Historial + Benchmarking

### 7.1 Build HistoryPage with evaluation list
- **Deliverable**: Paginated list of past evaluations with date, name, general_pct
- **Dependencies**: 2.2, 2.4, 1.8
- **Testing**: All user's evaluations listed; sorted by date descending
- **[x] Complete

### 7.2 Add search and filter to HistoryPage
- **Deliverable**: Search by establishment name; filter by date range
- **Dependencies**: 7.1
- **Testing**: Search narrows results; filters apply correctly
- **[x] Complete

### 7.3 Add CSV export to HistoryPage
- **Deliverable**: "Export CSV" button downloading evaluation data
- **Dependencies**: 7.1
- **Testing**: CSV opens in Excel with correct columns and data
- **[x] Complete

### 7.4 Build BenchmarkingPage (historical comparison)
- **Deliverable**: Line chart showing evaluation trend over time (general_pct by date)
- **Dependencies**: 2.2, 2.4, 7.1
- **Testing**: Chart shows correct trend; can compare PA vs PO over time
- **[x] Complete

### 7.5 Add benchmarking annotation (milestones)
- **Deliverable**: Mark key dates (e.g., "After implementing plan") on trend chart
- **Dependencies**: 7.4
- **Testing**: Annotations appear on chart at correct dates
- **[x] Complete

---

## 8. Settings + Invites

### 8.1 Build SettingsPage with profile edit
- **Deliverable**: Form to edit full_name, establishment_name
- **Dependencies**: 2.2, 2.4, 1.5
- **Testing**: Edit and save → changes reflected in Supabase and UI
- **[x] Complete

### 8.2 Add invite viewer flow
- **Deliverable**: Input email + "Send Invite" button; list of pending/invited viewers
- **Dependencies**: 2.2, 2.4, 1.11
- **Testing**: Owner sends invite → viewer receives email → viewer can sign up as viewer role
- **[x] Complete

### 8.3 Add Google OAuth connection status
- **Deliverable**: Show if Google OAuth is connected; button to reconnect if needed
- **Dependencies**: 8.1
- **Testing**: Status shows correctly; reconnect flow works
- **[x] Complete

### 8.4 Build viewer management (list, revoke access)
- **Deliverable**: List of invited viewers with revoke button
- **Dependencies**: 8.2
- **Testing**: Revoke → viewer can no longer access data
- **[x] Complete

---

## 9. PDF + Testing

### 9.1 Add regression test for PDF generation
- **Deliverable**: pytest test comparing PDF output with known-good baseline
- **Dependencies**: 1.10
- **Testing**: Test passes with current pdf_generator.py output
- **[x] Complete

### 9.2 Add Playwright E2E tests
- **Deliverable**: E2E tests for critical flows: signup, create evaluation, view results
- **Dependencies**: 2.1, 3.1, 4.5, 5.1
- **Testing**: `npx playwright test` passes; all critical flows work
- **[x] Complete

### 9.3 Add React Query integration tests
- **Deliverable**: Tests for API hooks (useEvaluation, useCreateEvaluation, etc.)
- **Dependencies**: 2.4, 1.8
- **Testing**: Tests mock API; all hooks return correct data shape
- **[x] Complete

### 9.4 Verify PDF with real evaluation data
- **Deliverable**: Generate PDF from a real evaluation; verify in Adobe Reader
- **Dependencies**: 9.1, 5.5
- **Testing**: PDF content matches evaluation data exactly
- **[x] Complete

---

## 10. Polish + Deploy

### 10.1 Responsive QA pass
- **Deliverable**: Test all pages at 375px (mobile), 768px (tablet), 1440px (desktop)
- **Dependencies**: All prior phases
- **Testing**: All pages functional and visually correct at all breakpoints
- **[x] Complete

### 10.2 Performance audit
- **Deliverable**: Lighthouse score ≥90 on Performance, Accessibility, Best Practices, SEO
- **Dependencies**: 10.1
- **Testing**: Run Lighthouse CI; scores meet threshold
- **[x] Complete

### 10.3 Production environment variables
- **Deliverable**: All env vars set in Vercel (frontend) and Railway (backend)
- **Dependencies**: 0.8, 10.1
- **Testing**: Production build works with real Supabase project
- **[x] Complete

### 10.4 DNS and custom domain (if needed)
- **Deliverable**: Custom domain configured in Vercel
- **Dependencies**: 10.3
- **Testing**: App accessible at custom domain
- **[x] Complete

### 10.5 Archive legacy app.py
- **Deliverable**: Move app.py to `legacy/` branch; delete from main
- **Dependencies**: 10.1
- **Testing**: No Streamlit dependency in main branch; legacy branch preserved in git
- **[x] Complete

### 10.6 Final smoke test in production
- **Deliverable**: Full flow tested in production: signup → evaluate → results → PDF
- **Dependencies**: 10.3
- **Testing**: All flows work in production; no console errors
- **[x] Complete

---

## Task Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| 0. Setup | 0.1–0.8 | 🔲 Not started |
| 1. Backend API | 1.1–1.13 | 🔲 Not started |
| 2. Frontend Base | 2.1–2.8 | ✅ Complete |
| 3. Dashboard + Layout | 3.1–3.5 | ✅ Complete |
| 4. Formularios PA/PO | 4.1–4.6 | ✅ Complete |
| 5. Resultados + Charts | 5.1–5.6 | ✅ Complete |
| 6. Recomendaciones + Plan | 6.1–6.4 | ✅ Complete |
| 7. Historial + Benchmarking | 7.1–7.5 | ✅ Complete |
| 8. Settings + Invites | 8.1–8.4 | ✅ Complete |
| 9. PDF + Testing | 9.1–9.4 | ✅ Complete |
| 10. Polish + Deploy | 10.1–10.6 | ✅ Complete |

**Total**: 63 tasks across 10 phases (~11-12 weeks)