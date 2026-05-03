# Tasks: Remove Auth and Fix Bugs

## Phase 1: Backend Auth Removal

- [x] 1.1 Delete `backend/app/auth/router.py` (all auth endpoints)
- [x] 1.2 Delete `backend/app/auth/schemas.py` (all auth schemas)
- [x] 1.3 Delete `backend/app/core/dependencies.py` (`get_current_user` dependency)
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

## Phase 2: Frontend Auth Removal

- [x] 2.1 Update `frontend/src/App.tsx` — remove `ProtectedRoute`, `OnboardingGuard`, `/login` route
- [x] 2.2 Delete `frontend/src/pages/AuthPage.tsx`
- [x] 2.3 Delete `frontend/src/hooks/useAuth.ts`
- [x] 2.4 Delete `frontend/src/stores/authStore.ts`
- [x] 2.5 Update `frontend/src/lib/api.ts` — remove Bearer token interceptor, remove 401 redirect to `/login`
- [x] 2.6 Delete `frontend/src/pages/OnboardingPage.tsx` (establishment name no longer user-gated)
- [x] 2.7 Update `frontend/src/pages/SettingsPage.tsx` — remove invites section, profile editing for role/establishment
- [x] 2.8 Update `frontend/src/components/layout/AppShell.tsx` — remove onboarding logic

## Phase 3: Bug Fixes

### EvaluationPage
- [x] 3.1 Replace stub in `frontend/src/pages/EvaluationPage.tsx` with redirect to `NewEvaluationPage`

### Matrices Data
- [x] 3.2 Populate PA ORGANIZACIÓN questions in `backend/app/api/matrices.py`
- [x] 3.3 Populate PA DIRECCIÓN questions in `backend/app/api/matrices.py`
- [x] 3.4 Populate PA CONTROL questions in `backend/app/api/matrices.py`
- [x] 3.5 Populate PO questions (all sections) in `backend/app/api/matrices.py`

### Recommendations API
- [x] 3.6 Fix `backend/app/api/recommendations.py` to actually use `evaluation_id` parameter
- [x] 3.7 Filter recommendations based on evaluation's `no-cumple`/`cumple-parcial` answers
- [x] 3.8 Calculate priority from answer type (no-cumple=ALTA, cumple-parcial=MEDIA)

### useApi Hook
- [x] 3.9 Fix `useUpdateProfile` hook path in `frontend/src/hooks/useApi.ts` line 138: change `'/users/profile'` to `'/profiles/me'`

### Action Plans Ownership
- [x] 3.10 Fix ownership check in `backend/app/api/action_plans.py` — removed ownership verification (already done in Phase 1 auth removal)

### PDF Generation
- [x] 3.11 Update `backend/app/api/pdf.py` to use establishment_name from settings/config instead of profile query (already done in Phase 1)

## Phase 4: Supabase RLS Policies

- [x] 4.1 Update `profiles` table RLS — allow public read/write (no auth required)
- [x] 4.2 Update `evaluations` table RLS — allow public read/write (no auth required)
- [x] 4.3 Update `action_plans` table RLS — allow public read/write (no auth required)
- [x] 4.4 Remove or relax RLS on `invites` table (or drop table if unused)

## Phase 5: Testing / Verification

- [ ] 5.1 Run `pytest` — verify no auth-related test failures
- [ ] 5.2 Test `GET /api/evaluations` without auth token — should return 200
- [ ] 5.3 Test `GET /api/matrices` — verify all PA/PO sections have questions
- [ ] 5.4 Test `POST /api/results/calculate` with evaluation_id — verify recommendations filter by answers
- [ ] 5.5 Test evaluation creation flow (create → fill PA → fill PO → complete)
- [ ] 5.6 Test PDF generation — verify establishment_name appears correctly
- [ ] 5.7 Run `npm run build` — verify frontend builds without errors
- [ ] 5.8 Manual smoke test: navigate to `/`, `/evaluations`, `/settings` without auth

## Implementation Order

1. **Phase 1 (Backend Auth)** first — removes middleware dependencies other code may rely on
2. **Phase 4 (RLS Policies)** second — database layer changes needed before application queries work
3. **Phase 2 (Frontend Auth)** third — UI changes depend on backend being stable
4. **Phase 3 (Bug Fixes)** fourth — fixes to EvaluationPage, Matrices, Recommendations, useApi
5. **Phase 5 (Testing)** last — verify everything works end-to-end

## Notes

- Auth removal means all `user_id` fields become meaningless — consider removing from inserts or defaulting to `NULL`
- Without auth, establishment_name should be configurable via settings without user context
- All evaluations become publicly accessible to anyone with the API URL