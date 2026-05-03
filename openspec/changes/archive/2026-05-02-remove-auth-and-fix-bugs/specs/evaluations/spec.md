# Delta for Evaluations Domain

## MODIFIED Requirements

### Requirement: List Evaluations

Authenticated users SHALL see a paginated list of their evaluations sorted by `fecha` descending. Each row SHALL display date, establishment name, general percentage, and status badge.
(Previously: Required authenticated user context)

#### Scenario: View evaluation list

- GIVEN the user is on `/history`
- WHEN the page loads
- THEN the system SHALL fetch and display all evaluations ordered by date descending
- AND SHALL show date, general_pct, pa_pct, po_pct, and status badge

#### Scenario: Empty evaluations list

- GIVEN the user has no evaluations
- WHEN the user navigates to `/history`
- THEN the system SHALL display "No hay evaluaciones. Crea tu primera evaluación."
- AND SHALL show a CTA button to start an evaluation

### Requirement: Create Evaluation

The system SHALL create a new evaluation record with a generated UUID, `fecha` set to today, and empty `evaluaciones_pa` and `evaluaciones_po` JSONB blobs. The system SHALL NOT require user authentication.
(Previously: Required user_id from authenticated session)

#### Scenario: Create new evaluation

- GIVEN the user is on the new evaluation page
- WHEN the user clicks "Nueva Evaluación"
- THEN the system SHALL create an evaluation record with today's date
- AND redirect to the evaluation wizard at step 1 (PA)

#### Scenario: Evaluation wizard navigation

- GIVEN the user is on the evaluation wizard
- WHEN the user completes PA step and clicks "Siguiente"
- THEN the system SHALL save PA draft and navigate to PO step
- AND when PO step is completed, SHALL navigate to review step

### Requirement: Delete Evaluation

The system SHALL allow any user to delete evaluations without authentication. Deletion SHALL cascade to linked `action_plans` records. The system SHALL prompt for confirmation before deletion.
(Previously: Required ownership verification via auth)

#### Scenario: Delete evaluation with confirmation

- GIVEN a user views an evaluation
- WHEN the user clicks "Eliminar" and confirms
- THEN the system SHALL delete the evaluation and its action plans
- AND redirect to the history page

### Requirement: Auto-save Draft

The system SHALL auto-save evaluation form data locally every 30 seconds during editing. The draft status SHALL be indicated with a "Guardado automático" toast notification.
(Previously: Saved to server via auth-protected endpoint)

#### Scenario: Auto-save triggers

- GIVEN the user is editing an evaluation form
- WHEN 30 seconds elapse without manual save
- THEN the system SHALL save current form state to local storage
- AND SHALL display "Guardado automático" toast

### Requirement: EvaluationPage Stub Fix

The system SHALL make `EvaluationPage` functional by displaying the evaluation wizard for creating new evaluations or connecting to existing evaluation data.
(Previously: Stub page with placeholder text)

#### Scenario: EvaluationPage displays wizard

- GIVEN the user navigates to `/evaluate/:id` with an existing evaluation ID
- WHEN the page loads
- THEN the system SHALL fetch and display that evaluation's data in the wizard
- AND SHALL allow editing of the evaluation

#### Scenario: EvaluationPage with new evaluation

- GIVEN the user navigates to `/evaluate` (no ID)
- WHEN the page loads
- THEN the system SHALL display the evaluation wizard starting at the PA step

## ADDED Requirements

### Requirement: Default User Context

The system SHALL operate without authentication by using a default/demo user context. All API calls SHALL work without Bearer token authentication. Supabase RLS policies SHALL be configured to allow anonymous read/write access.

#### Scenario: API calls without auth token

- GIVEN the app is loaded without any auth token
- WHEN any API endpoint is called (evaluations, matrices, results, etc.)
- THEN the system SHALL NOT include Authorization header
- AND the request SHALL succeed without 401 response

#### Scenario: Matrices endpoint accessible

- GIVEN the user navigates to `/evaluate/wizard`
- WHEN the matrices are fetched
- THEN the `/api/matrices` endpoint SHALL return complete PA and PO data
- AND SHALL NOT require authentication
