# Exploration: Remove Auth and Fix Bugs

## Current State

### Backend Auth System

**Auth Endpoints (all in `/api/auth/*`):**
- `POST /auth/signup` - Creates user with Supabase Auth
- `POST /auth/login` - Authenticates user, returns token + profile
- `POST /auth/logout` - Dummy endpoint (no-op)
- `GET /auth/me` - Returns current user from token

**Auth Middleware:**
- `app/core/dependencies.py` - `get_current_user()` dependency that extracts JWT from `Authorization: Bearer <token>` header
- `app/core/security.py` - `verify_token()` function that validates JWT with Supabase

**Files:**
- `backend/app/auth/router.py` - Auth endpoints (116 lines)
- `backend/app/auth/schemas.py` - Pydantic models (UserCreate, UserLogin, UserResponse, TokenResponse)
- `backend/app/core/dependencies.py` - Auth dependency (19 lines)
- `backend/app/core/security.py` - Token verification (14 lines)

**Auth-protected API endpoints:**
All of these use `Depends(get_current_user)`:
- `GET/POST /evaluations` - List/create evaluations
- `GET/PUT/DELETE /evaluations/{id}` - CRUD single evaluation
- `GET/PATCH /profiles/me` - Get/update profile
- `GET/POST /action-plans` - List/create action plans
- `PUT/DELETE /action-plans/{id}` - Update/delete action plans
- `POST /invites` - Create invite (owner only)
- `PUT /invites/accept` - Accept invite (viewer)
- `GET /matrices` - Get PA/PO matrices
- `POST /results/calculate` - Calculate results
- `GET /pdf/{id}` - Generate PDF

### Frontend Auth Flow

**Auth Components:**
- `frontend/src/pages/AuthPage.tsx` - Login/signup form (125 lines)
- `frontend/src/stores/authStore.ts` - Zustand store with user, token, isAuthenticated (76 lines)
- `frontend/src/hooks/useAuth.ts` - Hook wrapping authStore (16 lines)

**Auth Guards in App.tsx:**
- `ProtectedRoute` - Redirects to `/login` if not authenticated
- `OnboardingGuard` - Shows OnboardingPage if user.role === 'owner' && !user.establishment_name

**API Client:**
- `frontend/src/lib/api.ts` - Axios instance that adds Bearer token to every request and redirects to `/login` on 401

### Supabase Schema (assumed)

Tables:
- `auth.users` - Supabase managed
- `profiles` - id, email, full_name, role ('owner'|'viewer'), establishment_name
- `evaluations` - id, user_id, fecha, general_pct, pa_pct, po_pct, evaluaciones_pa, evaluaciones_po
- `action_plans` - id, evaluation_id, element, action, responsible, due_date, status
- `invites` - id, owner_id, email, token, expires_at, accepted

## Affected Areas

### Files Requiring Modification (Auth Removal)

**Backend:**
- `backend/app/auth/router.py` - DELETE all auth endpoints
- `backend/app/auth/schemas.py` - DELETE all auth schemas
- `backend/app/core/dependencies.py` - DELETE get_current_user dependency
- `backend/app/core/security.py` - DELETE verify_token function
- `backend/app/api/router.py` - Remove auth_router import/inclusion
- `backend/app/api/evaluations.py` - Remove `Depends(get_current_user)` from all endpoints
- `backend/app/api/profiles.py` - Remove `Depends(get_current_user)` from all endpoints
- `backend/app/api/action_plans.py` - Remove `Depends(get_current_user)` from all endpoints
- `backend/app/api/invites.py` - Remove entire invites router (viewer system)
- `backend/app/api/matrices.py` - Remove `Depends(get_current_user)` from all endpoints
- `backend/app/api/results.py` - Remove `Depends(get_current_user)` from all endpoints
- `backend/app/api/pdf.py` - Remove `Depends(get_current_user)` from all endpoints
- `backend/app/api/recommendations.py` - Remove `Depends(get_current_user)` from all endpoints
- `backend/main.py` - May need CORS adjustment if removing login page

**Frontend:**
- `frontend/src/App.tsx` - Remove ProtectedRoute, OnboardingGuard, /login route
- `frontend/src/pages/AuthPage.tsx` - DELETE entire file
- `frontend/src/stores/authStore.ts` - Delete or repurpose (remove auth state)
- `frontend/src/hooks/useAuth.ts` - DELETE entire file
- `frontend/src/lib/api.ts` - Remove auth interceptor, remove 401 redirect to login
- `frontend/src/pages/OnboardingPage.tsx` - DELETE entire file (establishment name no longer needed)
- `frontend/src/pages/SettingsPage.tsx` - Remove profile editing, invites, Google auth sections
- `frontend/src/components/layout/AppShell.tsx` - May need adjustment if onboarding logic removed

### Additional Issues Found

