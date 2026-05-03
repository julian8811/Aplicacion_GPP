# Design: Remove Auth and Fix Bugs

## Technical Approach

Remove Supabase Auth entirely, making the app fully public. All API endpoints use the anon key. A hardcoded guest user context replaces auth state. RLS policies in Supabase are updated to allow public access.

## Architecture Decisions

### Decision: Guest User Context

**Choice**: Replace auth with a static guest user context rather than removing user_id columns
**Alternatives considered**: Remove user_id entirely (breaks foreign keys), keep Supabase auth but make optional
**Rationale**: Guest context allows existing data model to work without migration. Hardcoded UUID `00000000-0000-0000-0000-000000000000` serves as the guest identifier.

### Decision: Anon Key Only

**Choice**: All Supabase operations use `settings.supabase_anon_key`
**Alternatives considered**: Per-request key switching, service role for writes
**Rationale**: Simplicity. The anon key works for all operations once RLS is disabled.

### Decision: Remove Auth Dependencies from All Endpoints

**Choice**: Remove `Depends(get_current_user)` from every endpoint
**Alternatives considered**: Keep dependency but make it optional, create a passthrough guest dependency
**Rationale**: Auth is being removed entirely. A no-op dependency makes more sense than keeping the structure.

## Data Flow

```
Frontend (Guest Context)
    │
    ▼
API Endpoints (no auth check)
    │
    ▼
Supabase Client (anon key)
    │
    ▼
Postgres (RLS disabled for public access)
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `backend/app/auth/router.py` | Delete | Auth endpoints (signup, login, logout, me) |
| `backend/app/auth/schemas.py` | Delete | UserCreate, UserLogin, UserResponse, TokenResponse |
| `backend/app/core/dependencies.py` | Modify | Remove `get_current_user`, add `get_guest_user` returning hardcoded dict |
| `backend/app/core/security.py` | Delete | `verify_token` function |
| `backend/app/api/router.py` | Modify | Remove `auth_router` import and inclusion |
| `backend/app/api/evaluations.py` | Modify | Use anon key, `Depends(get_guest_user)`, remove user_id filtering |
| `backend/app/api/profiles.py` | Modify | Remove auth dependency (or make optional) |
| `backend/app/api/action_plans.py` | Modify | Use anon key, remove ownership checks |
| `backend/app/api/invites.py` | Delete | Viewer invite system no longer needed |
| `backend/app/api/matrices.py` | Modify | Remove auth, complete PA/PO question data |
| `backend/app/api/results.py` | Modify | Remove auth, persist results to evaluation |
| `backend/app/api/pdf.py` | Modify | Remove auth dependency |
| `backend/app/api/recommendations.py` | Modify | Actually use evaluation_id to filter recommendations |
| `frontend/src/App.tsx` | Modify | Remove ProtectedRoute/OnboardingGuard, direct routing |
| `frontend/src/pages/AuthPage.tsx` | Delete | Login/signup page |
| `frontend/src/pages/OnboardingPage.tsx` | Delete | Not needed without profile system |
| `frontend/src/stores/authStore.ts` | Delete | Auth state store |
| `frontend/src/hooks/useAuth.ts` | Delete | Auth hook |
| `frontend/src/lib/api.ts` | Modify | Remove token interceptor, remove 401 redirect |
| `frontend/src/contexts/GuestUserContext.tsx` | Create | Provide hardcoded guest user to components |
| `frontend/src/hooks/useApi.ts` | Modify | Fix `/users/profile` → `/profiles/me` |

## Backend Detailed Changes

### dependencies.py
```python
# Replace get_current_user with:
async def get_guest_user():
    """Returns a hardcoded guest user for all requests"""
    return {
        "id": "00000000-0000-0000-0000-000000000000",
        "email": "guest@local",
        "role": "owner"
    }
```

### evaluations.py
```python
def get_supabase_client():
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)
# Remove user_id from inserts, remove .eq("user_id", ...) filters
```

### matrices.py
Complete the missing question data for ORGANIZACIÓN, DIRECCIÓN, CONTROL (PA) and all PO sections.

### recommendations.py
```python
# Fetch evaluation, filter recommendations based on low-scoring aspects
@router.get("")
async def get_recommendations(evaluation_id: str = None):
    if evaluation_id:
        # Fetch evaluation, determine which aspects scored low
        # Return only relevant recommendations with calculated priority
```

## Frontend Detailed Changes

### App.tsx
```tsx
// Remove ProtectedRoute and OnboardingGuard
// Remove /login route
// Make all routes direct children of Routes (no wrapper)
```

### GuestUserContext.tsx
```tsx
const guestUser = { id: "00000000-0000-0000-0000-000000000000", role: "owner" }
// Provide via context for components that currently use useAuth().user
```

### api.ts
```tsx
// Remove request interceptor
// Remove 401 response interceptor
// Remove Authorization header
```

### useApi.ts line 138
```typescript
// Change: '/users/profile' → '/profiles/me'
```

## Supabase Schema (RLS Policies)

Need to execute in Supabase:
```sql
-- Disable RLS on evaluations for public access
ALTER TABLE evaluations DISABLE ROW LEVEL SECURITY;
ALTER TABLE action_plans DISABLE ROW LEVEL SECURITY;
ALTER TABLE profiles DISABLE ROW LEVEL SECURITY;

-- Or if keeping some policies, set to allow anon key
```

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Guest context provides correct user object | Simple assertion test |
| Integration | API endpoints return data without auth | Test with anon key client |
| E2E | Full evaluation flow works without login | Playwright flow test |

## Migration / Rollout

1. Backend changes first (auth removal, bug fixes)
2. Frontend changes (routing, remove auth pages)
3. Supabase RLS policy update
4. No data migration required — guest user uses existing schema

## Open Questions

- [ ] Should we remove the `user_id` column from evaluations or keep it with guest UUID?
- [ ] Is there a Supabase schema file we should update, or is the schema managed elsewhere?