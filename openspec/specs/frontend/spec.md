# Delta for Frontend Domain

## MODIFIED Requirements

### Requirement: No Authentication Required

The system SHALL allow full access to all pages without authentication. No login, registration, or session SHALL be required. Users SHALL see the app shell immediately upon loading.
(Previously: All routes protected by ProtectedRoute; required auth token)

#### Scenario: App loads without auth

- GIVEN the user loads the app
- WHEN the page loads
- THEN the system SHALL display the app shell directly
- AND SHALL NOT redirect to `/login`
- AND SHALL NOT show any auth-related UI

#### Scenario: API requests without token

- GIVEN the app makes an API request
- WHEN the request is sent
- THEN the system SHALL NOT add `Authorization: Bearer` header
- AND the request SHALL use the Supabase anon key only

### Requirement: Removed Auth-Related UI

The system SHALL NOT render any authentication-related pages, components, or guards. The `/login` route SHALL NOT exist. ProtectedRoute and OnboardingGuard components SHALL be removed.
(Previously: AuthPage, ProtectedRoute, OnboardingGuard, authStore, useAuth hook existed)

#### Scenario: Login route removed

- GIVEN the user navigates to `/login`
- WHEN the navigation occurs
- THEN the system SHALL show a 404 or redirect to dashboard
- AND SHALL NOT show an auth form

#### Scenario: No auth interceptor on API

- GIVEN the user makes an API call
- WHEN the request is configured
- THEN the api client SHALL NOT read `gpp_token` from localStorage
- AND SHALL NOT add auth headers

## ADDED Requirements

### Requirement: Fixed useApi.ts Profile Endpoint

The `useUpdateProfile` hook SHALL use the correct API path `/profiles/me` instead of `/users/profile`. The system SHALL NOT make requests to non-existent endpoints.
(Previously: useApi.ts line 138 had wrong path `'/users/profile'`)

#### Scenario: Profile update uses correct path

- GIVEN the `useUpdateProfile` mutation is called with profile data
- WHEN the API request is made
- THEN the request SHALL be to `PUT /profiles/me`
- AND NOT to `PUT /users/profile`

### Requirement: EvaluationPage Connected to Wizard

The `EvaluationPage` SHALL be connected to the evaluation wizard. Navigating to `/evaluate/:id` SHALL load the existing evaluation in the wizard for editing. Navigating to `/evaluate` SHALL start a new evaluation.
(Previously: EvaluationPage was a stub with placeholder text)

#### Scenario: View existing evaluation

- GIVEN the user navigates to `/evaluate/abc123`
- WHEN the page loads
- THEN the system SHALL fetch evaluation `abc123`
- AND SHALL display it in the evaluation wizard

#### Scenario: Start new evaluation

- GIVEN the user clicks "Nueva Evaluación" on dashboard
- WHEN the navigation occurs
- THEN the system SHALL navigate to `/evaluate/wizard`
- AND SHALL show the evaluation wizard starting fresh
