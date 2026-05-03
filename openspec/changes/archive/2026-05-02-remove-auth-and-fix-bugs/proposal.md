# Proposal: Remove Auth and Fix Bugs

## Intent

Remove the entire Supabase JWT authentication flow (login/registration) and make the app 100% functional without it. Additionally, fix all identified bugs to make the app fully operational.

## Scope

### In Scope
- Remove auth endpoints from backend (`/auth/*`)
- Remove auth middleware and security utilities (`get_current_user`, `verify_token`)
- Update all API endpoints to not require authentication
- Remove frontend auth pages, stores, and guards (`AuthPage`, `authStore`, `ProtectedRoute`, `OnboardingGuard`)
- Fix EvaluationPage stub (currently placeholder text)
- Populate Matrices data with complete PA/PO questions
- Fix Recommendations API to use `evaluation_id` parameter
- Fix `useApi.ts` wrong API path (`'/users/profile'` → `'/profiles/me'`)
- Update Supabase RLS policies for anonymous access
- Hardcode a default user context for the frontend

### Out of Scope
- New authentication mechanism
- Multi-user/data isolation
- User profiles or settings
- Invites system

## Capabilities

### New Capabilities
- `anonymous-access`: Full app functionality without authentication using anon key

### Modified Capabilities
- `evaluations`: Becomes publicly accessible (no user ownership)
- `recommendations`: Fixed to filter by `evaluation_id` instead of returning all
- `matrices`: Populated with complete PA/PO question data
- `evaluation-page`: Connected to real evaluation wizard/flow

## Approach

**Backend:**
1. Delete `backend/app/auth/` directory (router.py, schemas.py)
2. Delete `backend/app/core/dependencies.py` (get_current_user)
3. Delete `backend/app/core/security.py` (verify_token)
4. Remove auth_router from `backend/app/api/router.py`
5. Remove `Depends(get_current_user)` from all API endpoints
6. Delete `backend/app/api/invites.py` (viewer system relies on auth)
7. Update all endpoint functions to work without user context
8. Fix Recommendations API to filter by `evaluation_id`
9. Update Supabase RLS policies to allow anonymous read/write

**Frontend:**
1. Remove `/login` route and `AuthPage.tsx`
2. Remove `ProtectedRoute` and `OnboardingGuard` from App.tsx
3. Delete `authStore.ts` and `useAuth.ts`
4. Update `api.ts` to not add Bearer tokens or redirect on 401
5. Hardcode a default user context (anonymous user with default establishment)
6. Connect EvaluationPage to actual evaluation flow
7. Fix `useApi.ts` path for profile update

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `backend/app/auth/` | Removed | All auth endpoints and schemas |
| `backend/app/core/dependencies.py` | Removed | Auth dependency injection |
| `backend/app/core/security.py` | Removed | JWT verification |
| `backend/app/api/*.py` | Modified | Remove auth guards, add anonymous access |
| `backend/app/api/invites.py` | Removed | Viewer invite system |
| `frontend/src/pages/AuthPage.tsx` | Removed | Login/signup page |
| `frontend/src/stores/authStore.ts` | Removed | Auth state management |
| `frontend/src/hooks/useAuth.ts` | Removed | Auth hook |
| `frontend/src/App.tsx` | Modified | Remove auth guards, routing |
| `frontend/src/lib/api.ts` | Modified | Remove token interceptor |
| `frontend/src/pages/EvaluationPage.tsx` | Modified | Implement real evaluation flow |
| `frontend/src/hooks/useApi.ts` | Modified | Fix wrong API path |
| Supabase RLS | Modified | Allow anonymous access |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| All data becomes public/shared | High | Explicitly acknowledged per user request |
| Breaking other Supabase features | Medium | Test RLS policies after changes |
| EvaluationPage implementation effort | Medium | Scope to basic connected flow if complex |
| Matrices data completeness | Medium | Verify with business requirements |

## Rollback Plan

1. Revert all file deletions via git
2. Restore auth dependencies: `backend/app/auth/`, `dependencies.py`, `security.py`
3. Restore `Depends(get_current_user)` on all endpoint signatures
4. Restore frontend auth files and guards
5. Revert Supabase RLS policies to authenticated-only
6. Rollback is straightforward since all auth code is being deleted, not modified

## Dependencies

- Supabase anon key must be configured and allowed in RLS policies
- Exploration phase identified all bugs and affected files

## Success Criteria

- [ ] App loads and functions without any login/authentication
- [ ] All API endpoints respond without Authorization header
- [ ] EvaluationPage shows real evaluation form, not stub
- [ ] Matrices display complete PA/PO questions for all aspects
- [ ] Recommendations API filters correctly by evaluation_id
- [ ] Profile update works with corrected path `/profiles/me`
- [ ] No 401 errors in browser console
- [ ] All tests pass (pytest)
