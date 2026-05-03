# Implementation Progress

**Change**: remove-auth-and-fix-bugs
**Mode**: Standard (Strict TDD not active)

## Phase 1: Backend Auth Removal

### Completed Tasks
- [x] 1.1 Delete `backend/app/auth/router.py` (all auth endpoints)
- [x] 1.2 Delete `backend/app/auth/schemas.py` (all auth schemas)
- [x] 1.3 Delete `backend/app/core/dependencies.py` (`get_current_user` dependency) - then recreated with `get_guest_user`
- [x] 1.4 Delete `backend/app/core/security.py` (`verify_token` function)
- [x] 1.5 Update `backend/app/api/router.py` — remove `auth_router` import and inclusion
- [x] 1.6 Remove `Depends(get_current_user)` from `backend/app/api/evaluations.py` (all endpoints)
- [x] 1.7 Remove `Depends(get_current_user)` from `backend/app/api/profiles.py` (all endpoints)
- [x] 1.8 Remove `Depends(get_current_user)` from `backend/app/api/action_plans.py` (all endpoints)
- [x] 1.9 Remove `Depends(get_current_user)` from `backend/app/api/matrices.py` (all endpoints)
- [x] 1.10 Remove `Depends(get_current_user)` from `backend/app/api/results.py` (all endpoints)
- [x] 1.11 Remove `Depends(get_current_user)` from `backend/app/api/pdf.py` (all endpoints)
- [x] 1.12 Remove `Depends(get_current_user)` from `backend/app/api/recommendations.py` (all endpoints)
- [x] 1.13 Delete `backend/app/api/invites.py` — viewer invite system no longer needed

## Phase 4: Supabase RLS Policies

- [x] 4.1 Update `profiles` table RLS — allow public read/write (no auth required)
- [x] 4.2 Update `evaluations` table RLS — allow public read/write (no auth required)
- [x] 4.3 Update `action_plans` table RLS — allow public read/write (no auth required)
- [x] 4.4 Remove or relax RLS on `invites` table (or drop table if unused)

### Files Changed
| File | Action | What Was Done |
|------|--------|---------------|
| `backend/app/auth/router.py` | Deleted | Auth endpoints removed |
| `backend/app/auth/schemas.py` | Deleted | Auth schemas removed |
| `backend/app/core/security.py` | Deleted | Token verification removed |
| `backend/app/api/invites.py` | Deleted | Invite system removed |
| `backend/app/core/dependencies.py` | Recreated | Replaced `get_current_user` with `get_guest_user` returning hardcoded guest user |
| `backend/app/api/router.py` | Modified | Removed auth_router import and inclusion |
| `backend/app/api/evaluations.py` | Modified | Removed auth dependencies, use anon key, removed user_id filters |
| `backend/app/api/profiles.py` | Modified | Removed auth dependencies, return default guest profile |
| `backend/app/api/action_plans.py` | Modified | Removed auth dependencies, removed ownership checks |
| `backend/app/api/matrices.py` | Modified | Removed auth dependency, matrices already populated |
| `backend/app/api/results.py` | Modified | Removed auth dependency |
| `backend/app/api/pdf.py` | Modified | Removed auth dependency, use establishment_name from settings |
| `backend/app/api/recommendations.py` | Modified | Removed auth, uses evaluation_id to filter recommendations |
| `backend/supabase_schema.sql` | Created | SQL to disable RLS on all tables |

### Deviations from Design
None — implementation matches design.

### Issues Found
None.

### Remaining Tasks (Phases 2, 3, 5 not implemented)
- Phase 2: Frontend auth removal (App.tsx, AuthPage, useAuth, authStore, api.ts, OnboardingPage, SettingsPage, AppShell)
- Phase 3: Bug fixes (EvaluationPage stub, matrices questions already populated, recommendations filtering, useApi hook, action plans ownership, PDF establishment_name)
- Phase 5: Testing/verification

### Status
Phase 1: 13/13 tasks complete ✓
Phase 4: 4/4 tasks complete ✓
**Overall: 17/85 tasks complete. Remaining phases not yet implemented.**