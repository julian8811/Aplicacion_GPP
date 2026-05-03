# Auth Specification

## Purpose

Handles user registration, login (email + Google OAuth), session management, and onboarding flow. Integrates with Supabase Auth and enforces RLS-based role model.

## Requirements

### Requirement: Email/Password Registration

The system SHALL allow users to register with email and password via Supabase Auth. The registration endpoint MUST validate email format and require a password of at least 8 characters. Upon successful registration, the system SHALL create a `profiles` row with role `owner` and prompt the user to complete onboarding (establishment name).

#### Scenario: Successful email registration

- GIVEN the user is on the registration page
- WHEN the user submits a valid email and password (≥8 chars)
- THEN the system SHALL create a Supabase Auth account
- AND the system SHALL create a `profiles` row with `role=owner`
- AND the system SHALL redirect to the onboarding page

#### Scenario: Registration with invalid email

- GIVEN the user is on the registration page
- WHEN the user submits an invalid email format
- THEN the system SHALL display "Invalid email format"
- AND SHALL NOT attempt account creation

#### Scenario: Registration with short password

- GIVEN the user is on the registration page
- WHEN the user submits a password shorter than 8 characters
- THEN the system SHALL display "Password must be at least 8 characters"
- AND SHALL NOT attempt account creation

### Requirement: Google OAuth Login

The system SHALL allow users to authenticate via Google OAuth. The first-time login via Google SHALL create a `profiles` row with `role=owner`. Returning Google users SHALL be routed to the dashboard directly.

#### Scenario: First-time Google OAuth login

- GIVEN the user clicks "Continue with Google" and approves permissions
- WHEN the OAuth callback is received with a new Google email
- THEN the system SHALL create a Supabase Auth user
- AND the system SHALL create a `profiles` row with `role=owner`
- AND the system SHALL redirect to onboarding

#### Scenario: Returning Google OAuth user

- GIVEN a user previously registered via Google OAuth
- WHEN the user clicks "Continue with Google"
- THEN the system SHALL authenticate the existing user
- AND redirect to the dashboard

### Requirement: Login

The system SHALL authenticate users via email/password. Failed login SHALL display "Invalid email or password" without revealing which field is incorrect.

#### Scenario: Successful login

- GIVEN a registered user with email `user@example.com`
- WHEN the user submits correct credentials
- THEN the system SHALL issue a valid session
- AND redirect to `/dashboard`

#### Scenario: Failed login with wrong password

- GIVEN a registered user with email `user@example.com`
- WHEN the user submits wrong password
- THEN the system SHALL display "Invalid email or password"
- AND redirect to login page after 2 seconds

### Requirement: Onboarding

The system SHALL prompt new owners to enter their `establishment_name` before accessing the app. This field SHALL be stored in the `profiles` table and SHALL be editable in settings.

#### Scenario: Onboarding completion

- GIVEN a newly registered user reaches the onboarding page
- WHEN the user submits an establishment name
- THEN the system SHALL update `profiles.establishment_name`
- AND redirect to the dashboard

### Requirement: Protected Routes

The system SHALL redirect unauthenticated users to `/login` when accessing protected routes. Authenticated users accessing `/login` or `/register` SHALL redirect to `/dashboard`.

#### Scenario: Access dashboard without auth

- GIVEN a user navigates to `/dashboard` without a session
- WHEN the page loads
- THEN the system SHALL redirect to `/login`

#### Scenario: Access login while authenticated

- GIVEN an authenticated user navigates to `/login`
- WHEN the page loads
- THEN the system SHALL redirect to `/dashboard`