1. **EvaluationPage.tsx (line 1-8)** - Stub page with placeholder text:
   ```tsx
   export function EvaluationPage() {
     return (
       <div className="space-y-6">
         <h1 className="text-2xl font-bold text-foreground">Nueva Evaluacion</h1>
         <p className="text-muted-foreground">Evaluation wizard coming soon...</p>
       </div>
     )
   }
   ```
   This is a placeholder - no real functionality.

2. **Matrices data is incomplete** - In `backend/app/api/matrices.py`:
   - PA has data for PLANEACIÓN only (questions 0-2)
   - ORGANIZACIÓN, DIRECCIÓN, CONTROL are empty objects `{}`
   - PO is entirely empty `{}` - only has structure labels

3. **Results calculation inconsistency** - In `backend/app/api/results.py`:
   - Takes `evals_pa` and `evals_po` directly instead of fetching from evaluation
   - Results are calculated but not persisted to the evaluation record
   - The frontend sends data directly to calculate, but evaluations store data separately

4. **Recommendations API** - In `backend/app/api/recommendations.py`:
   - Takes `evaluation_id` parameter but ignores it
   - Returns ALL recommendations with hardcoded "ALTA" priority
   - Does not filter based on actual evaluation scores

5. **PDF generation** - In `backend/app/api/pdf.py`:
   - Gets establishment_name from profile query, but profile requires auth
   - Without auth, establishment_name will always be "Unknown"

6. **Invites system** - In `frontend/src/pages/SettingsPage.tsx`:
   - Uses `/users/profile` endpoint but frontend API has no such endpoint (uses `/profiles/me`)
   - The `useUpdateProfile` hook in `useApi.ts` line 138 has wrong path: `'/users/profile'` should be `'/profiles/me'`

7. **Action Plans ownership check** - In `backend/app/api/action_plans.py`:
   - Line 55-57: Gets action plan by ID but doesn't verify ownership before allowing updates
   - Lines 59-63: Does verify through evaluation ownership for updates
   - But line 54-58 is before the ownership check - could leak data

8. **AuthStore persists to localStorage** - `frontend/src/stores/authStore.ts`:
   - Persists user and isAuthenticated state
   - On 401 response, auth token is removed but state may remain inconsistent

## Approaches

### Approach 1: Remove Auth Completely (Anonymous App)

**Description:** Make the app fully public with no authentication. All API endpoints become publicly accessible. Frontend removes all auth-related UI.

**Pros:**
- Simplest approach - no more auth complexity
- No user accounts to manage
- Works immediately without setup

**Cons:**
- All data is shared/public (everyone sees same evaluations)
- No personalization or user-specific data
- Cannot track who created what
- If this was meant to be multi-tenant, this breaks that entirely

**Effort:** Medium

### Approach 2: Make Auth Optional with Local Storage (Simpler Multi-user)

**Description:** Instead of removing auth entirely, use anonymous/magic link auth or local storage to create a simple user session without Supabase Auth complexity.

**Pros:**
- Keeps some user separation
- Simpler than full Supabase auth flow
- Can still have establishment names per user

**Cons:**
- Still requires some auth infrastructure
- May be over-engineering if user just wants simpler

**Effort:** Medium-High

## Recommendation

Based on the user's explicit request to "Remove registration and login (no auth)", **Approach 1** is recommended - fully remove auth.

However, be aware this means:
- All evaluations will be shared/public
- No way to distinguish who created what
- The "establishment_name" concept becomes global rather than per-user

If the intent was to have a simpler auth that doesn't require Supabase (e.g., local storage based), that would be a different approach.

**For the Bugs:**
1. EvaluationPage needs to be completed or connected to the wizard
2. Matrices data needs to be populated with real questions for all PA and PO aspects
3. Results calculation and storage flow needs review
4. Recommendations endpoint needs to actually use evaluation_id

## Risks

1. **Data model assumptions** - All evaluations are currently stored with `user_id`. Removing auth means `user_id` becomes meaningless or should be removed.
2. **Onboarding flow** - Current onboarding sets establishment_name on the profile. If removing auth, this flow needs alternative handling (maybe a settings page to set it without auth).
3. **Supabase dependency** - The app uses Supabase client throughout. If removing auth but keeping Supabase for data, need to ensure RLS policies are updated.
4. **Frontend routing** - Removing `/login` route and auth guards requires careful routing changes.

## Ready for Proposal

**Yes** - Ready to proceed with sdd-propose. The exploration is complete.

Key changes to propose:
1. Backend: Remove all auth endpoints and middleware
2. Frontend: Remove AuthPage, ProtectedRoute, OnboardingGuard, authStore
3. Fix EvaluationPage to be functional
4. Populate matrices with complete question data
5. Fix recommendations API to actually filter by evaluation
6. Fix any other bugs found during exploration